# NOTE: extract two entities (head/tail) and relation triplets for Knowledge Graph Construction

import warnings
warnings.filterwarnings('ignore')
import ollama  
import json 
from utils.labels import entity_labels, relation_labels 
from utils.kg_prompt import build_prompt 
# print(build_prompt)

def llm_extract_triplet(
    model_id,
    document_input
): 
    system_prompt = build_prompt(document_input) 
 
    import ollama
    response = ollama.chat(

        model=model_id,

        messages=[
            {
                "role": "system",
                "content": system_prompt
            }
        ],

        options={

            # directional consistency 강화
            "temperature": 0.0,

            # output length 제한
            "num_predict": 300,

            # repetition 감소
            "repeat_penalty": 1.1
        }
    )

    raw_output = response[
        "message"
    ]["content"]

    from utils.parse import parse_llm_output 
    parsed = parse_llm_output(
        raw_output
    )

    return parsed

# add eval-assisted functions 
def triplets_to_set(triplets):

    return set(
        (
            t["head"],
            t["relation"],
            t["tail"]
        )
        for t in triplets
    )

def evaluate_triplets(pred, gt): 

    pred_set = triplets_to_set(pred)
    gt_set = triplets_to_set(gt)

    tp = len(pred_set & gt_set)

    fp = len(pred_set - gt_set)

    fn = len(gt_set - pred_set)

    precision = tp / (tp + fp + 1e-8)

    recall = tp / (tp + fn + 1e-8)

    f1 = (
        2 * precision * recall /
        (precision + recall + 1e-8)
    ) 

    return {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4)
    }

# metrics = evaluate_triplets(
#     pred=gliner_normalized,
#     gt=llm_normalized
# )

def evaluate_by_relation(pred, gt):
    """relation-wise evaluation"""

    results = {}

    relation_types = set()

    for t in pred + gt:

        relation_types.add(
            t["relation"]
        )

    for rel in relation_types:

        pred_rel = [
            x for x in pred
            if x["relation"] == rel
        ]

        gt_rel = [
            x for x in gt
            if x["relation"] == rel
        ]

        results[rel] = evaluate_triplets(
            pred_rel,
            gt_rel
        )

    return results

def evaluate_directional_accuracy(
    pred, gt
):

    directional_relations = [
        "cause_of",
        "depends_on"
    ]

    gt_set = set(
        (
            t["head"],
            t["relation"],
            t["tail"]
        )
        for t in gt
        if t["relation"]
        in directional_relations
    )

    correct = 0
    total = 0

    reversed_errors = 0

    for t in pred:

        if (
            t["relation"]
            in directional_relations
        ):

            total += 1

            forward = (
                t["head"],
                t["relation"],
                t["tail"]
            )

            reverse = (
                t["tail"],
                t["relation"],
                t["head"]
            )

            if forward in gt_set:

                correct += 1

            elif reverse in gt_set:

                reversed_errors += 1

    return {

        "directional_accuracy":
            round(
                correct /
                (total + 1e-8),
                4
            ),

        "reverse_direction_errors":
            reversed_errors,

        "total_directional":
            total
    }