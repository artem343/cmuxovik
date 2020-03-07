from django.urls import path
from cmuxovik import views
from .views import (
    CmuxListView, 
    CmuxDetailView, 
    CmuxCreateView, 
    CmuxUpdateView,
    CmuxDeleteView,
    UserCmuxListView
)

urlpatterns = [
    path("", CmuxListView.as_view(), name="cmuxovik-home"),
    path("user/<str:username>/", UserCmuxListView.as_view(), name="user-posts"),
    path("cmux/<int:pk>/", CmuxDetailView.as_view(), name="cmux-detail"),
    path("cmux/new/", CmuxCreateView.as_view(), name="cmux-create"),
    path("cmux/<int:pk>/update/", CmuxUpdateView.as_view(), name="cmux-update"),
    path("cmux/<int:pk>/delete/", CmuxDeleteView.as_view(), name="cmux-delete"),
]