from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.name

class StudySession(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    date = models.DateField()
    duration_minutes = models.IntegerField()
    notes = models.TextField(blank=True)