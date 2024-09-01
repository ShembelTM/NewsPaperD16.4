from datetime import *
import datetime
from django.conf import settings
from django.conf.global_settings import DEFAULT_FROM_EMAIL
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Post, Category
from NewsPaper import settings
from django.utils import timezone


@shared_task
def weekly_email_job():
    today = datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(time_create__gte=last_week)
    categories = set(posts.values_list('category__name', flat=True))
    subscribers = set(
        Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'posts/posts_created_last_week.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,

        }
    )
    msg = EmailMultiAlternatives(
        subject='Статьи за неделю',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def notify_about_new_post(pk):
    post = Post.objects.get(pk=pk)
    categories = post.postCategory.all()
    subscribers = []
    for category in categories:
        subscribers_user = category.subscribers.all()
        for user in subscribers_user:
            subscribers.append(user.email)
    html_context = render_to_string(
        'news_created_email.html',
        {
            'text': post.models.News.description,
            'link': f'{settings.SITE_URL}/{pk}'
        }
    )

    msg = EmailMultiAlternatives(
        subject=post.name,
        body='',
        from_email=DEFAULT_FROM_EMAIL,
        to=subscribers,
    )

    msg.attach_alternative(html_context, 'text/html')
    msg.send()