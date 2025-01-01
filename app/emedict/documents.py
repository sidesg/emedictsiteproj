from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Lemma, Pos, LemmaDef, Form

@registry.register_document
class LemmaDocument(Document):
    pos = fields.ObjectField(properties={
        "term": fields.TextField()
    })
    definitions = fields.NestedField(properties={
        "definition": fields.TextField(),
        "pk": fields.IntegerField(),
    }) 
    forms = fields.NestedField(properties={
        "cf": fields.TextField()
    })

    class Index:
        name = "lemma"
        settings = {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    
    class Django:
        model = Lemma

        fields = [
            "cf",
            "sortform",
            "notes",
        ]
        related_models = [Pos, LemmaDef]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Pos):
            related_instance.lemma_set.all()
        elif isinstance(related_instance, LemmaDef):
            related_instance.lemma
        elif isinstance(related_instance, Form):
            related_instance.lemma_set.all()
    