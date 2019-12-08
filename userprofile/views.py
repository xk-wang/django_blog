from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm, ProfileForm
from .models import Profile

# Create your views here.
def user_login(request):
    if request.method == 'POST':
        user_login_form=UserLoginForm(request.POST)
        if user_login_form.is_valid():
            data=user_login_form.cleaned_data
            user=authenticate(username=data['username'],password=data['password'])
            if user:
                login(request,user)
                return redirect('blog:post_list')
            else:
                return HttpResponse('用户名或密码有误')
        else:
            return HttpResponse('账号或密码输入不合法')
    elif request.method == 'GET':
        user_login_form=UserLoginForm()
        return render(request,'userprofile/login.html',context={'form':user_login_form})
    else:
        return HttpResponse('请使用POST或者GET请求数据')
def user_logout(request):
    logout(request)
    return redirect('blog:post_list')
def user_register(request):
    if request.method=='POST':
        user_register_form=UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            new_user=user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request, new_user)
            return redirect('blog:post_list')
        else:
            return HttpResponse('注册表单有误')
    elif request.method=='GET':
        user_register_form = UserRegisterForm()
        return render(request, 'userprofile/register.html',context={'form':user_register_form})
    else:
        return HttpResponse('请使用GET或POST请求数据')

@login_required(login_url='/userprofile/login/')
def user_delete(request, id):
    if request.method=='POST':
        user=User.objects.get(id=id)
        if request.user == user:
            logout(request)
            user.delete()
            redirect('blog:post_list')
        else:
            return HttpResponse('您没有权限删除')
    else:
        return HttpResponse('仅接受POST请求')
@login_required(login_url='/userprofile/login/')
def profile_edit(request, id):
    user=User.objects.get(id=id)
    if Profile.objects.filter(user_id=id).exists():
        profile=Profile.objects.get(user_id=id)
    else:
        profile=Profile.objects.create(user=user)

    if request.method=='POST':
        if request.user!=user:
            return HttpResponse('你没有权限修改此用户信息')
        profile_form=ProfileForm(request.POST, request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar=profile_cd['avatar']
            profile.save()
            return redirect('userprofile:edit', id =id)
        else:
            return HttpResponse('注册表单输入有误，请重新输入')
    elif request.method == 'GET':
        profile_form = ProfileForm()
        return render(request, 'userprofile/edit.html', context=
            {'profile_form':profile_form, 'profile':profile, 'user':user})
    else:
        return HttpResponse('请使用GET或POST请求数据')
