from django.urls import path
from .views import ExpenseListCreateView, ExpenseDetailView, expense_list_view, expense_create_view

urlpatterns = [
    # API
    path('api/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('api/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),

    # HTML
    path('', expense_list_view, name='expense-list'),
    path('new/', expense_create_view, name='expense-create'),
]
