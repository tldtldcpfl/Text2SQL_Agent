from utils.labels import KOREAN_PARTICLES, RELATION_MAP
# print(KOREAN_PARTICLES)
import re
import json 

def parse_gliner_relations(relations):

    triplets = []

    for rel in relations[0]:

        triplets.append({
            "head": rel["head"]["text"].strip(),
            "relation": rel["relation"].strip(),
            "tail": rel["tail"]["text"].strip(),
            "score": round(rel["score"], 4)
        })

    return triplets 

def normalize_entity(text):

    text = text.lower().strip()

    # 괄호 제거
    text = re.sub(r"\(.*?\)", "", text)

    # 특수문자 제거
    text = re.sub(r"[^\w\s가-힣]", "", text)

    text = text.strip()

    # 조사 제거
    for particle in KOREAN_PARTICLES:

        if text.endswith(particle):
            text = text[:-len(particle)]

    # 공백 normalize
    text = " ".join(text.split())

    return text.strip()


def normalize_relation(rel):

    rel = rel.lower().strip()

    return RELATION_MAP.get(rel, rel)

def normalize_triplets(triplets):

    normalized = []

    for t in triplets:

        normalized.append({
            "head": normalize_entity(t["head"]),
            "relation": normalize_relation(t["relation"]),
            "tail": normalize_entity(t["tail"])
        })

    return normalized 

def parse_llm_output(text):

    try:

        parsed = json.loads(text)

        if isinstance(parsed, list):
            return parsed

        if isinstance(parsed, dict):

            if "triplets" in parsed:
                return parsed["triplets"]

    except:
        pass

    # fallback:
    # markdown/codeblock/json extraction

    match = re.search(
        r"\[.*\]",
        text,
        re.DOTALL
    )

    if match:

        try:
            return json.loads(
                match.group()
            )

        except:
            return []

    return [] 