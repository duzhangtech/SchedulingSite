from django import forms
import re
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.core.validators import EMPTY_VALUES
from django.forms.fields import Field
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
            raise forms.ValidationError(_(u"This field is required."))

        for email in value:
            if not re.match('\b[\w.-]+@[\w.-]+.\w{2,5}\b', email):
                raise forms.ValidationError(_(u"'%s' is not a valid "
                                              "e-mail address.") % email)
        return value

class MtnCreationForm(forms.Form):
	name = forms.CharField(required = True, max_length = 20, help_text = 'Name of the meeting',)
	description = forms.CharField(required = False, max_length = 100, )
	share = CommaSeparatedEmailField()