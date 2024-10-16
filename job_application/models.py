from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


class Job(models.Model):
    status_choices = [
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected'),
        ('Accepted', 'Accepted'),
        ('Withdrawn', 'Withdrawn'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    date_applied = models.DateTimeField(default=datetime.now)
    status = models.CharField(max_length=100, choices=status_choices)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_applied']
        verbose_name_plural = 'Jobs'


class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_type = models.CharField(max_length=20)


class Note(models.Model):
    job = models.ForeignKey(
        Job, on_delete=models.CASCADE, related_name='notes')
    notes = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Note for {self.job.title} - {self.date_created.strftime('%Y-%m-%d')}"
