from django.db import models
from django.conf import settings


class WellnessGoal(models.Model):
    GOAL_TYPE_CHOICES = [
        ('steps', 'Steps'),
        ('active_time', 'Active Time'),
        ('sleep', 'Sleep'),
        ('water', 'Water Intake'),
        ('calories', 'Calories'),
        ('custom', 'Custom'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wellness_goals')
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPE_CHOICES)
    title = models.CharField(max_length=100)
    target_value = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=20, default='')  # steps, minutes, hours, ml, kcal
    date = models.DateField()
    is_completed = models.BooleanField(default=False)
    
    # Additional data for specific goal types
    extra_data = models.JSONField(blank=True, null=True)  # e.g., sleep start/end time, distance
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', 'goal_type']
        unique_together = ['user', 'goal_type', 'date']
    
    def __str__(self):
        return f"{self.user.email} - {self.title} - {self.date}"
    
    @property
    def progress_percentage(self):
        if self.target_value == 0:
            return 0
        return min(100, int((self.current_value / self.target_value) * 100))
    
    def save(self, *args, **kwargs):
        if self.current_value >= self.target_value:
            self.is_completed = True
        super().save(*args, **kwargs)


class DailyGoalLog(models.Model):
    """Log individual entries for goals throughout the day"""
    goal = models.ForeignKey(WellnessGoal, on_delete=models.CASCADE, related_name='logs')
    value = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True, null=True)
    logged_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-logged_at']
    
    def __str__(self):
        return f"{self.goal.title} - {self.value} at {self.logged_at}"


class PreventiveCareReminder(models.Model):
    REMINDER_TYPE_CHOICES = [
        ('blood_test', 'Blood Test'),
        ('vaccination', 'Vaccination'),
        ('checkup', 'General Checkup'),
        ('screening', 'Health Screening'),
        ('dental', 'Dental Checkup'),
        ('eye_exam', 'Eye Examination'),
        ('custom', 'Custom'),
    ]
    
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('missed', 'Missed'),
        ('rescheduled', 'Rescheduled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    scheduled_date = models.DateField()
    scheduled_time = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    location = models.CharField(max_length=200, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    # For recurring reminders
    is_recurring = models.BooleanField(default=False)
    recurrence_interval = models.PositiveIntegerField(blank=True, null=True, help_text="Days between reminders")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['scheduled_date', 'scheduled_time']
    
    def __str__(self):
        return f"{self.user.email} - {self.title} - {self.scheduled_date}"


class HealthTip(models.Model):
    CATEGORY_CHOICES = [
        ('nutrition', 'Nutrition'),
        ('exercise', 'Exercise'),
        ('sleep', 'Sleep'),
        ('mental_health', 'Mental Health'),
        ('hydration', 'Hydration'),
        ('general', 'General'),
    ]
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    is_active = models.BooleanField(default=True)
    display_date = models.DateField(blank=True, null=True)  # Specific date to show this tip
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-display_date', '-created_at']
    
    def __str__(self):
        return self.title
