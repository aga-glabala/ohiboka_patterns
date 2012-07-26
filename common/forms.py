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
    subject = forms.CharField(max_length = 100)
    sender = forms.EmailField()
    message = forms.CharField(widget = forms.Textarea)


    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)

        self.fields['subject'].label = _("Subject")
        self.fields['sender'].label = _("Sender")
        self.fields['message'].label = _("Message")
