from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Problem(models.Model):
    name = models.CharField(max_length=200, unique=True)
    desc = models.TextField()
    difficulty = models.CharField(max_length=200)
    inputFile = models.CharField(max_length=500)
    outputFile = models.CharField(max_length=500)

    def __str__(self) -> str:
        return self.name

class Submission(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    problemID = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='submissions')
    userID = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    verdict = models.CharField(max_length=30)
    code = models.CharField(max_length=500)

    def __str__(self) -> str:
        return str(self.timestamp)
