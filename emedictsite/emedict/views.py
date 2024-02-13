from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Lemma


def index(request):
    return render(request, "emedict/emedict.html")

def lemma_home(request):
    lemmalist = Lemma.objects.order_by("cf")
    context = {
        "lemmalist": lemmalist,
        "poslist": Lemma.POS
    }
    return render(request, "emedict/lemma_home.html", context)

def lemma_filter(request):
    return HttpResponse([i for i in request.POST.items()][1:])

def lemma_id(request, oid):
    lemma = get_object_or_404(Lemma, oid=oid)

    oid = "o" + str(lemma.oid).zfill(7)
    context = {
        "lemma": lemma,
        "oid": oid,
    }
    return render(request, "emedict/lemma_id.html", context)

def lpos(request, oid):
    lemma = get_object_or_404(Lemma, oid=oid)

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

        oid = "o" + str(lemma.oid).zfill(7)

        return HttpResponseRedirect(reverse("emedict:lemma", args=(lemma.oid,)))

def tags(request):
    ...

def tag_id(reques, pk):
    ...