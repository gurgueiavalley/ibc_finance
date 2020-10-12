from django import forms

class FormExcel(forms.Form):
    arquivo = forms.FileField()
