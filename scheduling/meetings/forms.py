# -*- coding: utf-8 -*- 
from django import forms
import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES
from django.forms.fields import Field
my_default_errors = {
    'required': '这个格子是必填的',
    'invalid': 'Enter a valid value',
}

def unzipEmails(value):
    if value in EMPTY_VALUES:
        return []
    value = value.replace(',', ';')
    value = [item.strip() for item in value.split(';') if item.strip()]

    return list(set(value))

class CommaSeparatedEmailField(Field):
    description = _(u"E-mail address(es)")

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop("token", ";")
        super(CommaSeparatedEmailField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if value in EMPTY_VALUES:
            return []
        value = value.replace(',', ';')
        value = [item.strip() for item in value.split(self.token) if item.strip()]

        return list(set(value))

    def clean(self, value):
        """
        Check that the field contains one or more 'comma-separated' emails
        and normalizes the data to a list of the email strings.
        """
        value = self.to_python(value)

        if value in EMPTY_VALUES and self.required:
            raise forms.ValidationError(_(u"会议总得有个名称吧"))

        for email in value:
            if not re.match('[a-zA-Z0-9-]{1,}@([a-zA-Z0-9\.])?[a-zA-Z0-9]{1,}\.[a-zA-Z0-9]{1,4}', str(email)):
                raise forms.ValidationError(_(u"'%s' 不是一个有效的邮箱地址，请重新输入！") % email)
        return value

class MtnCreationForm(forms.Form):
    name = forms.CharField(label="会议名称", required = True, max_length = 20, error_messages = my_default_errors,)
    location = forms.CharField(label="会议地点", required = False, max_length = 20, error_messages = my_default_errors,)    
    description = forms.CharField(label="会议描述", required = False, max_length = 100, )
    share = CommaSeparatedEmailField(label="邀请", error_messages = my_default_errors,)