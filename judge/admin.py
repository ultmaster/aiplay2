from django.contrib import admin

from judge.models import CombatSolution, GameSolution, Solution

admin.site.register(Solution)
admin.site.register(CombatSolution)
admin.site.register(GameSolution)
