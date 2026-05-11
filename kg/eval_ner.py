from tqdm.auto import tqdm
import pandas as pd
import time
import warnings
warnings.filterwarnings('ignore')
from gliner import GLiNER
import json 

from utils.labels import entity_labels, relation_labels
from utils.parse import normalize_triplets 
# print('[debug]', normalize_triplets)

# Load config.json 
with open("config.json", "r", encoding='utf-8') as f:
    config = json.load(f)


def run_kg_benchmark(

    eval_data,

    enc,

    model_id,  # llm_id 

    entity_labels,

    relation_labels
):

    # =====================================================
    # accumulators
    # =====================================================

    gliner_all_pred = []
    llm_all_pred = []
    all_gt = []

    gliner_latency = []
    llm_latency = []

    # =====================================================
    # eval loop
    # =====================================================

    for sample in tqdm(
        eval_data, 
        desc="NER Evaluating..."
    ):

        document = sample["document"]
        
        gt = normalize_triplets(
            sample["triplets"]
        )

        all_gt.extend(gt)

        # =================================================
        # GLINER
        # =================================================

        start = time.time()

        entities, relations = enc.inference(

            texts=[document],

            labels=entity_labels,

            relations=relation_labels,

            threshold=0.25,

            adjacency_threshold=0.5,

            relation_threshold=0.3,

            return_relations=True,

            flat_ner=False
        )
        # print('[debug]\n', entities, relations)

        gliner_latency.append(
            time.time() - start
        )
        from utils.parse import (
            parse_gliner_relations, 
            normalize_entity
            )
        parsed_gliner = parse_gliner_relations(
            relations
        )

        gliner_normalized = normalize_triplets(
            parsed_gliner
        )

        gliner_all_pred.extend(
            gliner_normalized
        )
        # print('[debug]', gliner_all_pred)

        # =================================================
        # LLM
        # =================================================

        start = time.time()

        from extraction import llm_extract_triplet 
        from utils.kg_prompt import build_prompt

        llm_raw = llm_extract_triplet(
            model_id,
            build_prompt(document)
        )

        llm_latency.append(
            time.time() - start
        )

        llm_normalized = normalize_triplets(
            llm_raw
        )

        llm_all_pred.extend(
            llm_normalized
        )
        # print('[debug]', llm_all_pred)

    # # =====================================================
    # # FINAL METRICS
    # # =====================================================
    # from extraction import (evaluate_triplets,
    #                         evaluate_by_relation,
    #                         evaluate_directional_accuracy
    #                         )
    
    # gliner_results = {

    #     "overall_metrics":

    #         evaluate_triplets(
    #             gliner_all_pred,
    #             all_gt
    #         ),

    #     "relation_metrics":

    #         evaluate_by_relation(
    #             gliner_all_pred,
    #             all_gt
    #         ),

    #     "directional_metrics":

    #         evaluate_directional_accuracy(
    #             gliner_all_pred,
    #             all_gt
    #         ),

    #     "avg_latency_sec":

    #         round(
    #             sum(gliner_latency)
    #             /
    #             len(gliner_latency),
    #             4
    #         )
    # }

    # # =====================================================

    # llm_results = {

    #     "overall_metrics":

    #         evaluate_triplets(
    #             llm_all_pred,
    #             all_gt
    #         ),

    #     "relation_metrics":

    #         evaluate_by_relation(
    #             llm_all_pred,
    #             all_gt
    #         ),

    #     "directional_metrics":

    #         evaluate_directional_accuracy(
    #             llm_all_pred,
    #             all_gt
    #         ),

    #     "avg_latency_sec":

    #         round(
    #             sum(llm_latency)
    #             /
    #             len(llm_latency),
    #             4
    #         )
    # }

    # # =====================================================
    # # flatten helper
    # # =====================================================

    # def flatten_results(
    #     extractor_name,
    #     results
    # ):

    #     overall = results[
    #         "overall_metrics"
    #     ]

    #     directional = results[
    #         "directional_metrics"
    #     ]

    #     row = {

    #         "model":
    #             extractor_name,

    #         # ---------------------------------------------
    #         # overall
    #         # ---------------------------------------------

    #         "precision":
    #             overall["precision"],

    #         "recall":
    #             overall["recall"],

    #         "f1":
    #             overall["f1"],

    #         # ---------------------------------------------
    #         # directional
    #         # ---------------------------------------------

    #         "directional_accuracy":
    #             directional[
    #                 "directional_accuracy"
    #             ],

    #         "reverse_direction_errors":
    #             directional[
    #                 "reverse_direction_errors"
    #             ],

    #         # ---------------------------------------------
    #         # latency
    #         # ---------------------------------------------

    #         "avg_latency_sec":
    #             results[
    #                 "avg_latency_sec"
    #             ]
    #     }

    #     # relation-wise metrics

    #     relation_metrics = results[
    #         "relation_metrics"
    #     ]

    #     for rel, metric in relation_metrics.items():

    #         row[f"{rel}_f1"] = metric["f1"]

    #     return row

    # # =====================================================
    # # final dataframe
    # # =====================================================

    # comparison_df = pd.DataFrame([

    #     flatten_results(
    #         "GLINER",
    #         gliner_results
    #     ),

    #     flatten_results(
    #         "LLM",
    #         llm_results
    #     )
    # ])

    # return comparison_df


def run_eval():
    # Load encoder 
    enc = GLiNER.from_pretrained(
        config["encoder_id"]
    )  
    # Load eval dataset 
    eval_data_path = config["eval_data_path"] 
    with open(eval_data_path, "r", encoding="utf-8") as f:
        eval_data = json.load(f) 

    comparison_df = run_kg_benchmark(

        eval_data=eval_data,

        enc=enc,

        model_id= config["llm_id"],

        entity_labels=entity_labels,

        relation_labels=relation_labels
    )

    return comparison_df

    # print(
    #     comparison_df.to_string(
    #         index=False
    #     ) )

# run_eval() 