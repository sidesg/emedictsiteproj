from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.db.models import Q

from .models import Lemma, Tag

LETTERS = ["A", "B", "D", "E", "G", "Ŋ", "H", "Ḫ", "I", "K",
            "L", "M", "N", "P", "R", "Ř", "S", "Š", "T", "U", "Z"]

class TagIdView(generic.DetailView):
    model = Tag
    template_name = "emedict/tags_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lemmata"] = Lemma.objects.filter(tags__id=self.kwargs['pk']).order_by("sortform")

        return context

class LemmaListView(generic.ListView): 
    model = Lemma
    context_object_name = "lemmalist"
    template_name = "emedict/lemma_home.html"
    queryset = Lemma.objects.filter(cf__startswith="a", pos__type="COM").order_by("sortform")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["letters"] = LETTERS

        return context

def index(request):
    return render(request, "emedict/emedict.html")

def lemma_initial(request):
    try:
        request.POST["letter"] in LETTERS
    except:
        return render(
            request,
            "emedict/lemma_home.html",
            {
                "lemmalist": Lemma.objects.filter(cf__startswith="a", pos__type="COM").order_by("sortform"),
                "poslist": Lemma.POS,
            },
        )
    else:
        sletter = request.POST["letter"]
        LemmaListView.queryset = Lemma.objects.filter(
            Q(cf__startswith=sletter) | Q(cf__startswith=sletter.lower()),
            pos__type="COM"
            ).order_by("sortform")

        return HttpResponseRedirect(reverse("emedict:lemma_home"))
    
class LemmaIdView(generic.DetailView):
    model = Lemma
    template_name = "emedict/lemma_id.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        used_in = Lemma.objects.filter(
            components__isnull=False,
            components__pk=self.kwargs['pk']
        ).order_by("cf")
        context["used_in"] = used_in

        return context    

def tags(request):
    taggedlems = Lemma.objects.filter(tags__isnull=False)
    ctags = Tag.objects.filter(type="CO", lemma__in=taggedlems).distinct().order_by("term")
    gtags = Tag.objects.filter(type="GR", lemma__in=taggedlems).distinct().order_by("term")
    stags = Tag.objects.filter(type="SO", lemma__in=taggedlems).distinct().order_by("term")
    wtags = Tag.objects.filter(type="WL", lemma__in=taggedlems).distinct().order_by("term")

    context = {
        "ctags": ctags, 
        "gtags": gtags,
        "stags": stags,
        "wtags": wtags
        }

    return render(request, "emedict/tags_home.html", context)

class CompVerbView(generic.ListView):
    model = Lemma
    queryset = Lemma.objects.filter(
        Q(pos__term="verb") & ~Q(components=None)
    ).order_by("sortform")

    context_object_name = "lemmalist"
    template_name = "emedict/compverbs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["verbs"] = Lemma.objects.filter(
                lemma__in=self.queryset, pos__term='verb'
            ).order_by('sortform').distinct()

        context["nouns"] = Lemma.objects.filter(
                lemma__in=self.queryset, pos__term='noun'
            ).order_by('sortform').distinct()

        return context

class CompVerbComponentView(generic.ListView):
    model = Lemma
    context_object_name = "lemmalist"
    template_name = "emedict/cverbnoun.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Lemma.objects.filter(
            Q(pos__term="verb") 
            & Q(components__pk=self.kwargs['pk'])
        ).order_by("sortform")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["baselem"] = Lemma.objects.get(pk=self.kwargs['pk'])
        return context
