from django.urls import path

from . import views

app_name = "emedict"
urlpatterns = [
    path("", views.index, name="index"),
    path("lemma/", views.LemmaListView.as_view(), name="lemma_home"),
    path("lemma/letter/", views.lemma_initial, name="lemma_initial"),
    path("lemma/<int:pk>/", views.LemmaIdView.as_view(), name="lemma"),
    path("lemma/<int:pk>.json", views.lemma_json, name="lemma_json"),
    path("lemma/<int:pk>.ttl", views.lemma_ttl, name="lemma_ttl"),
    path("lemma/emesal/", views.LemmaEmesalListView.as_view(), name="lemesal"),
    path("tags/", views.tags, name="tags_home"),
    path("tags/<int:pk>/", views.TagIdView.as_view(), name="tag_id"),
    path("compverbs/", views.CompVerbView.as_view(), name="comp_verbs"),
    path("compverbs/<int:pk>/", views.CompVerbComponentView.as_view(), name="compverbcomp")
]