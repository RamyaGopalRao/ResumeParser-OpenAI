from django.db import models

class Resume(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    skills = models.TextField()

class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='education')
    degree = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    institution = models.CharField(max_length=200)
    year = models.CharField(max_length=4)

class Experience(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='experience')
    position = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
