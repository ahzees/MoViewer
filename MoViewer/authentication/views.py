from django.shortcuts import render, redirect
from authentication.forms import RegisterForm, LoginForm, ChangeUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import Http404
from authentication.models import CustomUser

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from authentication.serializers import UserSerializer


# Create your views here.

class CustomUserApiView(APIView):
    serializer_class = UserSerializer()

    def get(self, request):
        return Response(UserSerializer(CustomUser.objects.all(), many=True).data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TheCustomUserApiView(APIView):
    serializer_class = UserSerializer()

    def get_user(self,pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except:
            raise Http404

    def get(self,request,pk):
        user = self.get_user(pk=pk)
        return Response(UserSerializer(user).data,status=status.HTTP_200_OK)

def login_(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            return render(request, 'authentication/login.html')
        return render(request, 'authentication/login.html')
    else:
        return redirect('home')


def register(request):
    if not request.user.is_authenticated:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Account created')
                return redirect('home')
            else:
                return redirect('register')
        if request.method == 'GET':
            return render(request, 'authentication/register.html', {'form': form})
    else:
        return redirect('home')


def logout_(request):
    logout(request)
    return redirect('home')


def my_profile(request):
    return render(request, 'authentication/my_profile.html')


def change_profile(request):
    form = ChangeUserForm(request.POST, request.FILES or None)
    if request.method == 'POST':
        form.is_valid()
        user = CustomUser.objects.get(pk=request.user.pk)
        for i, y in form.cleaned_data.items():
            if y:
                user.__dict__[i] = y
        print(user.image)
        user.save()
        return render(request, 'authentication/change_profile.html', {'form': form})
    return render(request, 'authentication/change_profile.html', {'form': form})
