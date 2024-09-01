from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, send_mail
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from .models import PostCategory
from django.conf import settings


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'news_created_email.html',
    {'text': preview,
     'link': f'{settings.SITE_URL}/news/{pk}',}
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )

    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers_emails =[]
        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, subscribers_emails)


