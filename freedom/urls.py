from django.urls import path
from freedom import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.home, name='home'),

    path("allvoters", views.allvoters, name="allvoters"),
    path('scan_save_fingerprint/<uuid:id>/', views.scan_save_fingerprint, name='scan_save_fingerprint'),
    path('voter_details/<uuid:id>/', views.voter_details, name='voter_details'),
    path('verify', views.main, name = 'verify'),
    path('registration/voter.html', views.voter_register, name='voter_register'),
    path('registration/exit.html', views.exit, name='exit'),
    path('registration/candidate.html', views.candidate, name='candidate'),
    path('receive-fingerprint', views.receive_fingerprint_image, name='receive_fingerprint_image'),
    path('fingerpattern', views.store_fingerprint, name='fingerpattern'),
    path('scanner', views.scanner, name='scanner'),
    path('language', views.language, name='language'),
    path('sunbird/<str:id>/', views.sunbird, name='sunbird'),
    path('english_vote/<str:post_aspired_for>/', views.english_vote, name='english_vote'),
    path('luganda_vote/<str:post_aspired_for>/', views.luganda_vote, name='luganda_vote'),
    path('candidate_engvote/<str:post_aspired_for>/', views.candidate_engvote, name='candidate_engvote'),
    path('candidate_lugvote/<str:post_aspired_for>/', views.candidate_lugvote, name='candidate_lugvote'),
    path('select_post', views.select_post, name='select_post'),
    path('select_post_lug', views.select_post_lug, name='select_post_lug'),
    path('posteng_choice', views.posteng_choice, name='posteng_choice'),
    path('postlug_choice', views.postlug_choice, name='postlug_choice'),
    path('english_vote_keypad/<str:post_aspired_for>/', views.english_vote_keypad, name='english_vote_keypad'),
    path('luganda_vote_keypad/<str:post_aspired_for>/', views.luganda_vote_keypad, name='luganda_vote_keypad'),
    path('candidate_engvote_keypad/<str:post_aspired_for>/', views.candidate_engvote_keypad, name='candidate_engvote_keypad'),
    path('candidate_lugvote_keypad/<str:post_aspired_for>/', views.candidate_lugvote_keypad, name='candidate_lugvote_keypad'),
    path('select_post_lugkeypad', views.select_post_lugkeypad, name='select_post_lugkeypad'),
    path('language_keypad', views.language_keypad, name='language_keypad'),
    path('select_post_keypad', views.select_post_keypad, name='select_post_keypad'),
    path('posteng_choice_keypad', views.posteng_choice_keypad, name='posteng_choice_keypad'),
    path('postlug_choice_keypad', views.postlug_choice_keypad, name='postlug_choice_keypad'),
    path('sessions', views.sessions, name ='sessions'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
