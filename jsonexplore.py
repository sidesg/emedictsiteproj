import json
import pprint

datapath = "emedictsite/emedict/migrations/data/gloss-sux-full.json"

with open(datapath, "r", encoding="utf8") as infile:
    data = json.load(infile)["entries"]

posset = set([l["pos"] for l in data])

posdict = dict()


posex = [
    (l["oid"], l["cf"], [(c["ref"], c["cf"]) for c in l["compound"]])
    for l in data 
    if (l.get("compound", None) and l.get("oid", None))]
pprint.pprint(posex)

# for pos in posset:
#     try:
#         posex = [
#             (l.get("cf", "cf error"), l.get("oid", "oid error")) 
#             for l in data 
#             if l["pos"] == pos][:5]
#         posdict[pos] = posex
#     except:
#         print(f"error {pos}")

# pprint.pprint(posdict)
# for pos in sorted(posset):
#     print(pos)
