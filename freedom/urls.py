from django.urls import path
from freedom import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('', views.home, name='home'),

    path("allvoters", views.allvoters, name="allvoters"),
    path('scan_save_fingerprint/<uuid:id>/', views.scan_save_fingerprint, name='scan_save_fingerprint'),
    path('voter_details/<uuid:id>/', views.voter_details, name='voter_details'),


    path('registration/voter.html', views.voter_register, name='voter_register'),
    path('registration/exit.html', views.exit, name='exit'),
    path('registration/candidate.html', views.candidate, name='candidate'),
    path('receive-fingerprint', views.receive_fingerprint_image, name='receive_fingerprint_image'),
    path('fingerpattern', views.store_fingerprint, name='fingerpattern'),
    path('scanner', views.scanner, name='scanner'),
    path('language/', views.language, name='language'),
    path('sunbird/<str:id>/', views.sunbird, name='sunbird'),
    path('english_vote/<str:post_aspired_for>/', views.english_vote, name='english_vote'),
    path('luganda_vote/<str:post_aspired_for>/', views.luganda_vote, name='luganda_vote'),
    path('candidate_engvote/<str:post_aspired_for>/', views.candidate_engvote, name='candidate_engvote'),
    path('select_post/', views.select_post, name='select_post'),
    path('posteng_choice/', views.posteng_choice, name='posteng_choice'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
