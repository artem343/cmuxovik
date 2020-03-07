from django.urls import path
from cmuxovik import views
from .views import (
    CmuxListView, 
    CmuxDetailView, 
    CmuxCreateView, 
    CmuxUpdateView,
    CmuxDeleteView
)

urlpatterns = [
    path("", CmuxListView.as_view(), name="cmuxovik-home"),
    path("cmux/<int:pk>/", CmuxDetailView.as_view(), name="cmux-detail"),
    path("cmux/new/", CmuxCreateView.as_view(), name="cmux-create"),
    path("cmux/<int:pk>/update/", CmuxUpdateView.as_view(), name="cmux-update"),
    path("cmux/<int:pk>/delete/", CmuxDeleteView.as_view(), name="cmux-delete"),
]