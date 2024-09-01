from datetime import *

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        # Суммарный рейтинг статей
        post_ratings = sum([post.rating * 3 for post in self.post_set.all()])

        # Суммарный рейтинг комментариев автора
        author_comment_ratings = sum([comment.rating for comment in self.user.comment_set.all()])

        # Суммарный рейтинг комментариев к статьям автора
        post_comment_ratings = sum([comment.rating for comment in Comment.objects.filter(post__author=self)])

        # Общий рейтинг
        self.rating = post_ratings + author_comment_ratings + post_comment_ratings
        self.save()

    def __str__(self):
        return self.user.username


class Appointment(models.Model):
    date = models.DateField(
        default=datetime.utcnow,
    )
    client_name = models.CharField(
        max_length=200
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.client_name}: {self.message}'


class Category(models.Model):
    categoryName = models.CharField(max_length=64, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, null=True, related_name='categories')

    def __str__(self):
        return self.categoryName.title()


class Post(models.Model):
    ARTICLE = 'AR'
    NEWS = 'NW'
    POST_TYPE = [
        (ARTICLE, 'Статья'),
        (NEWS, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name='Автор')
    categoryType = models.CharField(max_length=2, choices=POST_TYPE, default=ARTICLE, verbose_name='Тип')
    dateCreation = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    postCategory = models.ManyToManyField(Category, through='PostCategory', verbose_name='Категория')
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст')
    rating = models.SmallIntegerField(default=0, verbose_name='Рейтинг')

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]} ...'

    def __str__(self):
        return f'{self.title.title()}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    #def __str__(self):
        #return f'{self.commentPost.title()}: {self.text[:20]}'