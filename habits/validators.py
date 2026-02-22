from django.core.exceptions import ValidationError


def validate_reward_and_linked_habit(reward, linked_habit):
    if reward and linked_habit:
        raise ValidationError("Нельзя указать и вознаграждение, и связанную привычку")


def validate_linked_habit_is_pleasant(linked_habit):
    if linked_habit and not linked_habit.is_pleasant:
        raise ValidationError("Связанная привычка должна быть приятной")


def validate_pleasant_habit(reward, linked_habit, is_pleasant):
    if is_pleasant and (reward or linked_habit):
        raise ValidationError("У приятной привычки не может быть вознаграждения или связанной привычки")


def validate_periodicity(periodicity):
    if periodicity < 1 or periodicity > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней")


def validate_duration(duration):
    if duration > 120:
        raise ValidationError("Время выполнения не может превышать 120 секунд")
