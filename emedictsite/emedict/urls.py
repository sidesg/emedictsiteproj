from django.urls import path

from . import views

app_name = "emedict"
urlpatterns = [
    path("", views.index, name="index"),
    path("lemma/", views.LemmaList.as_view(), name="lemma_home"),
    path("lemma/letter/", views.lemma_initial, name="lemma_initial"),
    path("lemma/filter", views.lemma_filter, name="lemma_filter"),
    path("lemma/<int:pk>/", views.LemmaId.as_view(), name="lemma"),
    path("lemma/<int:pk>/pos", views.lpos, name="lpos"),
    path("tags/", views.tags, name="tags_home"),
    path("tags/<int:pk>", views.TagId.as_view(), name="tag_id"),
    path("compverbs/", views.CompVerb.as_view(), name="comp_verbs")
]