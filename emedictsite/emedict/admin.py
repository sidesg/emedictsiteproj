from django.contrib import admin

from .models import *

admin.site.register(Lemma)
admin.site.register(LemmaDef)
admin.site.register(LemmaSpelling)
admin.site.register(LemmaGTag)
admin.site.register(LemmaCTag)
admin.site.register(GrammarTag)
admin.site.register(ContentTag)
