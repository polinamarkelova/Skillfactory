from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


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
        self.author_rating = 0
        self.total_comment_rating = 0
        self.total_post_rating = 0
        self.total_comment_post = 0
        for com_iter in Comment.objects.filter(comment_user=self.author):
            self.total_comment_rating = self.total_comment_rating + com_iter.comment_rating
        for post_iter in Post.objects.filter(author=self):
            self.total_post_rating = self.total_post_rating + post_iter.post_rating
            for com_iter in Comment.objects.filter(comment_post=post_iter):
                self.total_comment_post = self.total_comment_post + com_iter.comment_rating
        self.author_rating = (self.total_post_rating * 3) + self.total_comment_rating + self.total_comment_post
        self.save()

    def __str__(self):
        return self.author.username


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
    category = models.ManyToManyField('Category', through='PostCategory', related_name='post')
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

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Category(BaseModel):
    category_name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.category_name


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
