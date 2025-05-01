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
        
        # 列出可用的API端点
        logger.info("Available API endpoints:")
        try:
            # 检查endpoints的类型
            logger.info(f"Endpoints type: {type(client.endpoints)}")
            
            if hasattr(client.endpoints, "__iter__") and not isinstance(client.endpoints, str):
                for i, api in enumerate(client.endpoints):
                    logger.info(f"  Endpoint #{i} type: {type(api)}")
            else:
                logger.info("  No iterable endpoints available")
        except Exception as e:
            logger.warning(f"Failed to enumerate endpoints: {str(e)}")
        
        # Format comments as required by the model
        comments_text = "\n".join(test_comments)
        
        # 测试所有可能的fn_index值
        success = False
        
        for fn_idx in range(5):  # 尝试前5个函数索引
            logger.info(f"Testing with fn_index={fn_idx}...")
            try:
                # 尝试使用当前函数索引
                predict_start = time.time()
                result = client.predict(
                    comments_text,
                    fn_index=fn_idx
                )
                predict_time = time.time() - predict_start
                
                logger.info(f"Prediction with fn_index={fn_idx} completed in {predict_time:.2f} seconds")
                logger.info(f"Result type: {type(result)}")
                
                # 检查结果是否是预期的格式
                is_valid_result = False
                
                if isinstance(result, dict):
                    logger.info(f"Result keys: {list(result.keys())}")
                    
                    # 检查是否包含关键字段
                    if any(key in result for key in ["sentiment_counts", "toxicity_counts", "comments_with_any_toxicity"]):
                        logger.info(f"Found valid result with fn_index={fn_idx}")
                        is_valid_result = True
                        
                        # 保存正确的函数索引
                        success = True
                        correct_fn_index = fn_idx
                        
                        # 记录详细信息
                        if "sentiment_counts" in result:
                            logger.info(f"Sentiment counts: {result['sentiment_counts']}")
                        
                        if "toxicity_counts" in result:
                            logger.info(f"Toxicity counts: {result['toxicity_counts']}")
                        
                        if "comments_with_any_toxicity" in result:
                            logger.info(f"Toxic comments: {result['comments_with_any_toxicity']}")
                        
                        # 找到有效结果后跳出循环
                        break
                
                if not is_valid_result:
                    logger.warning(f"fn_index={fn_idx} returned unexpected result format")
                
            except Exception as e:
                logger.warning(f"fn_index={fn_idx} failed: {str(e)}")
        
        if success:
            logger.info(f"✅ Found working endpoint with fn_index={correct_fn_index}")
            logger.info("✅ Space CLI connection test successful!")
            return True
        else:
            logger.error("❌ Could not find a working endpoint in the Space API")
            return False
        
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