#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/7/13 7:59
# @Author   :   robert
# @FileName :   forms.py
# @Software :   PyCharm

from django import forms

# 定义一个注册的form类
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class RegistryForm(forms.Form):

    username = forms.CharField(
        label="用户名",
        max_length=16,
        min_length=6,
        widget= forms.widgets.TextInput(
            attrs={
                "class" : "form-control"
            }
        ),
        required=True,
        error_messages= {
            'max_length': "账号长度超过限制",
            # 'm_length': "账号长度不能低于6位",
            'required': "账号不能位空"
        }
    )
    password = forms.CharField(
        label="密码",
        min_length=6,
        max_length=16,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control"
            }
        ),
        required=True,
        # 定义密码必须要包含大小写，数字和字母组合
        validators= [
            RegexValidator(r'[A-Z]+',"密码必须包含大小写字母，数字"),
            RegexValidator(r'[0-9]+',"密码必须包含大小写字母，数字"),
            RegexValidator(r'[a-z]+',"密码必须包含大小写字母，数字"),
        ],
        error_messages={
            'min_length': "密码不能低于6位",
            'max_length': "密码最多16位",
            'required': "密码不能位空"
        }
    )

    verify_password = forms.CharField(
        label="确认密码",
        required=True,
        widget=forms.widgets.PasswordInput(
            attrs={
                "class" : "form-control"
            }
        ),

        error_messages= {
            'required': "请输入确认密码",
        }
    )


    def clean(self):
        password = self.cleaned_data.get('password'),
        verify_password = self.cleaned_data.get('verify_password'),
        if password != verify_password:
            self.add_error('verify_password',ValidationError("两次的密码输入不一致"))
        return self.cleaned_data


    email = forms.EmailField(
        label = "邮箱",
        widget = forms.widgets.EmailInput(
            attrs={
                "class" : "form-control"
            }
        ),
        error_messages= {
            "invalid": "邮箱格式不正确",
            "required": "邮箱没有填写",
        }
    )
