"""aiplay2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib import auth
from django.contrib.auth.views import LoginView

from scene.views import HomeView, SceneDetailedSubmitView, SceneSolutionVisualizationView, ChallengeListView, \
    ChallengeAcceptView, ChallengeVisualizationView
from program.views import CodeListView, CodeDetailView, CodeCompileView

urlpatterns = [
    url(r'^$', HomeView.as_view()),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', LoginView.as_view()),
    url(r'^code/$', CodeListView.as_view()),
    url(r'^code/(?P<pk>\d+)/$', CodeDetailView.as_view(), name='code_detail'),
    url(r'^code/(?P<pk>\d+)/compile/$', CodeCompileView.as_view(), name='code_compile'),
    url(r'^scene/(?P<pk>\d+)/$', SceneDetailedSubmitView.as_view(), name='scene_detail'),
    url(r'^scene/(?P<pk>\d+)/solution/(?P<spk>\d+)/$', SceneSolutionVisualizationView.as_view(), name='scene_solution'),
    url(r'^challenge/$', ChallengeListView.as_view()),
    url(r'^challenge/(?P<pk>\d+)/accept/$', ChallengeAcceptView.as_view(), name='challenge_accept'),
    url(r'^challenge/(?P<pk>\d+)/$', ChallengeVisualizationView.as_view(), name='challenge_detail'),
]
