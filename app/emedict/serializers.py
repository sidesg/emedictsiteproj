from rest_framework import serializers

from .models import Lemma, Pos, LemmaDef, Form, Spelling

class SpellingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spelling
        fields = ["spelling_lat"]

class FormSerializer(serializers.ModelSerializer):
    spellings = SpellingSerializer(many=True)
    class Meta:
        model = Form
        fields = ["cf", "spellings"]

class DefSerializer(serializers.ModelSerializer):
    class Meta:
        model = LemmaDef
        fields = ["definition"]

class PosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pos
        fields = ["term", "type"]

class LemmaSerializer(serializers.ModelSerializer):
    pos = PosSerializer()
    definitions = DefSerializer(many=True)
    forms = FormSerializer(many=True)

    class Meta:
        model = Lemma
        fields = ["cf", "notes", "forms", "definitions", "pos"]