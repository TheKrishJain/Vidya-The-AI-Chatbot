from django.contrib import admin
from django.urls import path, include
from . import views  # Assuming your views are in views.py
from .new import download_pdf  # Assuming your download_pdf function is in new.py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Your application's URL patterns
    path('', views.index, name='index'),  # Assuming you have an index view
    path('send-transcript/', views.send_transcript, name='send_transcript'),
    path('send-user-info/', views.send_user_info, name='send_user_info'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),
    path('api/suggested-questions/', views.suggested_questions, name='suggested_questions'),
    path('download/<str:filename>/', download_pdf, name='download_pdf'),  # Use the download_pdf function
     

    # Serve static and media files in development mode (optional)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)