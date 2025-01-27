from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path('vote/', views.vote),
    path("<slug:slug>/", views.poll_view, name='poll_view'),
    path("<slug:slug>/results/", views.results_view)
]