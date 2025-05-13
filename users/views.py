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

from .models import EmailVerification
from .utils import generate_verification_code, send_verification_email
from .forms import VerifyForm


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
        email = request.POST['email']

        existing = EmailVerification.objects.filter(email=email, is_verified=False).first()
        code = generate_verification_code()

        if existing:
            existing.code = code
            existing.save()
        else:
            EmailVerification.objects.create(email=email, code=code)

        send_verification_email(email, code)

        request.session['pending_email'] = email
        return redirect('verify-email')

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
            update_session_auth_hash(request, user)  # Logout bo‘lib qolmasligi uchun

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


def verify_email_view(request):
    email = request.session.get('pending_email')

    if request.method == 'POST':
        form = VerifyForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                record = EmailVerification.objects.get(email=email, code=cd['code'], is_verified=False)
                record.is_verified = True
                record.save()

                user = CustomUser.objects.create_user(
                    email=email,
                    password=cd['password'],
                    first_name=cd['first_name'],
                    last_name=cd['last_name'],
                    phone_number=cd['phone_number'],
                    card_number=cd['card_number']
                )

                login(request, user)
                return redirect('home')

            except EmailVerification.DoesNotExist:
                messages.error(request, "❌ Kod noto‘g‘ri yoki eskirgan!")
    else:
        form = VerifyForm()

    return render(request, 'verify.html', {'form': form})
