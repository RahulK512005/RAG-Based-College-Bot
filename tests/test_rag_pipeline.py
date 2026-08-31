import os
import sys
import json

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))

from app.database.session import SessionLocal
from app.rag.retriever import retriever
from app.rag.generator import rag_generator

def run_rag_evaluation():
    dataset_path = os.path.join(os.path.dirname(__file__), "evaluation_dataset.json")
    with open(dataset_path, "r", encoding="utf-8") as f:
        test_cases = json.load(f)

    db = SessionLocal()
    passed = 0
    total = len(test_cases)

    print("\n=======================================================")
    print(f"  RUNNING RAG EVALUATION BENCHMARK ({total} Test Cases)")
    print("=======================================================\n")

    try:
        for idx, tc in enumerate(test_cases):
            q_id = tc["id"]
            question = tc["question"]
            category = tc["category"]
            should_answer = tc["should_answer"]

            # 1. Retrieve
            retrieval = retriever.retrieve(db, question)
            
            # 2. Generate
            result = rag_generator.generate_answer(question, retrieval)
            answer = result["answer"]
            sources = result["sources"]
            is_unknown = result["is_unknown"]

            # 3. Evaluate
            test_passed = False
            failure_reason = ""

            if should_answer:
                if is_unknown:
                    failure_reason = "System incorrectly refused a known question."
                elif not sources:
                    failure_reason = "No sources attached to grounded answer."
                else:
                    # Check if expected document is cited
                    exp_doc = tc.get("expected_document")
                    matched_doc = any(exp_doc.lower() in s["document_title"].lower() for s in sources) if exp_doc else True
                    
                    if not matched_doc:
                        failure_reason = f"Expected document '{exp_doc}' was not among retrieved sources."
                    else:
                        test_passed = True
            else: # Unknown / Out-of-Domain question
                if is_unknown and "couldn't find reliable information" in answer.lower():
                    test_passed = True
                else:
                    failure_reason = "System hallucinated/answered an unknown question instead of refusing."

            status_str = "[PASS]" if test_passed else "[FAIL]"
            if test_passed:
                passed += 1

            print(f"{status_str} #{q_id} [{category}]")
            print(f"       Q: \"{question}\"")
            print(f"       Max Score: {retrieval.get('max_score', 0):.3f} | Sources: {len(sources)} | Refused: {is_unknown}")
            if not test_passed:
                print(f"       Reason: {failure_reason}")
                print(f"       Answer snippet: {answer[:120]}...")
            print("-" * 55)

        pass_rate = (passed / total) * 100
        print(f"\nEvaluation Summary: {passed}/{total} Passed ({pass_rate:.1f}%)")
        assert pass_rate >= 90.0, f"RAG pass rate {pass_rate}% below acceptable threshold!"
        print("ALL RAG EVALUATION BENCHMARKS VERIFIED SUCCESSFULLY!\n")

    finally:
        db.close()

if __name__ == "__main__":
    run_rag_evaluation()
