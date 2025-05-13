from django.urls import path
from .views import ExportPDFView, ExportExcelView

urlpatterns = [
    path('pdf/', ExportPDFView.as_view(), name='export-pdf'),
    path('excel/', ExportExcelView.as_view(), name='export-excel'),
]
