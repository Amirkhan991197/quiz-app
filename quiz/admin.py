from django.contrib import admin
from .models import Quiz, Question, Option, Result

# Question aur Options ko ek saath dikhane ke liye inline class
class OptionInline(admin.TabularInline):
    model = Option
    extra = 4  # Default 4 options show honge

# Question ko admin panel me achhe se show karne ke liye
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'difficulty')
    list_filter = ('quiz', 'difficulty')
    search_fields = ('text',)
    inlines = [OptionInline]  # Question ke saath options dikhane ke liye

# Result ke liye admin setup
class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'passed')
    list_filter = ('quiz', 'passed')

# Registering Models
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Result, ResultAdmin)
