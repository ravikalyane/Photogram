from django.contrib import admin
from .models import UserProfile, Photo, Comment


class UserProfileAdmin(admin.ModelAdmin):
    list_display = 'user', 'id', 'gender'


class CommentAdmin(admin.ModelAdmin):
    list_display = 'user', 'comment', 'created_on'


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Photo)
admin.site.register(Comment, CommentAdmin)
