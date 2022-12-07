from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse_lazy

from .models import Post, Comment
from .forms import PostForm, UpdateUserForm

from django.conf import settings
from django.shortcuts import render, redirect
from django.views import generic


class PostsListView(generic.ListView):
    model = Post
    paginate_by = settings.PAGINATION_DATA_PER_PAGE
    queryset = Post.objects.filter(is_active=True)


class PostDetailView(generic.DetailView):
    model = Post
    queryset = Post.objects.prefetch_related('comment_set')

    def get_queryset(self):
        return self.model.objects.filter(Q(is_active=True) | Q(author_id=self.request.user.id))


class PostUpdate(LoginRequiredMixin, generic.UpdateView):
    model = Post
    fields = ['title', 'short_description', 'description', 'image_field', 'is_active']

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class PostDelete(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:user-posts')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


@login_required
def create_new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post-detail', pk=post.id)
    else:
        form = PostForm
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def user_posts(request):
    posts = Post.objects.filter(author_id=request.user.id)
    return render(request, 'blog/user_posts_list.html', {'posts': posts})


class UserPublicProfile(generic.DetailView):
    model = User
    # queryset = User.objects.prefetch_related('post_set', 'comment_set').all()
    template_name = 'user_profile/public_profile.html'

class UserProfile(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'user_profile/user_profile.html'

    def get_queryset(self):
        return self.model.objects.filter(pk=self.request.user.id)

@login_required()
def show_user_profile(request):
    user = User.objects.get(pk=request.user.id)
    return render(request, 'user_profile/user_profile.html', {'user': user})


@login_required()
def update_user_profile(request):
    if request.method == 'POST':
        form = UpdateUserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect('blog:user-profile')
    else:
        form = UpdateUserForm(instance=request.user)
    return render(request, 'user_profile/update_user_profile.html', {'form': form})
