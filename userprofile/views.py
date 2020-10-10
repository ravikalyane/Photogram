from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from .models import UserProfile, Photo, Comment
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def feed(request):
    user = request.user
    profile = UserProfile.objects.all()
    photos = Photo.objects.filter(publish=1)
    context = {'profile': profile, 'photos': photos, 'user': user}
    return render(request, 'feed.html', context)


def profile(request):
    try:
        profile = UserProfile.objects.filter(user=request.user)
        photos = Photo.objects.filter(user=request.user, publish=1)
        total_posts = Photo.objects.filter(user=request.user, publish=1).count()
    except:
        profile = UserProfile.objects.all()
        photos = Photo.objects.all()
        total_posts = Photo.objects.all()
    context = {'profile': profile, 'total_posts': total_posts,
               'photos': photos}
    return render(request, 'profile.html', context)


def draft(request):
    try:
        profile = UserProfile.objects.filter(user=request.user)
        photos = Photo.objects.filter(user=request.user, publish=0)
        total_posts = Photo.objects.filter(user=request.user).count()
    except:
        profile = UserProfile.objects.all()
        photos = Photo.objects.all()
        total_posts = Photo.objects.all()
    context = {'profile': profile, 'total_posts': total_posts,
               'photos': photos}
    return render(request, 'profile.html', context)


def post_detail(request, pk):
    photo = Photo.objects.get(id=pk)
    comment = photo.comments.all()
    comment_count = photo.comments.all().count()
    total_likes = photo.likes.all().count()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.photo = photo
            comment.user = request.user
            comment.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = CommentForm()
    context = {'photo': photo, 'comment': comment, 'form': form, 'comment_count': comment_count,
               'total_likes': total_likes}
    return render(request, 'post_detail.html', context)


def delete_post(request, pk):
    photo = Photo.objects.get(id=pk)
    photo.delete()
    return redirect('/profile')


def delete_profile_photo(request, pk):
    userprofile = UserProfile.objects.get(id=pk)
    if userprofile.user == request.user:
        profile_photo = userprofile.profile_photo
        profile_photo.delete()
        return redirect('/profile')
    else:
        return HttpResponse('<h1>Not Allowed</h1>')


def like_photo(request, pk):
    # photo = get_object_or_404(Photo, id=request.POST.get('photo_id'))
    photo = Photo.objects.get(id=pk)
    if photo.likes.filter(id=request.user.id).exists():
        photo.likes.remove(request.user)
    else:
        photo.likes.add(request.user)
    # return redirect('/')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def profile_view(request, pk):
    profile = UserProfile.objects.get(id=pk)
    photos = Photo.objects.filter(user=profile.user)
    total_posts = Photo.objects.filter(user=profile.user).count()
    return render(request, 'profile_view.html', {'profile': profile, 'photos': photos,
                                                 'total_posts': total_posts})


def friends(request):
    user = User.objects.all()
    return render(request, 'friends.html', {'user': user})


# Forms
def add_photo(request):
    profile = UserProfile.objects.all()
    photos = Photo.objects.all()
    if request.method == 'POST':
        form = AddPhoto(request.POST, request.FILES)
        if form.is_valid():
            # form.save()
            photos = form.save(commit=False)
            photos.user = request.user
            photos.save()
        return redirect('/')
    else:
        form = AddPhoto()
    return render(request, 'add_photo.html', {'profile': profile, 'form': form, 'photos': photos})


def add_dp(request, pk):
    profile = UserProfile.objects.get(id=pk)
    if request.method == 'POST':
        form = AddDp(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            # photos = form.save(commit=False)
            # photos.user = request.user
            # photos.save()
        return redirect('/profile')
    else:
        form = AddDp()
    return render(request, 'add_dp.html', {'profile': profile, 'form': form})


def edit_profile(request, pk):
    userprofile = UserProfile.objects.get(id=pk)
    if userprofile.user == request.user:
        if request.method == 'GET':
            userprofile = UserProfile.objects.get(id=pk)
            form = EditProfileForm(instance=userprofile)
        else:
            userprofile = UserProfile.objects.get(id=pk)
            form = EditProfileForm(request.POST, instance=userprofile)
            if form.is_valid():
                form.save()
                return redirect('/profile')
    else:
        return HttpResponse('<h1>Not Allowed</h1>')
    return render(request, 'edit_profile.html', {'form': form, 'userprofile': userprofile})


def edit_post(request, pk):
    user = request.user
    photo = Photo.objects.get(id=pk)
    if photo.user == user:
        if request.method == 'GET':
            form = PostUpdateForm(instance=photo)
        else:
            form = PostUpdateForm(request.POST, instance=photo)
            if form.is_valid():
                form.save()
                return redirect('/profile')
    else:
        return HttpResponse('<h1>NOT ALLOWED</h1>')
    return render(request, 'edit_post.html', {'photo': photo, 'form': form})


# Login and Register
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def guest(request):
    return render(request, 'guest.html')


def settings(request):
    return render(request, 'settings.html')
