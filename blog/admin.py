from django.contrib import admin

from blog.models import Post, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'text', 'post_id', 'pubdate', 'is_published']
    list_filter = ['pubdate']
    search_fields = ['username', 'text']
    date_hierarchy = 'pubdate'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'short_description', 'author', 'pubdate', 'is_active']
    list_filter = ['pubdate']
    search_fields = ['title', 'author_username']
    date_hierarchy = 'pubdate'
