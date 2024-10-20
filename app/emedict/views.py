from typing import Any
from django.db.models.query import QuerySet
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from django.db.models import Q

from .forms import LemmaSearchForm, LemmaInitialLetterForm, FacetSideBarForm
from .models import Lemma, Tag, FormType, Form, TxtSource, Pos

class TagIdView(generic.DetailView):
    model = Tag
    template_name = "emedict/tags_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lemmata"] = Lemma.objects.filter(tags__id=self.kwargs['pk']).order_by("sortform")

        return context

class LemmaListView(generic.FormView):
    template_name = "emedict/lemma_home.html"
    lemmalist = None

    def get(self, request, *args, **kwargs):
        form = LemmaInitialLetterForm(self.request.GET or None)

        if form.is_valid():
            initial = request.GET["initial"]
            self.lemmalist = Lemma.objects.filter(
                Q(cf__startswith=initial.lower()) | Q(cf__startswith=initial.upper()),
                pos__type="COM"
            ).order_by("sortform")

        else:
            self.lemmalist = Lemma.objects.filter(
                Q(cf__startswith="a") | Q(cf__startswith="A"), 
                pos__type="COM"
            ).order_by("sortform")

        return self.render_to_response(self.get_context_data(form=form))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["lem_search_form"] = LemmaSearchForm
        context["lem_init_form"] = LemmaInitialLetterForm
        context["sidebar_form"] = FacetSideBarForm
        context["lemmalist"] = self.lemmalist

        if self.lemmalist:
            context["sidebar_form"] = FacetSideBarForm(
                Pos.objects.filter(id__in=self.lemmalist.values("pos")),
                Tag.objects.filter(id__in=self.lemmalist.values("tags"))               
            )

        return context
    
class LemmaFacetView(generic.FormView):
    template_name = "emedict/facet_landing.html"

    def get(self, request, *args, **kwargs):
        form = FacetSideBarForm(self.request.GET or None)

        self.poss = request.GET.getlist("poss", default=[p.term for p in Pos.objects.all()])
        self.tags = request.GET.getlist("tags", default=[t.term for t in Tag.objects.all()])

        self.lemmalist = Lemma.objects.filter(
            Q(pos__term__in=self.poss)
            & Q(tags__term__in=self.tags),
            pos__type="COM"
        ).distinct().order_by("sortform")

        return self.render_to_response(self.get_context_data(form=form))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["poss"] = self.poss
        context["tags"] = self.tags
        context["lemmalist"] = self.lemmalist

        return context

class LemmaSearchView(LemmaListView):
    template_name = "emedict/lemma_search.html"

    def get(self, request, *args, **kwargs):
        form = LemmaSearchForm(self.request.GET or None)
        if form.is_valid():
            term = request.GET["lemma"]
            # TODO: convert sub nums to regular? (or just need to add elasticsearch?)
            self.lemmalist = Lemma.objects.filter(
                Q(cf=term.lower()) | Q(cf=term.upper())
                | Q(sortform=term.lower())
                | Q(form__spelling__spelling_lat=term.lower(),
                    pos__type="COM")
            ).distinct().order_by("sortform")
    
        return self.render_to_response(self.get_context_data(form=form))

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
        context["lem_search_form"] = LemmaSearchForm
        context["lem_init_form"] = LemmaInitialLetterForm

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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)

    #     return context

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
