#-*- coding:utf-8 -*-
from django import forms
from models import Comment

class CommentForm(forms.Form):
    pre_comid       = forms.IntegerField(required=False)


    anickname        = forms.CharField(max_length=30,error_messages={'required':u'请填写昵称'})
    bemail           = forms.EmailField(error_messages={'required': u'请填写您的邮箱(不会公开你的邮箱)',
                                                    'invalid': u'邮箱格有误,请重新输入'})
    cwebsite         = forms.URLField(required=False,
                                     error_messages={'invalid': u'博客地址不正确(请以http或https开头)'})
    dcontent         = forms.CharField(widget=forms.Textarea,
                                      error_messages={'required': u'你的评论在哪呢？'})
    mcaptcha         = forms.CharField(max_length=8,required=False,
                                      error_messages={'required': u'请填写验证码',
                                                      'invalid': u'验证码不正确'})