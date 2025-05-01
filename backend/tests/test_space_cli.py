#!/usr/bin/env python
"""
Space CLI 测试脚本
用于测试与Hugging Face Spaces的连接

运行方式:
python -m backend.tests.test_space_cli
"""

import os
import sys
import logging
import time
from typing import List, Dict, Any

# 设置日志记录
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_space_connection():
    """
    Test Space CLI connection to HuggingFace Spaces
    
    Returns:
        bool: Success or failure
    """
    logger.info("Starting Space CLI connection test...")
    
    try:
        # Import the gradio_client package
        logger.info("Importing gradio_client...")
        from gradio_client import Client
        
        # Test comment data
        test_comments = [
            "G'day mate! Bloody ripper video, loved it!",  # 澳大利亚俚语-正面评论
            "Crikey! This was a shocker. Total rubbish!"   # 澳大利亚俚语-负面评论
        ]
        
        # Create client instance - this is the core of Space CLI
        logger.info("Creating Space client connection...")
        start_time = time.time()
        
        client = Client("https://jet-12138-commentresponse.hf.space/")
        
        connection_time = time.time() - start_time
        logger.info(f"Space client connection established in {connection_time:.2f} seconds")
        
        # Format comments as required by the model
        comments_text = "\n".join(test_comments)
        
        # Make the prediction call
        logger.info("Calling Space predict endpoint...")
        predict_start = time.time()
        
        result = client.predict(
            comments_text,
            api_name="predict"
        )
        
        predict_time = time.time() - predict_start
        logger.info(f"Prediction completed in {predict_time:.2f} seconds")
        
        # Report result type and summary
        logger.info(f"Result type: {type(result)}")
        
        if isinstance(result, dict):
            logger.info(f"Result keys: {list(result.keys())}")
            
            # Check for expected sentiment and toxicity data
            if "sentiment_counts" in result:
                logger.info(f"Sentiment counts: {result['sentiment_counts']}")
            
            if "toxicity_counts" in result:
                logger.info(f"Toxicity counts: {result['toxicity_counts']}")
            
            if "comments_with_any_toxicity" in result:
                logger.info(f"Toxic comments: {result['comments_with_any_toxicity']}")
                
        elif isinstance(result, str):
            # If result is a JSON string, log the first 500 chars
            logger.info(f"Result preview: {result[:500]}...")
        else:
            logger.info(f"Result: {result}")
            
        logger.info("✅ Space CLI connection test successful!")
        return True
        
    except ImportError as ie:
        logger.error(f"❌ Failed to import gradio_client: {str(ie)}")
        logger.error("Please ensure gradio_client is installed: pip install gradio_client>=0.6.1")
        return False
        
    except Exception as e:
        logger.error(f"❌ Space CLI connection test failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False
        
if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("SPACE CLI CONNECTION TEST")
    logger.info("=" * 60)
    
    # Show environment info
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current working directory: {os.getcwd()}")
    
    # Check for HF token
    hf_token = os.environ.get("HF_TOKEN")
    logger.info(f"HF_TOKEN set: {bool(hf_token)}")
    
    # Run the test
    success = test_space_connection()
    
    if success:
        logger.info("✅ Test completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Test failed!")
        sys.exit(1) 