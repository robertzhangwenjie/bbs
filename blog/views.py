import os

from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from bbs import settings
from blog import models
# Create your views here.


def index(request):
    return render(request,'index.html')

@login_required
def upload(request):
    if request.method == "POST":
        upload_file = request.FILES.get('filename')
        local_file = os.path.join(settings.UPLOAD_DIR,upload_file.name)
        for chunk in upload_file.chunks():
            with open(local_file,'wb') as f:
                f.write(chunk)
        return HttpResponse("上传成功")
    return render(request,'upload.html')


def login(request):
    if request.method == "POST":
        # 初始化返回对象
        ret = {
            "status": 0,
            "msg": ""
        }
        username = request.POST.get("username")
        password = request.POST.get("password")
        validate_code = request.POST.get("validate_code")
        if username and password:
            # 判断用户名和密码是否正确
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                # 如果登录成功，将登录的用户信息封装到request中
                auth.login(request, user)
                return redirect(index)
            return HttpResponse("用户名和密码不正确")
        else:
            return HttpResponse("用户名和密码不能为空")
    return render(request, "login.html")


def logout(request):
    # 清空浏览器和数据库中的session
    auth.logout(request)

    return redirect(login)


from blog import forms
def registry(request):
    if request.method == "POST":
        ret = {
            'status': 0,
            'msg': ""
        }
        form_obj = forms.RegistryForm(request.POST)
        avatar = request.FILES.get('avatar')
        # form表单对象帮助校验
        if form_obj.is_valid():
            # 校验通过，去数据库创建一个新用户
            form_obj.cleaned_data.pop("verify_password")
            print(request.POST)
            models.UserInfo.objects.create_user(avatar=avatar, **form_obj.cleaned_data)
            ret['msg'] = "/index"
            return JsonResponse(ret)
        else:
            print(form_obj.errors)
            # return render(request,'registry.html',{'form_obj':form_obj})
            # ajax请求时返回
            ret['status'] = 1
            # 如果有错误，则把错误列表返回
            ret['msg'] = form_obj.errors
            return JsonResponse(ret, json_dumps_params={'ensure_ascii':False})
    # 生成一个form对象
    form_obj = forms.RegistryForm()
    return render(request,'registry.html',{'form_obj':form_obj})