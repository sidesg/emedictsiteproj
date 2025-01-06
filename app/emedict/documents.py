from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from .models import Lemma, Pos, LemmaDef, Form, Spelling

@registry.register_document
class LemmaDocument(Document):
    pos = fields.ObjectField(properties={
        "term": fields.TextField()
    })
    definitions = fields.ObjectField(properties={
        "definition": fields.TextField()
    }) 
    forms = fields.ObjectField(properties={
        "cf": fields.TextField(),
        "spellings": fields.ObjectField(properties={
            "spelling_lat": fields.TextField()
        })
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
            "id",
            "cf",
            "sortform",
            "notes",
        ]
        related_models = [Pos, LemmaDef, Form, Spelling]

    def get_instances_from_related(self, related_instance):
        if isinstance(related_instance, Pos):
            related_instance.lemma_set.all()
        elif isinstance(related_instance, LemmaDef):
            related_instance.lemma
        elif isinstance(related_instance, Form):
            related_instance.lemma_set.all()
