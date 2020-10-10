from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save


class UserProfile(models.Model):
    genders = ((0, 'Female'), (1, 'Male'))
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    profile_photo = models.ImageField(blank=True, null=True, upload_to='profile_photos')
    # date_of_birth = models.DateField(blank=True, null=True)
    gender = models.IntegerField(choices=genders, blank=True, null=True)
    mobile_number = models.CharField(max_length=10, blank=True, null=True, unique=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=50, default='', blank=True)
    account_disabled = models.BooleanField(default=False)


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])


post_save.connect(create_profile, sender=User)


class Photo(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    post_option = ((0, 'draft'), (1, 'publish'))
    photo = models.ImageField(upload_to='user_photos')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    created_on = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=True)
    location = models.CharField(max_length=50, blank=True)
    publish = models.IntegerField(choices=post_option, default=1)

    '''
    # Auto delete files from storage when deleted by user 
    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)
    '''

    class Meta:
        ordering = ['-created_on']


class Comment(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=1000)
    created_on = models.DateTimeField(auto_now_add=True)
    edited_on = models.DateTimeField(auto_now=True)
