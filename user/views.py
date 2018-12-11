from django.shortcuts import render
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import redirect

# Create your views here.
def mylogin(request):
    if request.method == 'GET':
        return render(request,'login1.html')
    else:
        #接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('/index/')
        else:
            return redirect(('/user/register'))


def myregister(request):
    if request.method == 'GET':
        return render(request,'register1.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        #检查username是否存在
        try:
            user = BlogUser.objects.get(username=username)
            return render(request,'register1.html',{'error':'用户已存在'})
        except BlogUser.DoesNotExist:
            user = BlogUser.objects.create_user(username,email,password)
        if user:
            return redirect('/user/login/')
        else:
            return render(request,'register1.html',{'error':'用户创建失败'})


def mylogout(request):
    logout(request)
    return redirect('/index/')
