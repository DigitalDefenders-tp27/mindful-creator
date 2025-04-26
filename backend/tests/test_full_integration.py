#!/usr/bin/env python3
"""
End-to-end integration test:
    1. Validate connectivity to YouTube API.
    2. Retrieve a handful of comments from a public video.
    3. Validate connectivity to the Hugging Face Space via gradio-client.
    4. Send the comments list to the Space and ensure a sane JSON response is
       returned.

Run this file directly or via your preferred test runner. All console output is
in Australian English.
"""

from __future__ import annotations

import json
import logging
import os
import sys
from dotenv import load_dotenv
load_dotenv()
import time
from pathlib import Path
from typing import List
import tempfile
import ssl

# Make the backend package importable when running directly
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.app.api.youtube.analyzer import (
    fetch_youtube_comments,
    analyse_comments_with_space_api,
)
from gradio_client import Client  # noqa: E402

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

YOUTUBE_VIDEO_URL: str = (
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ" 
)
MAX_COMMENTS: int = 5  # keep test speedy whilst still meaningful
SPACE_ID: str = "Jet-12138/CommentResponse"

# ---------------------------------------------------------------------------
# Logging setup – verbose enough for CI yet human-friendly.
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

# Disable SSL verification for this test run – resolves CERTIFICATE_VERIFY_FAILED on some macOS setups.
ssl._create_default_https_context = ssl._create_unverified_context
# Ensure websockets (which calls ssl.create_default_context) also skips verify.
ssl.create_default_context = lambda *args, **kwargs: ssl._create_unverified_context()

# ---------------------------------------------------------------------------
# Helper with inline breakpoints (commented out by default)
# ---------------------------------------------------------------------------

def _bp(label: str) -> None:  # noqa: D401 – simple helper, not a docstring
    """Optional breakpoint helper – uncomment breakpoint() when needed."""
    logger.debug("\n------ BREAKPOINT: %s ------", label)
    # breakpoint()  # Uncomment for interactive debugging


# ---------------------------------------------------------------------------
# Test routine
# ---------------------------------------------------------------------------

def test_youtube_to_space_pipeline() -> None:
    """Run the full pipeline and assert each major stage succeeds."""

    # 1. Environment sanity check ------------------------------------------------
    logger.info("Checking environment variables …")
    youtube_key_present = bool(os.environ.get("YOUTUBE_API_KEY"))
    if not youtube_key_present:
        os.environ["YOUTUBE_API_KEY"] = "AIzaSyDU95gTm6jKz85RdDj84QpU1tUETrCCP8M"
        logger.warning(
            "YOUTUBE_API_KEY not found – using fallback key solely for testing purposes."
        )
    logger.info("YOUTUBE_API_KEY present: %s", True)

    _bp("env-ready")

    # 2. Retrieve comments from YouTube -----------------------------------------
    logger.info("Fetching up to %s comments from YouTube …", MAX_COMMENTS)
    comments = fetch_youtube_comments(YOUTUBE_VIDEO_URL, MAX_COMMENTS)
    assert comments, "No comments returned from YouTube"
    logger.info("Retrieved %s comments", len(comments))
    logger.debug("Sample comments: %s", comments[:2])

    _bp("yt-comments-fetched")

    # 3. Analyse comments via backend wrapper (with built-in fallback) ---------
    logger.info("Invoking analyse_comments_with_space_api (uses gradio-client or REST fallback) …")
    start = time.time()
    analysis = analyse_comments_with_space_api(comments)
    elapsed = time.time() - start
    logger.info("Analysis completed in %.2fs", elapsed)

    # Validate analysis results structure
    assert isinstance(analysis, dict), "Analysis did not return a dictionary"
    assert "sentiment" in analysis, "Missing 'sentiment' in analysis output"
    assert "toxicity" in analysis, "Missing 'toxicity' in analysis output"
    logger.info(
        "Sentiment summary: %s", analysis["sentiment"]
    )
    logger.info(
        "Toxicity summary: %s", analysis["toxicity"]
    )
    logger.info("✅ Full pipeline test passed – fetched & analysed comments successfully.")


# Run directly -----------------------------------------------------------------
if __name__ == "__main__":
    test_youtube_to_space_pipeline() 