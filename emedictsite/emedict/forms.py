from django import forms

class AddDefinition(forms.Form):
    definition = forms.CharField(label="Definition", max_length=1000)
