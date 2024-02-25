from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse

from .models import *

class OidInline(admin.StackedInline):
    model = LemmaOid
    extra = 0

class DefInline(admin.StackedInline):
    model = LemmaDef
    extra = 0

class SpellingInline(admin.StackedInline):
    model = Spelling
    extra = 0

class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,  instance._meta.model_name),  args=[instance.pk] )
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''

class FormInline(EditLinkToInlineObject, admin.TabularInline):
    model = Form
    extra=0
    readonly_fields = ('edit_link', )

class TagInline(admin.StackedInline):
    model = LemmaTag
    extra = 0

class CitationInline(admin.StackedInline):
    model = LemmaCitation
    extra = 0

class LemmaAdmin(admin.ModelAdmin):
    inlines = [OidInline, DefInline, FormInline, TagInline, CitationInline]

class FormAdmin(admin.ModelAdmin):
    inlines = [SpellingInline,]

admin.site.register(FormType)
admin.site.register(Form, FormAdmin)
admin.site.register(Lemma, LemmaAdmin)
admin.site.register(Tag)
admin.site.register(TxtSource)
admin.site.register(Pos)
