from django.urls import path
from cmuxovik import views

urlpatterns = [
    path("", views.home, name="cmuxovik-home")
]