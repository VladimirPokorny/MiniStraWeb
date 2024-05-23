from django.urls import path
from . import views

from .views import (
    MinistrantListView,
    MinistrantDetailView,
    MinistrantCreateView,
    MinistrantUpdateView,
    MinistrantDeleteView,
    UserMinistrantListView,
    AllMinistrantListView,
    MinistrantInvoiceView,
    MinistrantPrintOutView,

)
from utils.printout_form_generator import PrintOutFormGenerator



from . import views


urlpatterns = [
    path('', MinistrantListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserMinistrantListView.as_view(), name='user-ministrants'),
    path('ministrant/<int:pk>/', MinistrantDetailView.ministrant_detail, name='ministrant-detail'),
    path('ministrant/new/', MinistrantCreateView.as_view(), name='ministrant-create'),
    path('ministrant/<int:pk>/update/', MinistrantUpdateView.as_view(), name='ministrant-update'),
    path('ministrant/<int:pk>/delete/', MinistrantDeleteView.as_view(), name='ministrant-delete'),
    path('ministrant/all/', AllMinistrantListView.as_view(), name='all-ministrants'),
    path('ministrant/pdf/<int:pk>/printout', MinistrantPrintOutView.generate_printout_form, name='ministrant-pdf-generate'),
    path('ministrant/pdf/<int:pk>/invoice', MinistrantInvoiceView.generate_invoice, name='ministrant-invoice-pdf'),
    path('about/', views.about, name='blog-about'),
]
