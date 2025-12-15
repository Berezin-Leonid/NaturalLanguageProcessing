# utils.py
import os
import razdel
import numpy as np
from collections import defaultdict
from typing import List, Tuple, Dict, Any
import re

# ---------- Tokenization & BIO ----------


def tokenize_with_spans(text: str):
    """Разбивает текст на токены с позициями."""
    return [(t.text, t.start, t.stop) for t in razdel.tokenize(text)]


def spans_to_bio(tokens, entities):
    """Конвертирует список сущностей (start,end,label) в BIO-теги."""
    tags = ["O"] * len(tokens)
    for i, (_, s, e) in enumerate(tokens):
        for es, ee, lab in entities:
            if s >= es and e <= ee:
                tags[i] = "B-" + lab if s == es else "I-" + lab
                break
    return tags


def bio_to_spans(tokens, tags):
    """Из BIO-тегов восстанавливает список (start,end,label)."""
    spans, cur = [], None
    for (tok, s, e), tag in zip(tokens, tags):
        if tag.startswith("B-"):
            if cur:
                spans.append(cur)
            cur = [s, e, tag[2:]]
        elif tag.startswith("I-") and cur and cur[2] == tag[2:]:
            cur[1] = e
        else:
            if cur:
                spans.append(cur)
            cur = None
    if cur:
        spans.append(cur)
    return [tuple(x) for x in spans]


# ---------- Features ----------


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


def prepare_examples(items):
    """Создаёт список примеров с токенами, BIO-тегами и фичами."""
    data = []
    for it in items:
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


# ---------- Metrics ----------


def compute_metrics(gold_list, pred_list):
    """Вычисляет среднее F1 по типам (точное совпадение спанов и типа)."""
    gold_by_t, pred_by_t = defaultdict(set), defaultdict(set)
    for i, (golds, preds) in enumerate(zip(gold_list, pred_list)):
        for s, e, l in golds:
            gold_by_t[l].add((i, s, e))
        for s, e, l in preds:
            pred_by_t[l].add((i, s, e))

    types = sorted(set(gold_by_t) | set(pred_by_t))
    per_t = {}
    for t in types:
        g, p = gold_by_t[t], pred_by_t[t]
        tp = len(g & p)
        P = tp / len(p) if p else 0
        R = tp / len(g) if g else 0
        F1 = 2 * P * R / (P + R) if (P + R) > 0 else 0
        per_t[t] = {"P": P, "R": R, "F1": F1, "gold": len(g), "pred": len(p), "tp": tp}

    avg_F1 = np.mean([v["F1"] for v in per_t.values()]) if per_t else 0
    return {"avg_F1": avg_F1, "per_type": per_t}


# ---------- Data loading ----------


def load_nerel_split(split_path: str):
    """
    Загружает один сплит NEREL (папка с .txt и .ann).
    Возвращает список словарей {id, text, entities}.
    """
    items = []
    for fname in os.listdir(split_path):
        if not fname.endswith(".txt"):
            continue
        text_path = os.path.join(split_path, fname)
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
