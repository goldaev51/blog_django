from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q, Prefetch
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import generic

from .forms import PostForm, CommentForm
from .models import Post, Comment
from .tasks import send_email_comment as celery_send_email_new_comment


class PostsListView(generic.ListView):
    model = Post
    paginate_by = settings.PAGINATION_DATA_PER_PAGE
    queryset = Post.objects.filter(is_active=True)


class PostDetailView(generic.DetailView):
    model = Post

    def get_queryset(self):
        return self.model.objects.filter(Q(is_active=True) | Q(author_id=self.request.user.id)) \
            .prefetch_related(Prefetch('comments', queryset=Comment.objects.filter(is_published=True)))


def post_details(request, pk):
    post = get_object_or_404(Post.objects.filter(Q(is_active=True) | Q(author_id=request.user.id)), pk=pk)
    post_comments = post.comments.filter(is_published=True)

    page = request.GET.get('page', 1)
    paginator = Paginator(post_comments, 2)
    try:
        post_comments_paginated = paginator.page(page)
    except PageNotAnInteger:
        post_comments_paginated = paginator.page(1)
    except EmptyPage:
        post_comments_paginated = paginator.page(paginator.num_pages)

    return render(request, 'blog/post_details.html', {'post': post ,'page_obj': post_comments_paginated})


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
            post.pubdate = timezone.now()
            post.save()

            if settings.DEBUG:
                admin_email_body = f'New post created, please verify it {post.get_admin_post_url()}'
                celery_send_email_new_comment.delay('New post created', admin_email_body, 'admin@admin.com')

            return redirect('blog:post-detail', pk=post.id)
    else:
        form = PostForm
    return render(request, 'blog/post_form.html', {'form': form})


@login_required
def user_posts(request):
    posts = Post.objects.filter(author=request.user)
    return render(request, 'blog/user_posts_list.html', {'posts': posts})


def save_comment_form(request, form, template_name, post_pk):
    data = dict()
    post = get_object_or_404(Post, pk=post_pk)

    if request.method == 'POST':
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            data['form_is_valid'] = True
            comments = Comment.objects.filter(post=post).filter(is_published=True)
            data['html_comment_list'] = render_to_string('blog/includes/partial_comment_list.html', {
                'comments': comments
            })

            if settings.DEBUG:
                admin_email_body = f'New comment created, please verify it {comment.get_admin_comment_url()}'
                celery_send_email_new_comment.delay('New comment created', admin_email_body, 'admin@admin.com')

                post_owner_email_body = f'You received new comment for your post. Check it {post.get_post_url()}'
                celery_send_email_new_comment.delay('New comment created', post_owner_email_body, post.author.email)

        else:
            data['form_is_valid'] = False
    context = {'form': form, 'post_pk': post_pk}
    data['html_form'] = render_to_string(template_name, context, request=request)
    return JsonResponse(data)


def comment_create(request, pk):
    if request.method == 'POST':
        form = CommentForm(request.POST)
    else:
        if request.user.is_anonymous:
            form = CommentForm(initial={'username': 'anonim'})
        else:
            form = CommentForm(initial={'username': request.user.username})
    return save_comment_form(request, form, 'blog/includes/partial_comment_create.html', pk)
