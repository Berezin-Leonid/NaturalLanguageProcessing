# tester.py
import sys
import io
import json
import numpy as np
from solution import Solution


path_to_data = "/home/berezin/Desktop/NLP/NaturalLanguageProcessing/Problem2/tracks.json"

# --- Загрузка данных ---
with open(path_to_data, "r", encoding="utf-8") as f:
    tracks = json.load(f)

print(f"Загружено {len(tracks)} треков")

# --- Метрики ---
def f1_micro(predicted, expected):
    total_tp = total_pred = total_exp = 0
    for pred, exp in zip(predicted, expected):
        pred_set, exp_set = set(pred), set(exp)
        tp = len(pred_set & exp_set)
        total_tp += tp
        total_pred += len(pred_set)
        total_exp += len(exp_set)

    if total_pred == 0 or total_exp == 0:
        return 0.0
    precision = total_tp / total_pred
    recall = total_tp / total_exp
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def f1_micro_one(pred, exp):
    pred_set, exp_set = set(pred), set(exp)
    tp = len(pred_set & exp_set)
    if len(pred_set) == 0 or len(exp_set) == 0:
        return 0.0, 0.0, 0.0
    precision = tp / len(pred_set)
    recall = tp / len(exp_set)
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
    return precision, recall, f1


# --- Подготовка данных ---
tracks_for_model = [
    ([line.strip() for line in track["lines"] if line.strip()], track.get("title", ""))
    for track in tracks
]
true_segments = [[tuple(seg) for seg in track["chorus"]] for track in tracks]

# --- Запуск модели ---
detector = Solution()
pred_segments_all = detector.detect(tracks_for_model)

# --- Расчёт метрик ---
all_prec, all_rec, all_f1 = [], [], []
for i, (pred, exp) in enumerate(zip(pred_segments_all, true_segments)):
    p, r, f = f1_micro_one(pred, exp)
    all_prec.append(p)
    all_rec.append(r)
    all_f1.append(f)
    print("=" * 80)
    print(f"Трек {tracks[i]['track_id']} | {tracks[i].get('title','')}")
    print(f"Истина: {exp}")
    print(f"Предсказано: {list(pred)}")
    print(f"Precision={p:.3f} Recall={r:.3f} F1={f:.3f}")

# --- Итоговые метрики ---
micro = f1_micro(pred_segments_all, true_segments)
print("=" * 80)
print("Средние значения по всем трекам:")
print(f"Precision={np.mean(all_prec):.3f} Recall={np.mean(all_rec):.3f} Macro-F1={np.mean(all_f1):.3f}")
print(f"Metric micro-F1: {micro:.3f}")
