from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext as _

class UserCreationFormExtended(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserCreationFormExtended, self).__init__(*args, **kwargs)
        self.fields['email'].required = True

    class Meta:
        model = User
        fields = ('username', 'email')

class ContactForm(forms.Form):
    subject = forms.CharField(label = _("Subject"), max_length = 100, required = True)
    sender = forms.EmailField(label = _("Sender"), required = True)
    message = forms.CharField(label = _("Message"), widget = forms.Textarea, required = True)
