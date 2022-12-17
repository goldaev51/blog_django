import datetime
import random

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from blog.models import Post, Comment


class Command(BaseCommand):

    def handle(self, *args, **options):
        # filling db with data
        self.create_users()
        self.create_posts()
        self.create_comments()
        self.stdout.write(self.style.SUCCESS('Database filled!'))

    def create_users(self):
        cnt = 10
        fake = Faker()
        users = list()
        for i in range(cnt):
            username = (fake.first_name() + fake.last_name()).lower()
            user_email = (username + '@' + fake.free_email_domain())
            password = make_password(fake.password())
            user = User(username=username, email=user_email, password=password)
            users.append(user)

        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS(f'Created {cnt} users'))

    def create_posts(self):
        cnt = 20
        posts = list()
        user_ids = User.objects.values_list('id', flat=True)
        user_ids_cnt = user_ids.count() - 1
        for i in range(cnt):
            title = f'Title_{i}'
            short_description = f'Short_Description_{i}'
            description = f'Description_{i}'
            is_active = True
            pubdate = make_random_date()
            post = Post(title=title,
                        short_description=short_description,
                        description=description,
                        is_active=is_active,
                        pubdate=pubdate)

            random_user_id = random.randint(0, user_ids_cnt)
            user = User.objects.get(pk=user_ids[random_user_id])
            post.author = user
            posts.append(post)

        Post.objects.bulk_create(posts)
        self.stdout.write(self.style.SUCCESS(f'Created {cnt} posts'))

    def create_comments(self):
        cnt = 40
        fake = Faker()
        post_ids = Post.objects.values_list('id', flat=True)
        post_ids_cnt = post_ids.count() - 1
        comments = list()
        for i in range(cnt):
            username = (fake.first_name() + fake.last_name()).lower()
            text = f'Comment_text_{i}'
            pubdate = timezone.now()
            is_published = True
            comment = Comment(username=username,
                              text=text,
                              pubdate=pubdate,
                              is_published=is_published)
            random_post_id = random.randint(0, post_ids_cnt)
            post = Post.objects.get(pk=post_ids[random_post_id])
            comment.post = post
            comments.append(comment)

        Comment.objects.bulk_create(comments)
        self.stdout.write(self.style.SUCCESS(f'Created {cnt} comments'))


# create random date between 01.10.1900 and 2022.10.30
def make_random_date():
    start_date = datetime.date(1900, 10, 1)
    end_date = datetime.date(2022, 10, 30)
    num_days = (end_date - start_date).days
    rand_days = random.randint(1, num_days)
    random_date = start_date + datetime.timedelta(days=rand_days)
    return random_date
