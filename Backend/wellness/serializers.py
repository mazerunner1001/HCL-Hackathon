from rest_framework import serializers
from .models import WellnessGoal, DailyGoalLog, PreventiveCareReminder, HealthTip


class DailyGoalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyGoalLog
        fields = ['id', 'value', 'notes', 'logged_at']
        read_only_fields = ['id', 'logged_at']


class WellnessGoalSerializer(serializers.ModelSerializer):
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = WellnessGoal
        fields = [
            'id', 'goal_type', 'title', 'target_value', 'current_value',
            'unit', 'date', 'is_completed', 'progress_percentage',
            'extra_data', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'is_completed', 'created_at', 'updated_at']
    
    def get_progress_percentage(self, obj):
        if obj.target_value == 0:
            return 0
        try:
            return min(100, int((float(obj.current_value) / float(obj.target_value)) * 100))
        except:
            return 0


class WellnessGoalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = WellnessGoal
        fields = ['goal_type', 'title', 'target_value', 'unit', 'date', 'extra_data']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class LogGoalProgressSerializer(serializers.Serializer):
    value = serializers.DecimalField(max_digits=10, decimal_places=2)
    notes = serializers.CharField(required=False, allow_blank=True)


class PreventiveCareReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreventiveCareReminder
        fields = [
            'id', 'reminder_type', 'title', 'description', 'scheduled_date',
            'scheduled_time', 'status', 'location', 'notes', 'is_recurring',
            'recurrence_interval', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class HealthTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthTip
        fields = ['id', 'title', 'content', 'category', 'display_date', 'created_at']
        read_only_fields = ['id', 'created_at']

