from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.feed, name='feed'),
    path('profile/', views.profile, name='profile'),
    path('profile_view/<str:pk>', views.profile_view, name='profile_view'),
    path('add_photo/', views.add_photo, name='add_photo'),
    path('register/', views.register, name='register'),
    path('draft/', views.draft, name='draft'),
    path('edit_profile/<str:pk>', views.edit_profile, name='edit_profile'),
    path('edit_post/<str:pk>', views.edit_post, name='edit_post'),
    path('add_dp/<str:pk>', views.add_dp, name='add_dp'),
    path('post_detail/<str:pk>', views.post_detail, name='post_detail'),
    path('like/<str:pk>', views.like_photo, name='like_photo'),
    path('delete_post/<str:pk>', views.delete_post, name='delete_post'),
    path('delete_profile_photo/<str:pk>', views.delete_profile_photo, name='delete_profile_photo'),
    path('guest/', views.guest, name='guest'),
    path('friends/', views.friends, name='friends'),
    path('settings/', views.settings, name='settings'),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
