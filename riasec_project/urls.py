from django.contrib import admin
from django.urls import path
from fate_95.views import (
    home,
    game_view,
    result_view,
    gender_view,
    register_view,
    quest_choice_view,
    elemental_view,
    element_intro_view,
    reset_game,
    painter_view, 
    painter_intro_view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('gender/', gender_view, name='gender'),
    path('register/', register_view, name='register'),
    path('quests/', quest_choice_view, name='quests'),
    path('elemental/', elemental_view, name='elemental'),
    path('element_intro/', element_intro_view, name='element_intro'),
    path('game/', game_view, name='game'),
    path('result/', result_view, name='result'),
    path("reset/", reset_game, name="reset"),
    path("painter/", painter_view, name="painter"),
    path("painter_intro/", painter_intro_view, name="painter_intro"),
]