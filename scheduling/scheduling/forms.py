# -*- coding: utf-8 -*-     
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
my_default_errors = {
    'required': '这个格子是必填的',
    'invalid': '请输入符合要求的值',
}
class MyRegistrationForm(UserCreationForm):
    error_messages = {
        'duplicate_username': ("同样的用户名已经被注册了"),
        'password_mismatch': ("和上次输入的不一样，请重新输入！"),
    }
    # this variable defines a field in the customized form, not a model datafield
    username = forms.RegexField(label = "用户名（其他所有人可见，请使用英文）", required=True, max_length=30,
        regex=r'^[\w.@+-\/\\]+$',
        error_messages=my_default_errors,)
    email = forms.EmailField(label="邮箱（用于登录）" ,required=True, max_length = 75, error_messages = my_default_errors, )
    password1 = forms.CharField(label= "密码", required=True, widget=forms.PasswordInput, error_messages = my_default_errors,)
    password2 = forms.CharField(label= "请再次输入", required=True, widget=forms.PasswordInput, error_messages = my_default_errors,)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("这个邮箱地址已被注册，是否忘记了密码？")
        except User.DoesNotExist:
            return email
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()   
        return user