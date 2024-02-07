from django.urls import path

from . import views

app_name = "emedict"
urlpatterns = [
    path("", views.index, name="index"),
    path("lemma/", views.lemma_home, name="lemma_home"),
    path("lemma/pos", views.home_filter, name="home_filter"),
    path("lemma/<int:oid>/", views.lemma_id, name="lemma"),
    path("lemma/<int:oid>/pos", views.lpos, name="lpos")
]