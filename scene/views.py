from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import TemplateView

from judge.models import CombatSolution, GameSolution
from judge.views import JudgeModule, create_solution
from scene.models import Scene, Challenge


class ChallengeJudgeModule(JudgeModule):

    @staticmethod
    def solve_rating(winner: CombatSolution, loser: CombatSolution, tie=False):
        def get_k(x):
            if x.rating < 2100:
                return 32
            elif x.rating < 2400:
                return 24
            else: return 16

        if winner.rating == 0:
            winner.rating = 1500
        if loser.rating == 0:
            loser.rating = 1500
        pa = 1 / (1 + pow(10, (loser.rating - winner.rating)) / 400)
        pb = 1 / (1 + pow(10, (winner.rating - loser.rating)) / 400)
        sa, sb = 1, 0
        if tie: sa, sb = 0.5, 0.5
        winner.rating += get_k(winner) * (sa - pa)
        loser.rating += get_k(loser) * (sb - pb)
        winner.save(update_fields=['rating'])
        loser.save(update_fields=['rating'])

    @staticmethod
    def judge_challenge(challenge, solution_a: CombatSolution, solution_b: CombatSolution, judge, time_limit):
        a, b, j = JudgeModule.judge_combat(solution_a, solution_b, judge, time_limit)
        challenge.report0_judge = j
        challenge.report1 = a
        challenge.report2 = b
        x, y = JudgeModule.fetch_score(j)
        challenge.score1, challenge.score2 = x, y
        challenge.save()
        if x >= y:
            ChallengeJudgeModule.solve_rating(solution_a, solution_b, tie=x == y)
        else:
            ChallengeJudgeModule.solve_rating(solution_b, solution_a)


class HomeView(ListView):
    template_name = 'base.html'
    queryset = Scene.objects.all()
    context_object_name = 'scene_list'


class SceneDetailedSubmitView(DetailView):
    queryset = Scene.objects.all()
    context_object_name = 'scene'
    template_name = 'scene/scene_base.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        ls = list(map(lambda x: x.pk, data['scene'].solutions.all()))
        if data['scene'].scene_type == 'game':
            data["solutions"] = GameSolution.objects.filter(pk__in=ls)
        else:
            data['solutions'] = CombatSolution.objects.filter(pk__in=ls)
        return data

    def post(self, request, pk):
        scene = get_object_or_404(Scene, pk=pk)
        solution = create_solution(request.POST['code'], request.POST["lang"], request.user, scene.scene_type)
        scene.solutions.add(solution)
        if scene.scene_type == 'game':
            JudgeModule.judge_game(solution, scene.judge, scene.time_limit / 1000)
        return redirect(request.path)


class SceneSolutionVisualizationView(TemplateView):
    template_name = 'scene/visualization.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['scene'] = get_object_or_404(Scene, pk=self.kwargs['pk'])
        data['solution'] = get_object_or_404(GameSolution, pk=self.kwargs['spk'])
        return data


class ChallengeListView(ListView):
    template_name = 'challenge/challenge_list.html'
    queryset = Challenge.objects.all()
    context_object_name = 'challenge_list'


class ChallengeVisualizationView(TemplateView):
    template_name = 'challenge/visualization.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['challenge'] = get_object_or_404(Challenge, pk=self.kwargs['pk'])
        data['scene'] = data['challenge'].belong_to
        return data


class ChallengeAcceptView(View):
    # again: get for demo purpose
    def get(self, request, pk):
        challenge = get_object_or_404(Challenge, pk=pk)
        ChallengeJudgeModule.judge_challenge(challenge, challenge.code1, challenge.code2, challenge.belong_to.judge,
                                             challenge.belong_to.time_limit / 1000)
        return redirect("/challenge/")
