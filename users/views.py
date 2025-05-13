from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, LoginSerializer

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .models import CustomUser, FamilyGroup
from django.contrib.auth.decorators import login_required


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def signup_view(request):
    if request.method == 'POST':
        data = request.POST
        user = CustomUser.objects.create_user(
            email=data['email'],
            phone_number=data['phone_number'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            card_number=data['card_number'],
            password=data['password'],
        )
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email yoki parol noto‘g‘ri.')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.phone_number = request.POST.get('phone_number')
        user.card_number = request.POST.get('card_number')

        if 'profile_photo' in request.FILES:
            user.profile_photo = request.FILES['profile_photo']

        if request.POST.get('password'):
            user.set_password(request.POST['password'])
            update_session_auth_hash(request, user)  

        user.save()
        return redirect('profile')

    return render(request, 'account.html', {'user': user})

@login_required
def family_group_view(request):
    user = request.user
    if request.method == 'POST':
        group_name = request.POST['group_name']
        group = FamilyGroup.objects.create(name=group_name)
        user.family_group = group
        user.role_in_family = 'admin'
        user.save()
        return redirect('family')

    family_members = CustomUser.objects.filter(family_group=user.family_group) if user.family_group else []
    return render(request, 'family.html', {'user': user, 'members': family_members})
