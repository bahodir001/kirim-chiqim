from rest_framework import generics, permissions
from .models import Income
from .serializers import IncomeSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

class IncomeListCreateView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.family_group:
            return Income.objects.filter(user__family_group=user.family_group)
        return Income.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.family_group:
            return Income.objects.filter(user__family_group=user.family_group)
        return Income.objects.filter(user=user)


@login_required
def income_list_view(request):
    user = request.user
    if user.family_group:
        incomes = Income.objects.filter(user__family_group=user.family_group)
    else:
        incomes = Income.objects.filter(user=user)
    return render(request, 'income_list.html', {'incomes': incomes})


@login_required
def income_create_view(request):
    if request.method == 'POST':
        data = request.POST
        Income.objects.create(
            user=request.user,
            income_type=data['income_type'],
            amount=data['amount'],
            date=data['date'],
            time=data['time'],
            method=data['method']
        )
        return redirect('income-list')
    return render(request, 'income_form.html')
