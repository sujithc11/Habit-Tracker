from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Habit, HabitLog


@login_required
def dashboard(request):
    habits = Habit.objects.filter(user=request.user)

    # 📊 Chart (last 7 days)
    labels = []
    data = []

    for i in range(6, -1, -1):
        day = date.today() - timedelta(days=i)
        labels.append(day.strftime("%a"))

        count = HabitLog.objects.filter(
            habit__user=request.user,
            completed_at=day
            ).count()

        data.append(count)
    print(labels)
    print(data)

    # 📅 Calendar (last 30 days)
    calendar = []

    for i in range(29, -1, -1):
        day = date.today() - timedelta(days=i)

        completed = Habit.objects.filter(
            user=request.user,
            last_completed=day
        ).exists()

        calendar.append({
            "day": day,
            "completed": completed
        })

    return render(request, "dashboard.html", {
        "habits": habits,
        "labels": labels,
        "data": data,
        "calendar": calendar
    })

@login_required
def add_habit(request):
    if request.method == "POST":
        name = request.POST.get("name")
        Habit.objects.create(name=name, user=request.user)
        return redirect('/')

    return render(request, "add.html")


from datetime import date, timedelta

@login_required
def complete_habit(request, id):

    habit = Habit.objects.get(id=id, user=request.user)

    today = date.today()

    # prevent multiple completions same day
    already_completed = HabitLog.objects.filter(
        habit=habit,
        completed_at=today
    ).exists()

    if already_completed:
        return redirect('/')

    # streak logic
    if habit.last_completed == today - timedelta(days=1):
        habit.streak += 1
    else:
        habit.streak = 1

    # update last completed
    habit.last_completed = today
    habit.save()

    # save completion history
    HabitLog.objects.create(
        habit=habit
    )

    return redirect('/')

from django.contrib.auth.models import User
from django.contrib.auth import login

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('/')

    return render(request, "signup.html")

@login_required
def delete_habit(request, id):
    habit = Habit.objects.get(id=id, user=request.user)
    habit.delete()
    return redirect('/')



