from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db.models import Q

from .models import Lemma, Tag

LETTERS = ["A", "B", "D", "E", "G", "Ŋ", "H", "Ḫ", "I", "K",
            "L", "M", "N", "P", "R", "Ř", "S", "Š", "T", "U", "Z"]

class TagId(generic.DetailView):
    model = Tag
    template_name = "emedict/tags_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lemmata"] = Lemma.objects.filter(tags__id=self.kwargs['pk'])

        return context

class LemmaList(generic.ListView): 
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

def lemma_filter(request):
    return HttpResponse([i for i in request.POST.items()][1:])

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
        LemmaList.queryset = Lemma.objects.filter(
            Q(cf__startswith=sletter) | Q(cf__startswith=sletter.lower()),
            pos__type="COM"
            ).order_by("cf")

        return HttpResponseRedirect(reverse("emedict:lemma_home"))
    
class LemmaId(generic.DetailView):
    model = Lemma
    template_name = "emedict/lemma_id.html"

def lpos(request, pk):
    lemma = get_object_or_404(Lemma, pk=pk)

    try:
        Lemma.POS[request.POST["choice"]]
    except:
        return render(
            request,
            "emedict/lemma_id.html",
            {
                "lemma": lemma,
                "error_message": "You didn't select a POS.",
            },
        )
    else:
        lemma.pos = request.POST["choice"]
        lemma.save()

        return HttpResponseRedirect(reverse("emedict:lemma", args=(lemma.oid,)))

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

class CompVerb(generic.ListView):
    model = Lemma
    queryset = Lemma.objects.filter(
        Q(pos__term="verb") & ~Q(components=None)
    )
    context_object_name = "lemmalist"
    template_name = "emedict/compverbs.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        shu = Lemma.objects.filter(
            Q(pos__term="verb") & Q(components__lemmaoid__oid="o0039506")
        ).order_by("cf")
        context["shu"] = shu
        comps = Lemma.objects.filter(components__pos__term="verb").values_list("components")
        verbs = [Lemma.objects.get(pk=l[0]) for l in comps]
        verbs = set([l for l in verbs if l.pos.term == "verb"])
        context["verbs"] = verbs

        nouns = [Lemma.objects.get(pk=l[0]) for l in comps]
        nouns = set([l for l in nouns if l.pos.term == "noun"])
        context["nouns"] = nouns

        return context
