from django.urls import path
from .views import BalanceStatsView, ChartDataView

urlpatterns = [
    path('balance/', BalanceStatsView.as_view(), name='balance-stats'),
    path('charts/', ChartDataView.as_view(), name='chart-data'),

]
