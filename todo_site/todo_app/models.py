from django.db import models

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

class Task(models.Model):
    description = models.CharField(max_length=255)
     # The `tags` field connects the `Tag` model to the `Task` model, automatically
     # creating a junction `task_tags` table in the database for us when migrated
    tags = models.ManyToManyField(Tag)

class Comment(models.Model):
    #id will be set for us
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
 