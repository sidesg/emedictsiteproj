from django import forms

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
        widget=forms.RadioSelect,
        choices=LETTERS
    )
    
