from django import forms


class LemmaSearchForm(forms.Form):
    searched_lemma = forms.CharField(label="Lemma search", max_length=100)