from django.db import models

class Lemma(models.Model):
    POS = {
        "V": "Verb",
        "N": "Noun",
        "ADJ": "Adjective",
        "CNJ": "Conjunction",
        "QP": "Question Particle",
        "O": "Other"
    }

    oid = models.IntegerField(default=None)
    cf = models.CharField(max_length=200)
    pos = models.CharField(choices=POS, max_length=200)
    notes = models.TextField(default="")

    def __str__(self) -> str:
        return self.cf

class LemmaDef(models.Model):
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE)
    definition = models.TextField()

    def __str__(self) -> str:
        return self.definition

class LemmaSpelling(models.Model):
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE)
    spelling_lat = models.CharField(max_length=200)
    spelling_cun = models.CharField(max_length=200, default="")

    def __str__(self) -> str:
        return self.spelling_lat

class Tag(models.Model):
    term = models.TextField()
    
    def __str__(self) -> str:
        return self.term

class LemmaTag(models.Model):
    lemma = models.ForeignKey(Lemma, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    citation = models.TextField()

    def __str__(self) -> str:
        return self.lemma.cf + ": " + self.tag.term