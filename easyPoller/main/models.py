from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Poll(models.Model):
    #author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class AnswerOptions(models.Model):
    poll = models.ForeignKey(Poll, related_name="answer_option", on_delete=models.CASCADE)
    option = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
