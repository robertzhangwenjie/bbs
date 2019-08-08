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


# 获取验证码图片
def get_valid_img(request):
    from PIL import Image, ImageDraw, ImageFont
    import random

    # 获取随机颜色
    def get_randow_color():
        return random.randint(0,255), random.randint(0,255), random.randint(0,255)

    # 生成一个图片对象
    img_obj = Image.new('RGB',(200, 35), get_randow_color())
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件，得到一个字体对象
    font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  #生成大写字母
        l = chr(random.randint(97, 122)) # 生成小写字母
        n = str(random.randint(0, 9)) # 生成数字， 注意要转换成字符串

        tmp = random.choice([u, l,  n])
        tmp_list.append(tmp)
        draw_obj.text((20+40*i, 0), tmp, fill=get_randow_color(), font=font_obj)

    print("".join(tmp_list))

    # 保存验证码到session中
    request.session['validate_code'] = "".join(tmp_list)

    # 将生成的图片数据保存在内存中
    from io import BytesIO
    io_obj = BytesIO()
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)


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
        print(request.POST)
        # 判断验证码是否输入正确
        if validate_code and validate_code.upper() != request.session.get("validate_code","").upper():
            ret["status"] = 1
            ret['msg'] = "验证码不正确"
            return JsonResponse(ret, json_dumps_params={'ensure_ascii': False})
        if username and password:
            # 判断用户名和密码是否正确
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                # 如果登录成功，将登录的用户信息封装到request中
                auth.login(request, user)
                ret['msg'] = "/login"
            else:
                ret['status'] = 1
                ret['msg'] = "用户名和密码不正确"
        else:
            ret["status"] = 1
            ret['msg'] = "用户名和密码不能为空"
        return JsonResponse(ret, json_dumps_params={'ensure_ascii': False})
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
        print(request.POST)
        form_obj = forms.RegistryForm(request.POST)
        avatar = request.FILES.get('avatar',"avatars/default.png")
        # form表单对象帮助校验
        if form_obj.is_valid():
            # 校验通过，去数据库创建一个新用户
            form_obj.cleaned_data.pop("verify_password")
            models.UserInfo.objects.create_user(**form_obj.cleaned_data, avatar=avatar)
            ret['msg'] = "/login"
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