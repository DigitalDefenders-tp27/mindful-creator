"""Backward‑compat wrapper kept for external callers."""
from .inference import predict_text  # re‑export

__all__ = ["predict_text"]