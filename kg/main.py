from pathlib import Path
import sys
import warnings

warnings.filterwarnings("ignore")


def _ensure_repo_root_on_path():
    repo_root = Path(__file__).resolve().parents[1]
    repo_root_str = str(repo_root)
    if repo_root_str not in sys.path:
        sys.path.insert(0, repo_root_str)


_ensure_repo_root_on_path()

from kg.gen_logical_answer import gen_kg_answer
from kg.query_router import classify_query


def route_query(user_query: str) -> str:
    probs = classify_query(user_query)
    return max(probs, key=probs.get).replace("_prob", "")


def main(user_query: str):
    probs = classify_query(user_query)
    query_prob_key = max(probs, key=probs.get)
    query_type = query_prob_key.replace("_prob", "")

    print(f"\n[query_router_probs] {probs}", flush=True) 
    print(f"\n[top_query_prob] {query_prob_key}: {probs[query_prob_key]:.4f}", flush=True)
    print(f"\n[query_type] {query_type}", flush=True)

    if query_type in {"Logical", "Hybrid"}:
        print("\n[KG pipeline] gen_kg_answer() 실행", flush=True)
        answer = gen_kg_answer(user_query)
        print("\n[answer]")
        print(answer)
        return answer

    print("\n[KG pipeline] Semantic으로 분류되어 gen_kg_answer()를 실행하지 않았습니다.", flush=True)
    print("\n[answer]", flush=True)
    print("Semantic query로 분류되었습니다.", flush=True)
    return None


if __name__ == "__main__":
    while True:
        user_query = input("질문을 입력하세요 (종료하려면 'exit' 입력): ").strip()

        if user_query.lower() == "exit":
            print("프로그램을 종료합니다.")
            break

        if not user_query:
            continue

        main(user_query) 
