from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('posts/', views.PostsListView.as_view(), name='posts-list'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('update-post/<int:pk>', views.PostUpdate.as_view(), name='post-update'),
    path('delete-post/<int:pk>', views.PostDelete.as_view(), name='post-delete'),
    path('create-post/', views.create_new_post, name='post-create'),
    path('my-posts/', views.user_posts, name='user-posts'),

    path('user/<int:pk>', views.UserPublicProfile.as_view(), name='user-data'),
    path('my-profile/', views.show_user_profile, name='user-profile'),
    path('update-profile/', views.update_user_profile, name='update-profile'),
]
