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
    path('user/<str:username>', UserMinistrantListView.as_view(), name='user-ministrants'),
    path('ministrant/<int:pk>/', MinistrantDetailView.as_view(), name='ministrant-detail'),
    path('ministrant/new/', MinistrantCreateView.as_view(), name='ministrant-create'),
    path('ministrant/<int:pk>/update/', MinistrantUpdateView.as_view(), name='ministrant-update'),
    path('ministrant/<int:pk>/delete/', MinistrantDeleteView.as_view(), name='ministrant-delete'),
    path('about/', views.about, name='blog-about'),
]
