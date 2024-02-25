from emedictsite.emedict.models import Lemma, LemmaOid

for lemma in Lemma.objects.all():
    newlemoid = LemmaOid(
        lemma = lemma,
        oid = lemma.oid
    )