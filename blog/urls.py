from django.urls import path
from .views import (
    MinistrantListView,
    MinistrantDetailView,
    MinistrantCreateView,
    MinistrantUpdateView,
    MinistrantDeleteView,
    UserMinistrantListView
)
from . import views

urlpatterns = [
    path('', MinistrantListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserMinistrantListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', MinistrantDetailView.as_view(), name='post-detail'),
    path('post/new/', MinistrantCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', MinistrantUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', MinistrantDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]
