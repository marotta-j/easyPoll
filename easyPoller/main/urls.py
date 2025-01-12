from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("<int:id>", views.poll_view, name='poll_view'),
    path("<int:id>/results", views.results_view),
    path('vote/', views.vote)
]