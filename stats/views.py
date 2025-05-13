from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
from income.models import Income
from expenses.models import Expense
from collections import defaultdict


class BalanceStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        today = datetime.today().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        def calculate_sum(queryset):
            return sum([item.amount for item in queryset])

        data = {
            "today": {
                "income": calculate_sum(Income.objects.filter(user=user, date=today)),
                "expense": calculate_sum(Expense.objects.filter(user=user, date=today)),
            },
            "week": {
                "income": calculate_sum(Income.objects.filter(user=user, date__gte=week_ago)),
                "expense": calculate_sum(Expense.objects.filter(user=user, date__gte=week_ago)),
            },
            "month": {
                "income": calculate_sum(Income.objects.filter(user=user, date__gte=month_ago)),
                "expense": calculate_sum(Expense.objects.filter(user=user, date__gte=month_ago)),
            },
            "total": {
                "income": calculate_sum(Income.objects.filter(user=user)),
                "expense": calculate_sum(Expense.objects.filter(user=user)),
            }
        }

        data["balance"] = data["total"]["income"] - data["total"]["expense"]

        return Response(data)


class ChartDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        income_data = defaultdict(float)
        for i in Income.objects.filter(user=user):
            income_data[i.income_type] += float(i.amount)

        expense_data = defaultdict(float)
        for e in Expense.objects.filter(user=user):
            expense_data[e.expense_type] += float(e.amount)

        return Response({
            'income': income_data,
            'expense': expense_data
        })