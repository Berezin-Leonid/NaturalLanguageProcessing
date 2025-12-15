import os
import json
import random
import joblib
import numpy as np
import sklearn_crfsuite

from utils import load_nerel_split, prepare_examples, bio_to_spans, compute_metrics

# ---------------- CONFIG ----------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

DATA_ROOT = os.path.join("NEREL", "NEREL-v1.1")
MODEL_PATH = "model.joblib"
RESULTS_PATH = "results.json"

DISCONTINUOUS_TEST_FILES = {
    "165459_text.txt",
    "176167_text.txt",
    "178485_text.txt",
    "192238_text.txt",
    "193267_text.txt",
    "193946_text.txt",
    "194112_text.txt",
    "2021.txt",
    "202294_text.txt",
    "2031.txt",
    "209438_text.txt",
    "209731_text.txt",
    "546860_text.txt",
}


# ---------------- MAIN ----------------
def train_and_eval():
    print("Loading NEREL v1.1 dataset from:", DATA_ROOT)
    train_items = load_nerel_split(os.path.join(DATA_ROOT, "train"))
    dev_items = load_nerel_split(os.path.join(DATA_ROOT, "dev"))
    test_items = load_nerel_split(os.path.join(DATA_ROOT, "test"))
    test_items = [it for it in test_items if it["id"] not in DISCONTINUOUS_TEST_FILES]

    print(f"Train: {len(train_items)}, Dev: {len(dev_items)}, Test: {len(test_items)}")

    # Prepare examples
    train_p = prepare_examples(train_items)
    val_p = prepare_examples(dev_items)
    test_p = prepare_examples(test_items)

    X_train = [ex["features"] for ex in train_p]
    y_train = [ex["tags"] for ex in train_p]

    print("Training CRF model...")
    crf = sklearn_crfsuite.CRF(
        algorithm="lbfgs",
        c1=0.1,  # L1-регуляризация
        c2=0.01,  # L2-регуляризация
        max_iterations=150,
        all_possible_transitions=True,
        verbose=True,
    )
    crf.fit(X_train, y_train)
    joblib.dump(crf, MODEL_PATH)
    print("Model saved to", MODEL_PATH)

    def eval_split(name, examples):
        X = [ex["features"] for ex in examples]
        y_pred = crf.predict(X)
        preds = [bio_to_spans(ex["tokens"], yp) for ex, yp in zip(examples, y_pred)]
        golds = [ex["entities"] for ex in examples]
        m = compute_metrics(golds, preds)
        print(f"{name} avg F1 = {m['avg_F1']:.4f}")
        return m

    metrics = {
        "val": eval_split("Validation", val_p),
        "test": eval_split("Test", test_p),
    }

    json.dump(
        metrics, open(RESULTS_PATH, "w", encoding="utf8"), ensure_ascii=False, indent=2
    )
    print("Saved metrics to", RESULTS_PATH)


if __name__ == "__main__":
    train_and_eval()
