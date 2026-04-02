"""
client.py — Universal Python client for any Elastic-Model-Fleet API.

Usage:
    from client import ModelClient

    client = ModelClient("https://sentiment-analysis-roberta.onrender.com")
    result = client.predict("This is amazing!")
    print(result)
"""

import requests
from typing import List, Optional, Dict, Any, Union


class ModelClient:
    """
    Universal client for any Elastic-Model-Fleet model API.
    
    Args:
        base_url: The base URL of your deployed Render service
        timeout: Request timeout in seconds (default: 60)
    """
    
    def __init__(self, base_url: str, timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    def predict(self, text: str, parameters: Optional[Dict[str, Any]] = None) -> Dict:
        """
        Run a single prediction.
        
        Args:
            text: Input text
            parameters: Optional model parameters
            
        Returns:
            dict with 'result' key containing model output
            
        Example:
            >>> client = ModelClient("https://my-service.onrender.com")
            >>> client.predict("Hello world")
            {'result': [{'label': 'POSITIVE', 'score': 0.98}]}
        """
        payload = {"text": text, "parameters": parameters or {}}
        response = self.session.post(
            f"{self.base_url}/predict",
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def predict_batch(self, texts: List[str], parameters: Optional[Dict[str, Any]] = None) -> Dict:
        """
        Run batch predictions.
        
        Args:
            texts: List of input texts
            parameters: Optional model parameters
            
        Returns:
            dict with 'results' key containing list of model outputs
            
        Example:
            >>> client.predict_batch(["Hello", "Goodbye"])
            {'results': [[{'label': 'POSITIVE', 'score': 0.98}], ...]}
        """
        payload = {"texts": texts, "parameters": parameters or {}}
        response = self.session.post(
            f"{self.base_url}/predict_batch",
            json=payload,
            timeout=self.timeout
        )
        response.raise_for_status()
        return response.json()

    def health(self) -> Dict:
        """Check if the model is healthy and loaded."""
        response = self.session.get(f"{self.base_url}/health", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def info(self) -> Dict:
        """Get model metadata."""
        response = self.session.get(f"{self.base_url}/info", timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def wait_until_ready(self, max_wait: int = 300, poll_interval: int = 5) -> bool:
        """
        Poll the health endpoint until the model is loaded.
        Useful right after deployment when the model is still downloading.
        
        Args:
            max_wait: Maximum seconds to wait (default: 300)
            poll_interval: Seconds between checks (default: 5)
            
        Returns:
            True if model loaded, False if timed out
        """
        import time
        waited = 0
        while waited < max_wait:
            try:
                health = self.health()
                if health.get("model_loaded"):
                    print(f"Model ready after {waited}s")
                    return True
                print(f"Waiting for model... ({waited}s)")
            except Exception as e:
                print(f"Not reachable yet ({waited}s): {e}")
            time.sleep(poll_interval)
            waited += poll_interval
        print(f"Timed out after {max_wait}s")
        return False


class MultiModelClient:
    """
    Client that manages multiple deployed model endpoints.
    
    Example:
        >>> fleet = MultiModelClient({
        ...     "sentiment": "https://sentiment.onrender.com",
        ...     "ner": "https://ner.onrender.com",
        ... })
        >>> fleet["sentiment"].predict("I love this!")
    """
    
    def __init__(self, endpoints: Dict[str, str], timeout: int = 60):
        self.clients = {
            name: ModelClient(url, timeout=timeout)
            for name, url in endpoints.items()
        }

    def __getitem__(self, model_name: str) -> ModelClient:
        return self.clients[model_name]

    def health_check_all(self) -> Dict[str, bool]:
        """Check health of all registered models."""
        results = {}
        for name, client in self.clients.items():
            try:
                h = client.health()
                results[name] = h.get("model_loaded", False)
            except Exception:
                results[name] = False
        return results


# ─── Example usage ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Single model
    print("=== Single Model Example ===")
    client = ModelClient("https://sentiment-analysis-roberta.onrender.com")

    print("Health:", client.health())
    print("Info:", client.info())
    result = client.predict("This framework is absolutely incredible!")
    print("Prediction:", result)

    batch = client.predict_batch([
        "I love this product",
        "This is terrible",
        "It's okay I guess"
    ])
    print("Batch:", batch)

    # Multi-model fleet
    print("\n=== Multi-Model Fleet Example ===")
    fleet = MultiModelClient({
        "sentiment": "https://sentiment-analysis-roberta.onrender.com",
        "ner": "https://named-entity-recognition-bert.onrender.com",
        "summarizer": "https://text-summarization-t5.onrender.com",
    })

    health = fleet.health_check_all()
    print("Fleet health:", health)

    # Use individual models
    # sentiment = fleet["sentiment"].predict("Great day today!")
    # ner = fleet["ner"].predict("Apple was founded by Steve Jobs.")
