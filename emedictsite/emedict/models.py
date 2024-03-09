from django.db import models
from django.db.models import Q
import re

class TxtSource(models.Model):
    abbr = models.CharField(max_length=200, blank=True)
    title = models.CharField(max_length=1000)
    url = models.URLField(max_length=200, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.title
    
class Pos(models.Model):
    PTYPES = {
        "COM": "Common",
        "PROP": "Proper nouns"
    }
    abbr = models.CharField(max_length=5)
    term = models.CharField(max_length=50)
    type = models.CharField(max_length=5, choices=PTYPES)
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.term

class Tag(models.Model):
    TAGTS = {
        "GR": "Grammar",
        "CO": "Content",
        "SO": "Source",
        "WL": "Word list"
    }
    term = models.CharField(max_length=200)
    type = models.CharField(choices=TAGTS, max_length=200)
    definition = models.TextField(blank=True)
    
    def __str__(self) -> str:
        return self.term

class Lemma(models.Model):
    STATUSES = {
        "NR": "not reviewd",
        "R": "reviewed",
        "RD": "reviewed and documented"
    }

    SORTS = {
        "ŋ": "gz",
        "š": "sz",
        "ř": "rz",
        "ḫ": "hz"
    }

    status = models.CharField(choices=STATUSES, default="NR", max_length=5)
    cf = models.CharField(max_length=200)
    pos = models.ForeignKey(Pos, blank=True, null=True, on_delete=models.SET_NULL)
    notes = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, through="LemmaTag", blank=True)
    components = models.ManyToManyField("self", symmetrical=False, blank=True)
    sortform = models.CharField(max_length=200)

    def make_sortform(self) -> str:
        sortform = self.cf.lower()
        for source, target in self.SORTS.items():
            sortform = re.sub(source, target, sortform)

        return sortform
    
    def update_sortform(self) -> None:
        self.sortform = self.make_sortform()

    def change_h(self):
        newcf = re.sub("h", "ḫ", self.cf)
        newcf = re.sub("H", "Ḫ", newcf)

        self.cf = newcf

    def merge_lem(self, duplicate: "Lemma"):
        for oid in duplicate.lemmaoid_set.filter(
            ~Q(oid__in=self.lemmaoid_set.all())
        ):
            newoid = LemmaOid(
                lemma=self,
                oid=oid
            )
            newoid.save()

        for form in duplicate.form_set.all():
            form.lemma=self
            form.save()

        part_ofs = Lemma.objects.filter(components=duplicate)
        for part_of in part_ofs:
            part_of.components.add(self)
            part_of.components.remove(duplicate)
            part_of.save()
       
        # duplicate.delete()

    def __str__(self) -> str:
        return self.cf

class LemmaOid(models.Model):
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE)
    oid = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return self.oid

class LemmaCitation(models.Model):
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE)
    citation = models.CharField(max_length=1000)
    source = models.ForeignKey(TxtSource, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self) -> str:
        return self.citation

class LemmaDef(models.Model):
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE)
    definition = models.TextField()

    def __str__(self) -> str:
        return self.definition
    
class LemmaTag(models.Model):
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    citation = models.TextField(blank=True)
    tagsource = models.ForeignKey(TxtSource, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return self.lemma.cf + ": " + self.tag.term
    
class FormType(models.Model):
    term = models.CharField(max_length=200)
    definition = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.term

class Form(models.Model):
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE)
    cf = models.CharField(max_length=200, blank=True)
    formtype = models.ManyToManyField(FormType, blank=True)
    
    def __str__(self) -> str:
        return self.cf

class Spelling(models.Model):
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    spelling_lat = models.CharField(max_length=200)
    spelling_cun = models.CharField(max_length=200, blank=True)

    def __str__(self) -> str:
        return self.spelling_lat