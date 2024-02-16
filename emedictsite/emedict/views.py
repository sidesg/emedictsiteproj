from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic

from .models import Lemma, Tag
from .forms import AddDefinition

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["poslist"] = Lemma.POS

        return context

def index(request):
    return render(request, "emedict/emedict.html")

def lemma_filter(request):
    return HttpResponse([i for i in request.POST.items()][1:])

def lemma_id(request, pk):
    lemma = get_object_or_404(Lemma, pk=pk)

    oid = "o" + str(lemma.oid).zfill(7)
    context = {
        "lemma": lemma,
        "oid": oid,
        "adddef": AddDefinition()
    }

    return render(request, "emedict/lemma_id.html", context)

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
    ctags = Tag.objects.filter(type="CO")
    gtags = Tag.objects.filter(type="GR")

    context = {"ctags": ctags, "gtags": gtags}

    return render(request, "emedict/tags_home.html", context)