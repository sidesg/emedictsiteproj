from django.contrib import admin

from .models import *

class DefInline(admin.StackedInline):
    model = LemmaDef
    extra = 0

class SpellingInline(admin.StackedInline):
    model = LemmaSpelling
    extra = 0

class TagInline(admin.StackedInline):
    model = LemmaTag
    extra = 0

class LemmaAdmin(admin.ModelAdmin):
    inlines = [DefInline, SpellingInline, TagInline]

admin.site.register(Lemma, LemmaAdmin)
admin.site.register(Tag)