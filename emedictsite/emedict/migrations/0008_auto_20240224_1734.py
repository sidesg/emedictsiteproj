# Generated by Django 5.0.2 on 2024-02-24 17:34

from django.db import migrations
import json

def load_data(datapath: str = "emedict/migrations/data/gloss-sux-full.json") -> list[dict]:
    with open(datapath, "r", encoding="utf8") as infile:
        data = json.load(infile)["entries"]

    return data

def add_data(apps, schema_editor):
    Lemma = apps.get_model("emedict", "Lemma")
    data = load_data()
    
    for parent in data:
        if (parent.get("compound", None) and parent.get("oid", None)):
            parentl = Lemma.objects.get(lemmaoid__oid=parent["oid"])
            comp_oids = [c["ref"] for c in parent["compound"]]
            for compoid in comp_oids:
                try:
                    compl = Lemma.objects.get(lemmaoid__oid=compoid)
                    parentl.components.add(compl)
                except:
                    print(f"Error: {parentl.cf} - {compl.cf}")



class Migration(migrations.Migration):

    dependencies = [
        ("emedict", "0007_alter_lemma_components"),
    ]

    operations = [
        migrations.RunPython(add_data),
    ]
