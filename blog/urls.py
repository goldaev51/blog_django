from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('posts/', views.PostsListView.as_view(), name='posts-list'),
    path('post/<int:pk>', views.post_details, name='post-detail'),
    path('post/<int:pk>/comment/', views.comment_create, name='post-comment'),

    path('update-post/<int:pk>', views.PostUpdate.as_view(), name='post-update'),
    path('delete-post/<int:pk>', views.PostDelete.as_view(), name='post-delete'),
    path('create-post/', views.create_new_post, name='post-create'),
    path('my-posts/', views.user_posts, name='user-posts'),
]
