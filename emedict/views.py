from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpRequest
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.db.models import Q

from .forms import LemmaSearchForm
from .models import Lemma, Tag, FormType, Form, TxtSource, Pos

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
        context["pos"] = Pos.objects.filter(
            id__in=self.queryset.values("pos")
        )
        context["tags"] = Tag.objects.filter(
            id__in=self.queryset.values("tags")
        )
        context["lem_search_form"] = LemmaSearchForm

        return context

def index(request):
    return render(request, "emedict/emedict.html")

def lemma_json(request, pk):
    lem = Lemma.objects.get(pk=pk)
    lem_uri = request.build_absolute_uri(lem.pk)
    data = lem.make_jsonld(lem_uri)
    return JsonResponse(data,safe = False) 

def lemma_ttl(request, pk):
    lem = Lemma.objects.get(pk=pk)
    lem_uri = request.build_absolute_uri(lem.pk)
    data = lem.make_ttl(lem_uri)
    response = HttpResponse(content_type='text/plain; charset=utf-8')  
    response['Content-Disposition'] = f'filename="{pk}.ttl"'

    response.write(data)

    return response

def lemma_initial(request: HttpRequest):
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
    
def lemma_search(request):
    if request.method == "POST":
        lem_search_form = LemmaSearchForm(request.POST)

        if lem_search_form.is_valid():
            term = request.POST["searched_lemma"]
            LemmaListView.queryset = Lemma.objects.filter(
                Q(cf=term.lower()) | Q(cf=term.upper())
            ).order_by("sortform")

            return HttpResponseRedirect(reverse("emedict:lemma_home"))
    else:
        lem_search_form = LemmaSearchForm()

    return render(request, "emedict/lemma_home.html", {"lem_search_form": lem_search_form})

class LemmaIdView(generic.DetailView):
    model = Lemma
    template_name = "emedict/lemma_id.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["used_in"] = Lemma.objects.filter(
            components__isnull=False,
            components__pk=self.kwargs['pk']
        ).order_by("sortform")
        context["admin_edit"] = reverse(
            "admin:emedict_lemma_change", args=(self.kwargs["pk"],))
        context["emesal"] = FormType.objects.get(term="emesal")

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

class LemmaEmesalListView(generic.ListView):
    model = Lemma
    context_object_name = "lemmalist"
    template_name = "emedict/lemesal.html"
    queryset = Lemma.objects.filter(
        pos__type="COM",
        form__in=Form.objects.filter(formtype=12)
                                    ).order_by("sortform")
    # emesalform = Form.objects.get(formtype=12)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["letters"] = LETTERS

        return context
    
class TxtSourceView(generic.DetailView):
    model = TxtSource
    template_name = "emedict/txtsource.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["lemmata"] = Lemma.objects.filter(
            lemmacitation__source__pk=self.kwargs['pk']
        ).order_by("sortform")

        return context

class TxtSourceListView(generic.ListView):
    model = TxtSource
    context_object_name = "txtlist"
    template_name = "txtsource_list.html"