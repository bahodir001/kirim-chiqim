from rest_framework import generics, permissions
from .models import Expense
from .serializers import ExpenseSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

class ExpenseListCreateView(generics.ListCreateAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.family_group:
            return Expense.objects.filter(user__family_group=user.family_group)
        return Expense.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.family_group:
            return Expense.objects.filter(user__family_group=user.family_group)
        return Expense.objects.filter(user=user)


@login_required
def expense_list_view(request):
    user = request.user
    if user.family_group:
        expenses = Expense.objects.filter(user__family_group=user.family_group)
    else:
        expenses = Expense.objects.filter(user=user)
    return render(request, 'expense_list.html', {'expenses': expenses})


@login_required
def expense_create_view(request):
    if request.method == 'POST':
        data = request.POST
        Expense.objects.create(
            user=request.user,
            expense_type=data['expense_type'],
            amount=data['amount'],
            date=data['date'],
            time=data['time'],
            method=data['method']
        )
        return redirect('expense-list')
    return render(request, 'expense_form.html')
