from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views
from .views import (
    custom_login, custom_logout, quiz_list, quiz_start, quiz_question, submit_quiz,about,contact,gallery,
    generate_pdf, generate_excel, leaderboard,
    send_quiz_email, register
)

urlpatterns = [
    # 🏠 Home & Quiz URLs
    path('', quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/', quiz_start, name='quiz_start'),
    path('quiz/<int:quiz_id>/<str:difficulty>/', quiz_question, name='quiz_question'),
    path('submit/', submit_quiz, name='submit_quiz'),
    path('', views.quiz_list, name='home'), # ✅ Yeh hona chahiye


    # 🔐 Custom Login & Logout
    path('login/', custom_login, name='login'),
    path('logout/', custom_logout, name='logout'),

    # 📥 Reports
    path('download/pdf/<str:user_name>/', generate_pdf, name='download_pdf'),
    path('download/excel/<str:user_name>/', generate_excel, name='download_excel'),

    # 🏆 Leaderboard
    path('leaderboard/', leaderboard, name='leaderboard'),

    # 📩 Email
    path('send-email/<str:user_name>/', send_quiz_email, name='send_email'),

    #certificate
    path('certificate/<str:user_name>/', views.generate_certificate, name='download_certificate'),

    # 👤 Registration
    path('register/', register, name='register'),
    
    #navbar
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('gallery/', gallery, name='gallery'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
