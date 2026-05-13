from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('kursus/', views.kursus, name='kursus'),
    path('komunitas/', views.komunitas, name='komunitas'),
    path('komunitas/<int:pk>/', views.komunitas_detail, name='komunitas_detail'),
    path('misi/', views.misi, name='misi'),
    path('misi/<int:mission_id>/materi/', views.materi_view, name='misi_materi'),
    path('misi/<int:mission_id>/kuis/', views.kuis_view, name='misi_kuis'),
    path('misi/<int:mission_id>/evaluasi/', views.evaluasi_view, name='misi_evaluasi'),
    path('misi/<int:mission_id>/selesai/', views.selesai_view, name='misi_selesai'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('pengaturan/', views.pengaturan, name='pengaturan'),
    path('pengaturan/avatar/', views.upload_avatar, name='upload_avatar'),

    # Admin Panel URLs
    path('panel/', views.admin_dashboard, name='admin_dashboard'),
    path('panel/users/', views.admin_users, name='admin_users'),
    path('panel/users/<int:user_id>/edit/', views.admin_user_edit, name='admin_user_edit'),
    path('panel/users/<int:user_id>/delete/', views.admin_user_delete, name='admin_user_delete'),
    path('panel/missions/', views.admin_missions, name='admin_missions'),
    path('panel/missions/create/', views.admin_mission_create, name='admin_mission_create'),
    path('panel/missions/<int:mission_id>/edit/', views.admin_mission_edit, name='admin_mission_edit'),
    path('panel/missions/<int:mission_id>/delete/', views.admin_mission_delete, name='admin_mission_delete'),
    path('panel/missions/<int:mission_id>/questions/', views.admin_questions, name='admin_questions'),
    path('panel/missions/<int:mission_id>/questions/create/', views.admin_question_create, name='admin_question_create'),
    path('panel/missions/<int:mission_id>/questions/<int:question_id>/delete/', views.admin_question_delete, name='admin_question_delete'),

    # Admin Course URLs
    path('panel/courses/', views.admin_courses, name='admin_courses'),
    path('panel/courses/create/', views.admin_course_create, name='admin_course_create'),
    path('panel/courses/<int:course_id>/edit/', views.admin_course_edit, name='admin_course_edit'),
    path('panel/courses/<int:course_id>/delete/', views.admin_course_delete, name='admin_course_delete'),

    # Admin Community URLs
    path('panel/community/', views.admin_community_rooms, name='admin_community_rooms'),
    path('panel/community/<int:room_id>/manage/', views.admin_community_room_manage, name='admin_community_room_manage'),

    # Gamification URLs
    path('gamifikasi/level1/', views.gamifikasi_level1, name='gamifikasi_level1'),
    path('gamifikasi/level2/', views.gamifikasi_level2, name='gamifikasi_level2'),
    path('gamifikasi/level3/', views.gamifikasi_level3, name='gamifikasi_level3'),
    path('gamifikasi/level4/', views.gamifikasi_level4, name='gamifikasi_level4'),
    path('gamifikasi/level5/', views.gamifikasi_level5, name='gamifikasi_level5'),
    # Serve module PDFs via Django view (inline with correct headers)
    path('modul/<str:filename>/', views.serve_modul_pdf, name='serve_modul_pdf'),
]
