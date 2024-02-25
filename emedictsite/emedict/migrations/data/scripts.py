import json
import polars as pl

def load_data(datapath: str = "emedict/migrations/data/gloss-sux-full.json") -> list[dict]:
    with open(datapath, "r", encoding="utf8") as infile:
        data = json.load(infile)["entries"]

    return data

def load_posmap(datapath: str) -> dict:
    df = pl.read_csv(datapath, columns=["epsd_abbr", "emepos_abbr"])

    return dict(zip(df['epsd_abbr'], df['emepos_abbr']))
