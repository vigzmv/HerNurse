from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class ModelUser(models.Model):
    USER_ROLES = (
        ('user', 'USER'),
        ('doctor', 'DOCTOR'),
        ('expert', 'EXPERT'),
    )

    user = models.ForeignKey(User)
    phone_number = models.CharField(max_length=10, blank=True, null=False)
    role = models.CharField(max_length=10, choices=USER_ROLES, default="user")
    age = models.IntegerField()

    def __str__(self):
        return str(self.user)

class ModelTag(models.Model):
    tagName = models.CharField(max_length=20, default="", blank=False, null=True)

    def __str__(self):
        return self.tagName


class ModelDiscuss(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    source = models.CharField(max_length=30, default="", blank=True)
    heading = models.CharField(max_length=250, default="", blank=False)
    body = models.TextField(default="")
    link = models.CharField(max_length=100, default="", blank=True)
    tag = models.ManyToManyField(ModelTag)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.heading

class ModelQuestion(models.Model):
    user = models.ForeignKey(User, blank=False, null=True)
    question = models.TextField(null=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

class ModelAnswer(models.Model):
    user = models.ForeignKey(User)
    ques = models.ForeignKey(ModelQuestion)
    answer = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.answer
