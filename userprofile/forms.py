from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Photo, UserProfile, Comment
from PIL import Image


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'username', 'email', 'password1', 'password2'


class AddPhoto(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = Photo
        exclude = 'user', 'likes',
        fields = '__all__'

    def save(self, *args, **kwargs):
        photo = super(AddPhoto, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.photo)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((1080, 1080), Image.ANTIALIAS)
        resized_image.save(photo.photo.path)

        return photo


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = 'user', 'profile_photo'
        fields = '__all__'
        # fields = 'gender', 'mobile_number', 'bio', 'location', 'account_disabled'


class CommentForm(forms.ModelForm):
    comment = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment'}))

    class Meta:
        model = Comment
        exclude = 'photo', 'user'
        fields = '__all__'


# Add Dp

class AddDp(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = UserProfile
        fields = 'profile_photo',

    def save(self, *args, **kwargs):
        photo = super(AddDp, self).save()
        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.profile_photo)
        cropped_image = image.crop((x, y, w + x, h + y))
        resized_image = cropped_image.resize((1080, 1080), Image.ANTIALIAS)
        resized_image.save(photo.profile_photo.path)

        return photo


class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = 'user', 'photo', 'likes',
        fields = '__all__'
