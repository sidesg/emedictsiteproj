from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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
        context["lemmata"] = Lemma.objects.filter(tags__id=self.kwargs['pk'])

        return context

class LemmaListView(generic.ListView): 
    model = Lemma
    context_object_name = "lemmalist"
    template_name = "emedict/lemma_home.html"
    queryset = Lemma.objects.filter(cf__startswith="a", pos__type="COM").order_by("cf")

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
                "lemmalist": Lemma.objects.filter(cf__startswith="a", pos__type="COM").order_by("cf"),
                "poslist": Lemma.POS,
            },
        )
    else:
        sletter = request.POST["letter"]
        LemmaListView.queryset = Lemma.objects.filter(
            Q(cf__startswith=sletter) | Q(cf__startswith=sletter.lower()),
            pos__type="COM"
            ).order_by("cf")

        return HttpResponseRedirect(reverse("emedict:lemma_home"))
    
class LemmaIdView(generic.DetailView):
    model = Lemma
    template_name = "emedict/lemma_id.html"

def tags(request):
    ctags = Tag.objects.filter(type="CO").order_by("term")
    gtags = Tag.objects.filter(type="GR").order_by("term")
    stags = Tag.objects.filter(type="SO").order_by("term")
    wtags = Tag.objects.filter(type="WL").order_by("term")

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
    ).order_by("cf")

    context_object_name = "lemmalist"
    template_name = "emedict/compverbs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        verbs=Lemma.objects.filter(
                lemma__in=self.queryset, pos__term='verb'
            ).order_by('cf').distinct()
        context["verbs"] = verbs

        nouns=Lemma.objects.filter(
                lemma__in=self.queryset, pos__term='noun'
            ).order_by('cf').distinct()
        context["nouns"] = nouns

        return context

class CompVerbComponentView(generic.ListView):
    model = Lemma
    context_object_name = "lemmalist"
    template_name = "emedict/cverbnoun.html"

    def get_queryset(self) -> QuerySet[Any]:
        return Lemma.objects.filter(
            Q(pos__term="verb") 
            & Q(components__pk=self.kwargs['pk'])
        ).order_by("cf")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baselem = Lemma.objects.get(pk=self.kwargs['pk'])
        context["baselem"] = baselem
        return context
