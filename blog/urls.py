from django.urls import path
from .views import (
    MinistrantListView,
    MinistrantDetailView,
    MinistrantCreateView,
    MinistrantUpdateView,
    MinistrantDeleteView,
    UserMinistrantListView,
    AllMinistrantListView,
    generate_pdf
)
from . import views

urlpatterns = [
    path('', MinistrantListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserMinistrantListView.as_view(), name='user-ministrants'),
    path('ministrant/<int:pk>/', MinistrantDetailView.ministrant_detail, name='ministrant-detail'),
    path('ministrant/new/', MinistrantCreateView.as_view(), name='ministrant-create'),
    path('ministrant/<int:pk>/update/', MinistrantUpdateView.as_view(), name='ministrant-update'),
    path('ministrant/<int:pk>/delete/', MinistrantDeleteView.as_view(), name='ministrant-delete'),
    path('ministrant/all/', AllMinistrantListView.as_view(), name='all-ministrants'),
    path('ministrant/<int:pk>/pdf/', generate_pdf, name='ministrant-pdf-generate'),
    path('about/', views.about, name='blog-about'),
]
