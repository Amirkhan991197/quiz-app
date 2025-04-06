from django.db import models

class Question(models.Model):
    LEVEL_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.question_text


class UserResponse(models.Model):
    user_name = models.CharField(max_length=255)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.user_name} - {self.question}"
