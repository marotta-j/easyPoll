from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("<slug:slug>", views.poll_view, name='poll_view'),
    path("<slug:slug>/results", views.results_view),
    path('vote/', views.vote)
]