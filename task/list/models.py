from django.db import models

# Create your models here.
class Task(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    isCompleted=models.BooleanField(default=False)

