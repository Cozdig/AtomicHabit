from django.db import models
from config.settings import AUTH_USER_MODEL
from .validators import (
    validate_reward_and_linked_habit,
    validate_linked_habit_is_pleasant,
    validate_pleasant_habit,
    validate_periodicity,
    validate_duration,
)


class Habit(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.TextField()
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
    periodicity = models.PositiveSmallIntegerField(default=1)
    reward = models.CharField(max_length=255, null=True, blank=True)
    duration = models.PositiveSmallIntegerField()
    is_public = models.BooleanField(default=False)

    def clean(self):
        validate_reward_and_linked_habit(self.reward, self.linked_habit)
        validate_linked_habit_is_pleasant(self.linked_habit)
        validate_pleasant_habit(self.reward, self.linked_habit, self.is_pleasant)
        validate_periodicity(self.periodicity)
        validate_duration(self.duration)

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["time"]
