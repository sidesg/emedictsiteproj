from django.contrib import admin

from .models import *

class OidInline(admin.StackedInline):
    model = LemmaOid
    extra = 0

class DefInline(admin.StackedInline):
    model = LemmaDef
    extra = 0

class SpellingInline(admin.StackedInline):
    model = LemmaSpelling
    extra = 0

class TagInline(admin.StackedInline):
    model = LemmaTag
    extra = 0

class CitationInline(admin.StackedInline):
    model = LemmaCitation
    extra = 0

class LemmaAdmin(admin.ModelAdmin):
    inlines = [OidInline, DefInline, SpellingInline, TagInline, CitationInline]

admin.site.register(Lemma, LemmaAdmin)
admin.site.register(Tag)
admin.site.register(TxtSource)
admin.site.register(Pos)