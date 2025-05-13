from django.urls import path
from .views import IncomeListCreateView, IncomeDetailView, income_list_view, income_create_view

urlpatterns = [
    # API endpointlar
    path('api/', IncomeListCreateView.as_view(), name='income-list-create'),
    path('api/<int:pk>/', IncomeDetailView.as_view(), name='income-detail'),

    # HTML viewlar
    path('', income_list_view, name='income-list'),
    path('new/', income_create_view, name='income-create'),
]
