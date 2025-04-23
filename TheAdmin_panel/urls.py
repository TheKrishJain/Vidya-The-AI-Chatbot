from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views  # Import views from the current app

urlpatterns = [
  path('', views.index, name='admin_index'),  # URL for the index page
  path('login/', views.login_view, name='login'),  # Login page
  path('dashboard/', views.dashboard_view, name='dashboard'),  # Dashboard page after login
  path('dashboard/fetch/', views.dashboard, name='dashboard'),  # Dashboard page after login
  path('dashboard/get_user_details/', views.get_user_details, name='get_user_details'),
  path('dashboard/unique_user_details/', views.get_user_details, name='unique_user_details'),
  path('dashboard/upload/', views.upload_pdf, name='upload_pdf'),
  path('dashboard/send-notification-email/', views.send_notification_email, name='send_notification_email'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
