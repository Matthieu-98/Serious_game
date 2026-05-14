from django.contrib import admin
from django.urls import path
from fate_95.views import (
    landing_view, home, game_view, result_view, gender_view, register_view,
    quest_choice_view, elemental_view, element_intro_view,
    reset_game, painter_view, painter_intro_view,
    chatbot_view,
    admin_login_view, admin_logout_view, admin_panel_view,
    admin_conseils_view, admin_questions_view,
    admin_session_detail_view,
    session_view,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Landing (code session)
    path('', landing_view, name='landing'),
    path('start/', home, name='home'),
    # Jeu
    path('gender/', gender_view, name='gender'),
    path('register/', register_view, name='register'),
    path('quests/', quest_choice_view, name='quests'),
    path('elemental/', elemental_view, name='elemental'),
    path('element_intro/', element_intro_view, name='element_intro'),
    path('game/', game_view, name='game'),
    path('result/', result_view, name='result'),
    path('reset/', reset_game, name='reset'),
    path('painter/', painter_view, name='painter'),
    path('painter_intro/', painter_intro_view, name='painter_intro'),
    path('chatbot/', chatbot_view, name='chatbot'),
    # Admin
    path('panel/', admin_panel_view, name='admin_panel'),
    path('panel/login/', admin_login_view, name='admin_login'),
    path('panel/logout/', admin_logout_view, name='admin_logout'),
    path('panel/conseils/', admin_conseils_view, name='admin_conseils'),
    path('panel/questions/', admin_questions_view, name='admin_questions'),
    path('panel/session/<str:code>/', admin_session_detail_view, name='admin_session_detail'),
    # Session publique
    path('session/', session_view, name='session'),
]
