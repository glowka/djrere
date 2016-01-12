from django.db import models


class Comment(models.Model):
    link = models.ForeignKey('frontpage.FrontLink', related_name='comments')
    content = models.TextField()


class FrontLink(models.Model):
    href = models.CharField(max_length=255)
    description = models.TextField()
