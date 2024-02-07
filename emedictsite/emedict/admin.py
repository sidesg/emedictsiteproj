from django.contrib import admin

from .models import *

admin.site.register(Lemma)
admin.site.register(LemmaDef)
admin.site.register(Tag)
admin.site.register(LemmaTag)
admin.site.register(LemmaSpelling)