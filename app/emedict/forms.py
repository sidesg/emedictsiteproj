from django import forms
from .models import Pos, Tag

class LemmaSearchForm(forms.Form):
    lemma = forms.CharField(label="Lemma search", max_length=100)

class LemmaInitialLetterForm(forms.Form):
    LETTERS = [
        ("A", "A"), 
        ("B", "B"), 
        ("D", "D"), 
        ("E", "E"), 
        ("G", "G"), 
        ("Ŋ", "Ŋ"), 
        ("H", "H"), 
        ("Ḫ", "Ḫ"), 
        ("I", "I"), 
        ("K", "K"),
        ("L", "L"), 
        ("M", "M"), 
        ("N", "N"), 
        ("P", "P"), 
        ("R", "R"), 
        ("Ř", "Ř"), 
        ("S", "S"), 
        ("Š", "Š"), 
        ("T", "T"), 
        ("U", "U"), 
        ("Z", "Z")] 
    initial = forms.ChoiceField(
        widget=forms.RadioSelect(
            attrs={"class": "lem_init"}
        ),
        choices=LETTERS
    )

class FacetSideBarForm(forms.Form):
    poss = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Parts of speech', 
        choices=list()
    )
    tags = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label='Tags', 
        choices=list()
    )

    def __init__(self, poss=None, tag_list=None, *args, **kwargs):
        super(FacetSideBarForm, self).__init__(*args, **kwargs)
        if poss:
            self.fields['poss'].choices = [
                (pos, pos)
                for pos in poss
            ]
        if tag_list:
            self.fields['tags'].choices = [
                (tag, tag)
                for tag in tag_list
            ]