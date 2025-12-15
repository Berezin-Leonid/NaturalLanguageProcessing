import os
import re
import json
import sklearn_crfsuite
import razdel
import joblib

def get_data(path):
    items = []
    for fname in os.listdir(path):
        if not fname.endswith(".txt"):
            continue
    
        text_path = os.path.join(path, fname)
        ann_path = text_path.replace(".txt", ".ann")
        text = open(text_path, encoding="utf8").read()
        ents = []
        if os.path.exists(ann_path):
            for line in open(ann_path, encoding="utf8"):
                if not line.strip():
                    continue
                parts = line.strip().split("\t")
                if len(parts) < 2:
                    continue
                tag = parts[1].split()
                if len(tag) >= 3:
                    try:
                        ents.append((int(tag[1]), int(tag[2]), tag[0]))
                    except:
                        pass
        items.append({"id": fname, "text": text, "entities": ents})
    return items

def train_data():
    return get_data("/home/berezin/Desktop/NLP/NaturalLanguageProcessing/Problem3/NEREL/NEREL-v1.1/train")


def shape(tok):
    return re.sub(r"[A-ZА-Я]", "X", re.sub(r"[a-zа-я]", "x", re.sub(r"\d", "d", tok)))



def token_features(tokens, i):
    tok = tokens[i][0]
    feats = {
        "bias": 1.0,
        "lower": tok.lower(),
        "isupper": tok.isupper(),
        "istitle": tok.istitle(),
        "isdigit": tok.isdigit(),
        "pref2": tok[:2],
        "pref3": tok[:3],
        "suff2": tok[-2:],
        "suff3": tok[-3:],
        "shape": shape(tok),
        "contains_dash": "-" in tok,
        "contains_dot": "." in tok,
    }

    for offset in [-2, -1, 1, 2]:
        j = i + offset
        if 0 <= j < len(tokens):
            feats[f"{offset}:lower"] = tokens[j][0].lower()
            feats[f"{offset}:istitle"] = tokens[j][0].istitle()

    if i == 0:
        feats["BOS"] = True
    if i == len(tokens) - 1:
        feats["EOS"] = True
    return feats


def process_data(data):
    data = []
    for it in data:
        text = it["text"]
        ents = [(int(s), int(e), str(l)) for s, e, l in it["entities"]]
        tokens = tokenize_with_spans(text)
        feats = [token_features(tokens, i) for i in range(len(tokens))]
        tags = spans_to_bio(tokens, ents)
        data.append(
            {
                "tokens": tokens,
                "features": feats,
                "tags": tags,
                "entities": ents,
                "id": it.get("id"),
            }
        )
    return data


def tokenize_with_spans(text: str):
    return [(t.text, t.start, t.stop) for t in razdel.tokenize(text)]


def spans_to_bio(tokens, entities):
    tags = ["O"] * len(tokens)
    for i, (_, s, e) in enumerate(tokens):
        for es, ee, lab in entities:
            if s >= es and e <= ee:
                tags[i] = "B-" + lab if s == es else "I-" + lab
                break
    return tags



def train():
    data = train_data()
    prep_data = process_data(data)

    X = [elem["features"] for elem in prep_data]
    y = [elem["tags"] for elem in prep_data]

    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1, # L1 regularization
        c2=0.1, # L2 regularization
        max_iterations=100,
        all_possible_transitions=True,
        verbose=True
    )
    crf.fit(X,y)

    joblib.dump(crf, "model.pkl")

if __name__ == "__main__":
    train()