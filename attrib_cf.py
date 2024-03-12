from emedict.models import Lemma, FormType

# assign "Citation Form" FormType to variable via pk

for lem in Lemma.objects.all():
    if lem.form_set.count() > 1:
        pass
    elif lem.form_set.count() == 1:
        cfform = lem.form_set.first()
        cfform.formtype.add()
    else:
        pass