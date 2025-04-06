from django.db import models
from django.contrib.auth.models import User

# ✅ Quiz Model
class Quiz(models.Model):
    title = models.CharField(max_length=200)  # Quiz ka naam
    created_at = models.DateTimeField(auto_now_add=True)  # Quiz banne ka time

    def __str__(self):
        return self.title


# ✅ Question Model
class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)  # Kis quiz se question belong karta hai
    text = models.TextField()  # Question ka actual text
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Easy')

    def __str__(self):
        return self.text


# ✅ Option Model
class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')  # Related to question
    text = models.CharField(max_length=200)  # Option ka text
    is_correct = models.BooleanField(default=False)  # Kya yeh sahi option hai?

    def __str__(self):
        return self.text


# ✅ UserResponse Model
class UserResponse(models.Model):
    user_name = models.CharField(max_length=255)  # Guest ya registered user ka naam
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=255)
    is_correct = models.BooleanField()  # Answer sahi tha ya nahi

    def __str__(self):
        return f"{self.user_name} - {self.question.text}"


# ✅ Result Model
class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Django User
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    total_questions = models.IntegerField()
    attempted = models.IntegerField()
    correct = models.IntegerField()
    incorrect = models.IntegerField()
    skipped = models.IntegerField(default=0)  # Agar skip ka use karna ho future mein
    score = models.FloatField()
    passed = models.BooleanField()

    def __str__(self):
        return f"{self.user.username} - {self.quiz.title}"
