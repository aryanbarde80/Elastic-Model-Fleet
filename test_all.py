"""
test_all.py — Tests all 100 model API endpoints.

Usage:
    python test_all.py --base-url https://your-service.onrender.com

Or test a specific model:
    python test_all.py --base-url https://your-service.onrender.com --model sentiment-analysis-roberta
"""

import requests
import argparse
import json
import time
from typing import Optional

MODELS = [
    "sentiment-analysis-roberta", "named-entity-recognition-bert", "text-embeddings-minilm",
    "code-generation-codeparrot", "translation-en-es", "question-answering-distilbert",
    "text-summarization-t5", "zero-shot-classification-deberta", "toxic-comment-detection",
    "spam-classification", "language-detection", "emotion-recognition", "intent-classification",
    "keyword-extraction", "text-matching-sentence-transformers", "paraphrase-detection",
    "semantic-search", "document-clustering", "topic-modeling", "relation-extraction",
    "aspect-based-sentiment", "offensive-language-detection", "hate-speech-detection",
    "sarcasm-detection", "humor-detection", "clickbait-detection", "fake-news-detection",
    "fact-checking", "claim-verification", "stance-detection", "argument-mining",
    "contradiction-detection", "natural-language-inference", "textual-entailment",
    "coreference-resolution", "dependency-parsing", "part-of-speech-tagging",
    "morphological-analysis", "lemmatization", "stemming", "tokenization",
    "sentence-splitting", "punctuation-restoration", "grammar-correction",
    "spelling-correction", "text-simplification", "readability-scoring", "text-complexity",
    "essay-scoring", "automated-feedback", "math-word-problems", "symbolic-reasoning",
    "common-sense-reasoning", "logical-fallacy-detection", "cognitive-bias-detection",
    "persuasion-strategy-detection", "propaganda-detection", "misinformation-detection",
    "rumour-detection", "conspiracy-theory-detection", "pseudoscience-detection",
    "medical-ner", "clinical-entity-recognition", "drug-name-recognition",
    "symptom-extraction", "diagnosis-prediction", "treatment-recommendation",
    "biomedical-relation-extraction", "chemical-entity-recognition",
    "protein-structure-prediction", "dna-sequence-analysis", "gene-name-recognition",
    "variant-calling", "mutation-detection", "legal-document-analysis",
    "contract-clause-extraction", "policy-document-summarization",
    "financial-sentiment-analysis", "stock-movement-prediction", "earning-call-analysis",
    "news-impact-analysis", "social-media-monitoring", "brand-sentiment-tracking",
    "customer-feedback-analysis", "product-review-scoring", "complaint-classification",
    "support-ticket-routing", "chat-intent-recognition", "dialogue-act-classification",
    "conversation-summarization", "response-generation", "empathetic-response-generation",
    "persona-based-chat", "role-playing-agent", "instruction-following",
    "tool-using-agent", "multi-turn-dialogue", "knowledge-grounded-response",
    "text-style-transfer", "multilingual-sentiment",
]

SAMPLE_INPUTS = {
    "translation-en-es": "Hello, how are you today?",
    "question-answering-distilbert": "What is machine learning?",
    "text-summarization-t5": "Machine learning is a type of artificial intelligence that allows computers to learn from data without being explicitly programmed. It has applications in many fields including healthcare, finance, and transportation.",
    "code-generation-codeparrot": "def sort_list(items):",
    "grammar-correction": "I are going to the store yestrday.",
    "spelling-correction": "The quik brown fox jumpd over the lazy dog.",
    "math-word-problems": "If John has 5 apples and gives 2 to Mary, how many does he have left?",
    "default": "This is a sample text for testing the model endpoint.",
}


def test_model(base_url: str, model_name: str, timeout: int = 30) -> dict:
    text = SAMPLE_INPUTS.get(model_name, SAMPLE_INPUTS["default"])
    results = {}

    # Test /health
    try:
        r = requests.get(f"{base_url}/health", timeout=timeout)
        results["health"] = {"status": r.status_code, "body": r.json()}
    except Exception as e:
        results["health"] = {"error": str(e)}

    # Test /info
    try:
        r = requests.get(f"{base_url}/info", timeout=timeout)
        results["info"] = {"status": r.status_code, "body": r.json()}
    except Exception as e:
        results["info"] = {"error": str(e)}

    # Test /predict
    try:
        r = requests.post(f"{base_url}/predict", json={"text": text}, timeout=timeout)
        results["predict"] = {"status": r.status_code, "body": r.json()}
    except Exception as e:
        results["predict"] = {"error": str(e)}

    # Test /predict_batch
    try:
        r = requests.post(f"{base_url}/predict_batch",
                          json={"texts": [text, text + " Again."]}, timeout=timeout)
        results["predict_batch"] = {"status": r.status_code, "body": r.json()}
    except Exception as e:
        results["predict_batch"] = {"error": str(e)}

    return results


def main():
    parser = argparse.ArgumentParser(description="Test Elastic-Model-Fleet endpoints")
    parser.add_argument("--base-url", required=True, help="Base URL of the deployed service")
    parser.add_argument("--model", help="Test a specific model folder name only")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout seconds")
    args = parser.parse_args()

    base_url = args.base_url.rstrip("/")
    models_to_test = [args.model] if args.model else MODELS

    passed = 0
    failed = 0

    for model in models_to_test:
        print(f"\n{'='*60}")
        print(f"Testing: {model}")
        print(f"URL: {base_url}")
        results = test_model(base_url, model, args.timeout)

        for endpoint, result in results.items():
            status = result.get("status", "ERR")
            ok = status == 200
            symbol = "✓" if ok else "✗"
            print(f"  {symbol} {endpoint}: {status}")
            if not ok:
                print(f"    → {result}")

        all_ok = all(r.get("status") == 200 for r in results.values())
        if all_ok:
            passed += 1
            print(f"  ✅ PASSED")
        else:
            failed += 1
            print(f"  ❌ FAILED")

    print(f"\n{'='*60}")
    print(f"Results: {passed} passed, {failed} failed out of {len(models_to_test)} models")


if __name__ == "__main__":
    main()
