from django.db import models


class PageComment(models.Model):
    link = models.ForeignKey('frontpage.PageLink', related_name='pageComments')
    content = models.TextField()


class PageLink(models.Model):
    href = models.CharField(max_length=255)
    description = models.TextField()
    likes_num = models.IntegerField(default=0)
