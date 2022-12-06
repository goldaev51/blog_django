from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Post, Comment
from .forms import PostForm

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
        if self.model.objects.filter(author=self.request.user) is None:
            return self.model.objects.all()
        else:
            return self.model.objects.filter(is_active=True)


# class PostCreate(LoginRequiredMixin, generic.CreateView):
#     model = Post
#     fields = ['title', 'short_description', 'description', 'image_field', 'is_active']


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



