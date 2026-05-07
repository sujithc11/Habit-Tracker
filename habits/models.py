from django.db import models
from django.contrib.auth.models import User

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    streak = models.IntegerField(default=0)
    last_completed = models.DateField(null=True, blank=True)

    # 🆕 NEW FIELDS
    created_at = models.DateTimeField(auto_now_add=True)
    reminder_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE)
    completed_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.habit.name} - {self.completed_at}"