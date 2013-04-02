'''
Created on Mar 16, 2012

@author: agnis
'''
from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()
