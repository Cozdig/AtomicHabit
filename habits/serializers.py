from rest_framework import serializers
from .models import Habit
from django.core.exceptions import ValidationError
from .validators import (
    validate_reward_and_linked_habit,
    validate_linked_habit_is_pleasant,
    validate_pleasant_habit,
    validate_periodicity,
    validate_duration,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ["id", "user"]

    def validate(self, data):
        try:
            validate_reward_and_linked_habit(data.get("reward"), data.get("linked_habit"))
            validate_linked_habit_is_pleasant(data.get("linked_habit"))
            validate_pleasant_habit(data.get("reward"), data.get("linked_habit"), data.get("is_pleasant", False))
            validate_periodicity(data.get("periodicity", 1))
            validate_duration(data.get("duration", 0))
        except ValidationError as e:
            raise serializers.ValidationError({"non_field_errors": e.messages})

        return data


class PublicHabitSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Habit
        fields = ["id", "user_username", "place", "time", "action", "is_pleasant", "periodicity", "duration"]
