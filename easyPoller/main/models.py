from django.db import models
from django.contrib.auth.models import User
import random
import string

# Create your models here.

class Poll(models.Model):
    #pauthor = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))

        # if another poll objects exists with this slug
        # generate a new slug
        while Poll.objects.filter(slug=self.slug).exists():
            self.slug = "".join(random.choices(string.ascii_lowercase + string.digits, k=4))

        # save
        super().save(*args, **kwargs)


class AnswerOptions(models.Model):
    poll = models.ForeignKey(Poll, related_name="answer_option", on_delete=models.CASCADE)
    option = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
