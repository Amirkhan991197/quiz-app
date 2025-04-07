from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Count, Q

from .models import Quiz, Question, Option, UserResponse, Result

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd


# ✅ Home Page - List of Quizzes
def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/home.html', {'quizzes': quizzes})

# ✅ Start Quiz Page
def quiz_start(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    return render(request, 'quiz/start.html', {'quiz': quiz})

# ✅ Fetch Questions Based on Difficulty
def quiz_question(request, quiz_id, difficulty):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = Question.objects.filter(quiz=quiz, difficulty=difficulty)
    return render(request, 'quiz/question.html', {'quiz': quiz, 'questions': questions})

# ✅ Submit Quiz
def submit_quiz(request):
    if request.method == "POST":
        user_name = request.POST.get("user_name", "Guest")
        quiz_id = request.POST.get("quiz_id")
        quiz = Quiz.objects.get(id=quiz_id)

        total_questions = 0
        attempted = 0
        correct_answers = 0
        incorrect_answers = 0
        score = 0

        questions = Question.objects.filter(quiz=quiz)
        for question in questions:
            total_questions += 1
            selected_option = request.POST.get(f"q{question.id}")

            if selected_option:
                attempted += 1
                correct_option = Option.objects.filter(question=question, is_correct=True).first()
                is_correct = selected_option == correct_option.text if correct_option else False

                UserResponse.objects.create(
                    user_name=user_name,
                    question=question,
                    selected_option=selected_option,
                    is_correct=is_correct
                )

                if is_correct:
                    correct_answers += 1
                else:
                    incorrect_answers += 1

        score = correct_answers * 1
        passing_score = int(0.5 * total_questions)
        passed = correct_answers >= passing_score

        # ✅ Result Save karo (agar user logged in hai)
        if request.user.is_authenticated:
            Result.objects.create(
                user=request.user,
                quiz=quiz,
                total_questions=total_questions,
                attempted=attempted,
                correct=correct_answers,
                incorrect=incorrect_answers,
                skipped=0,  # ❌ Skip count hata diya, 0 set kar diya
                score=score,
                passed=passed
            )

        return render(request, "quiz/result.html", {
    "user_name": user_name,
    "quiz": quiz,
    "score": score,
    "total_questions": total_questions,
    "attempted": attempted,
    "correct_answers": correct_answers,
    "incorrect_answers": incorrect_answers,
    "passed": passed,
    "passing_score": passing_score, 
})

    return redirect("home")

# ✅ Generate PDF Report
def generate_pdf(request, user_name):
    responses = UserResponse.objects.filter(user_name=user_name)
    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{user_name}_quiz_report.pdf"'
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y_position = height - 50
    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, y_position, "Quiz Report")
    y_position -= 40
    p.setFont("Helvetica", 12)
    p.drawString(50, y_position, f"User Name: {user_name}")
    y_position -= 20
    for res in responses:
        p.drawString(50, y_position, f"Q: {res.question.text}")
        p.drawString(50, y_position - 15, f"Your Answer: {res.selected_option}")
        p.drawString(50, y_position - 30, f"Result: {'✔ Correct' if res.is_correct else '❌ Incorrect'}")
        y_position -= 60
        if y_position < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y_position = height - 50
    p.save()
    return response

def generate_excel(request, user_name):
    responses = UserResponse.objects.filter(user_name=user_name)

    data = []
    for res in responses:
        # 🔍 Get correct option text from the Option model
        correct_option_obj = Option.objects.filter(question=res.question, is_correct=True).first()
        correct_option_text = correct_option_obj.text if correct_option_obj else "N/A"

        data.append({
            "Question": res.question.text,
            "Your Answer": res.selected_option,
            "Correct Answer": correct_option_text,
            "Result": "Correct" if res.is_correct else "Incorrect",
        })

    df = pd.DataFrame(data)

    # 📥 Create Excel Response
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = f'attachment; filename="{user_name}_quiz_report.xlsx"'

    # ✅ Write DataFrame to Excel
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="Quiz Results", index=False)

    return response

# ✅ Leaderboard
def leaderboard(request):
    leaderboard_data = UserResponse.objects.values("user_name").annotate(
        correct_answers=Count("id", filter=Q(is_correct=True)),
        total_attempts=Count("id")
    ).order_by("-correct_answers")[:10]
    return render(request, "quiz/leaderboard.html", {"leaderboard_data": leaderboard_data})

# ✅ Send Quiz Report via Email
def send_quiz_email(request, user_name):
    responses = UserResponse.objects.filter(user_name=user_name)
    subject = "Your Quiz Result"
    message = f"Hello {user_name},\n\nHere is your quiz result:\n"
    correct_answers = sum(res.is_correct for res in responses)
    for res in responses:
        message += f"Q: {res.question.text}\nYour Answer: {res.selected_option} ({'✔ Correct' if res.is_correct else '❌ Incorrect'})\n\n"
    message += f"\nTotal Correct Answers: {correct_answers}\n\nThank you for participating!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [f"{user_name}@gmail.com"])
    return HttpResponse("Email Sent Successfully!")

# ✅ User Registration
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect("register")
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return redirect("register")
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        login(request, user)
        messages.success(request, "Registration successful! You are now logged in.")
        return redirect("quiz_list")  # ✅ Fixed
    return render(request, "quiz/register.html")

# ✅ Protected Quiz Page
@login_required
def quiz_page(request):
    return render(request, "quiz/quiz.html")

# ✅ Custom Logout
def custom_logout(request):
    logout(request)
    request.session.flush()
    return redirect('login')

# ✅ Custom Login View
def custom_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('quiz_list')  
        else:
            return render(request, 'quiz/login.html', {'error': 'Invalid Credentials'})
    return render(request, 'quiz/login.html')



from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

def generate_certificate(request, user_name):
    try:
        # ✅ Path to certificate background (inside static/images/)
        background_path = os.path.join(settings.STATICFILES_DIRS[0], 'images', 'certificate_bg.png')

        if not os.path.exists(background_path):
            return HttpResponse("❌ Error: Certificate background not found!", status=404)

        # ✅ Create response for PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{user_name}_certificate.pdf"'

        # ✅ Set up PDF canvas
        c = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # ✅ Draw background image
        try:
            bg_image = ImageReader(background_path)
            c.drawImage(bg_image, 0, 0, width, height, mask='auto')
        except Exception as e:
            return HttpResponse(f"❌ Error loading image: {str(e)}", status=500)

        # ✅ Add text
        # c.setFont("Helvetica-Bold", 24)
        # c.setFillColorRGB(0.2, 0.2, 0.2)
        # c.drawCentredString(width / 2, height - 200, "🎖️ Certificate of Achievement")

        # c.setFont("Helvetica", 18)
        # c.drawCentredString(width / 2, height - 250, f"{user_name}")

        c.setFont("Helvetica", 22)
        c.drawCentredString(width / 2, height - 430, f"{user_name}")

        # ✅ Save PDF
        c.save()
        return response

    except Exception as e:
        return HttpResponse(f"❌ Unexpected Error: {str(e)}", status=500)
    
    
    #navbar


def about(request):
    return render(request, 'quiz/about.html');

def contact(request):
    return render(request, 'quiz/contact.html');

def gallery(request):
    return render(request, 'quiz/gallery.html');


