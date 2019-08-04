import json
import os

from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from bbs import settings
from blog import models
# Create your views here.


def index(request):
    return render(request,'index.html')

@csrf_exempt
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

    return render(request,'upload.html')



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
            try:
                models.UserInfo.objects.create_user(avatar=avatar, **form_obj.cleaned_data)
                ret['msg'] = "/index"
                return JsonResponse(ret)
            except IntegrityError as err:
                ret['status'] = 1
                ret['msg']= {}
                ret['msg']['username'] = ["该账户已注册",]
                print(ret)
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