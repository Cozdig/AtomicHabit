from django.urls import path
from . import views

app_name = "habits"

urlpatterns = [
    path("", views.HabitListCreateView.as_view()),
    path("public/", views.PublicHabitListView.as_view()),
    path("<int:pk>/", views.HabitRetrieveUpdateDestroyView.as_view()),
]
