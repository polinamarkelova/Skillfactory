from django.db import models
from django.contrib.auth.models import User
from django.db.models import *


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


class Author(BaseModel):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.SmallIntegerField(default=0)

    @property
    def rating_author(self):
        return self.author_rating

    @rating_author.setter
    def rating_author(self, value):
        self.author_rating = int(value) if value >= 0 else 0
        self.save()

# функция к сожалению не работает, не знаю, как ее правильно записать(
    def update_rating(self):
        posts_rate = self.post_set.all().aggregate(post_sum=Sum('post_rating') * 3)['post_sum']
        self_comm_rate = self.user.comment_set.all().aggregate(self_comm_sum=Sum('comment_rating'))['self_comm_sum']
        total_comm_rate = self.post_set.all().aggregate(Sum('comment__comment_rating'))['comment__comment_rating__sum']
        own_post_rate = self.user.comment_set.all().filter(post__author_id=self.id).aggregate(Sum('comment_rating'))[
                'comment_rating__sum']
        self.author_rating = posts_rate + self_comm_rate + total_comm_rate - own_post_rate
        self.save()


class Post(BaseModel):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, null=False)
    text = models.TextField(null=False)

    news = 'NW'
    article = 'AR'

    CHOICES = [
        (news, 'Новость'),
        (article, 'Статья')
    ]

    post_type = models.CharField(max_length=2, choices=CHOICES, default=article)
    posting_time = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField('Category', through='PostCategory')
    post_rating = models.SmallIntegerField(default=0)

    @property
    def rating_post(self):
        return self.post_rating

    @rating_post.setter
    def rating_post(self, value):
        self.post_rating = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'


class Category(BaseModel):
    category_name = models.CharField(max_length=50, unique=True)


class PostCategory(BaseModel):
    post_connection = models.ForeignKey(Post, on_delete=models.CASCADE)
    category_connection = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(BaseModel):
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(null=False)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.SmallIntegerField(default=0)

    @property
    def rating_comment(self):
        return self.comment_rating

    @rating_comment.setter
    def rating_comment(self, value):
        self.comment_rating = int(value) if value >= 0 else 0
        self.save()

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
