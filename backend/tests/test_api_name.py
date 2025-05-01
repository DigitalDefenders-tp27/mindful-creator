#!/usr/bin/env python
"""
Space API名称测试脚本
专门测试使用api_name="/predict"与Hugging Face Spaces的连接

运行方式:
python -m backend.tests.test_api_name
"""

import os
import sys
import logging
import time
import json

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_api_name():
    """测试api_name='/predict'是否能正确连接到Space API"""
    try:
        from gradio_client import Client
        
        space_url = "https://jet-12138-commentresponse.hf.space/"
        logger.info(f"Connecting to Space: {space_url}")
        
        client = Client(space_url)
        logger.info("Connected successfully!")
        
        # 测试评论数据
        test_comments = [
            "G'day mate! Bloody ripper video, loved it!",  # 澳大利亚俚语-正面评论
            "Crikey! This was a shocker. Total rubbish!"   # 澳大利亚俚语-负面评论
        ]
        
        # 格式化评论文本
        comments_text = "\n".join(test_comments)
        
        # 尝试使用api_name="/predict"
        logger.info("=" * 50)
        logger.info("TESTING WITH api_name='/predict'")
        logger.info("=" * 50)
        
        try:
            logger.info("Calling predict with api_name='/predict'...")
            start_time = time.time()
            
            # 使用前导斜杠的API名称
            result = client.predict(
                comments_text,
                api_name="/predict"
            )
            
            duration = time.time() - start_time
            logger.info(f"Call completed in {duration:.2f} seconds")
            
            # 分析结果
            logger.info(f"Result type: {type(result)}")
            
            if isinstance(result, dict):
                logger.info(f"Result keys: {list(result.keys())}")
                
                # 检查关键字段
                for key in ["sentiment_counts", "toxicity_counts", "comments_with_any_toxicity"]:
                    if key in result:
                        logger.info(f"{key}: {result[key]}")
                
                # 打印完整结果（有限长度）
                logger.info(f"Complete result: {json.dumps(result, indent=2)[:1000]}...")
                
                logger.info("✅ API call with api_name='/predict' successful!")
                return True
            else:
                logger.warning(f"Unexpected result type: {type(result)}")
                logger.warning(f"Result content: {str(result)[:500]}...")
                return False
                
        except Exception as e:
            logger.error(f"❌ API call with api_name='/predict' failed: {str(e)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ Test failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("SPACE API NAME TEST")
    logger.info("=" * 60)
    
    # 环境信息
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"HF_TOKEN set: {bool(os.environ.get('HF_TOKEN'))}")
    logger.info(f"GRADIO_CLIENT_TEMP_DIR: {os.environ.get('GRADIO_CLIENT_TEMP_DIR', 'Not set')}")
    
    # 运行测试
    success = test_api_name()
    
    if success:
        logger.info("✅ Test completed successfully!")
        sys.exit(0)
    else:
        logger.error("❌ Test failed!")
        sys.exit(1) 