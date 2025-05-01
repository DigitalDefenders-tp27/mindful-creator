#!/usr/bin/env python
"""
测试脚本：检查Gradio Space API可用的端点
"""

import os
import sys
import time
import json
import logging

# 确保项目根目录在Python路径中
proj_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Space URL
SPACE_URL = "https://jet-12138-commentresponse.hf.space"

# 测试数据
TEST_COMMENTS = [
    "G'day mate! Brilliant video, absolute ripper content!",
    "So helpful, thanks for sharing these tips!",
    "Crikey! This content is rubbish, total waste of time.",
    "I'm absolutely loving your videos, keep up the good work!",
    "Not sure why anyone would watch this garbage."
]

def test_gradio_client_endpoints():
    """使用gradio_client检查可用端点"""
    logger.info("=" * 50)
    logger.info("测试gradio_client可用端点")
    logger.info("=" * 50)
    
    try:
        # 导入gradio_client
        from gradio_client import Client
        
        # 创建客户端连接
        logger.info(f"尝试连接到 {SPACE_URL}")
        start_time = time.time()
        client = Client(SPACE_URL)
        duration = time.time() - start_time
        
        logger.info(f"✅ 连接成功，耗时: {duration:.2f}秒")
        
        # 检查和记录端点信息
        if hasattr(client, "endpoints"):
            endpoints = client.endpoints
            logger.info(f"端点类型: {type(endpoints)}")
            if isinstance(endpoints, (list, tuple)):
                logger.info(f"可用端点数量: {len(endpoints)}")
                for i, endpoint in enumerate(endpoints):
                    logger.info(f"端点 {i+1}: {endpoint}")
            else:
                logger.info(f"端点值: {endpoints}")
                
        # 尝试另一种方法获取端点
        try:
            endpoint_info = client.predict_api_info()
            logger.info("API信息:")
            logger.info(json.dumps(endpoint_info, indent=2))
        except Exception as api_err:
            logger.warning(f"无法获取predict_api_info: {str(api_err)}")
            
        # 尝试使用不同的API名称调用预测
        comments_text = "\n".join(TEST_COMMENTS)
        
        logger.info("\n尝试不同的API名称:")
        api_names = [
            None,       # 默认API（一般是第一个）
            "",         # 空字符串
            "/",        # 斜杠
            "/predict", # 带斜杠
            "predict"   # 不带斜杠
        ]
        
        for api_name in api_names:
            api_display = api_name if api_name is not None else "默认API (None)"
            logger.info(f"\n尝试API名称: {api_display}")
            
            try:
                start_time = time.time()
                if api_name is None:
                    result = client.predict(comments_text)
                else:
                    result = client.predict(comments_text, api_name=api_name)
                    
                duration = time.time() - start_time
                
                logger.info(f"✅ 调用成功! 耗时: {duration:.2f}秒")
                logger.info(f"结果类型: {type(result)}")
                
                if isinstance(result, dict):
                    logger.info(f"结果键: {list(result.keys())}")
                    
                    if "sentiment_counts" in result:
                        logger.info(f"情感统计: {result['sentiment_counts']}")
                    
                    if "toxicity_counts" in result:
                        logger.info(f"毒性统计: {result['toxicity_counts']}")
                        
                elif isinstance(result, str):
                    preview = result[:100] + "..." if len(result) > 100 else result
                    logger.info(f"字符串结果预览: {preview}")
                    
                    # 尝试解析JSON
                    try:
                        json_result = json.loads(result)
                        logger.info(f"解析为JSON后的键: {list(json_result.keys())}")
                    except:
                        logger.info("非JSON字符串")
            
            except Exception as pred_err:
                logger.error(f"❌ 使用API名称 '{api_display}' 调用失败: {str(pred_err)}")
                
        return True
    
    except ImportError:
        logger.error("❌ gradio_client库未安装")
        return False
    except Exception as e:
        logger.error(f"❌ 测试过程中发生异常: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("开始检查Gradio Space API端点")
    
    # 指定缓存目录
    os.environ["GRADIO_CLIENT_TEMP_DIR"] = "/tmp/gradio_client_cache"
    
    # 设置超时
    os.environ["GRADIO_CLIENT_REQUEST_TIMEOUT"] = "60"
    
    result = test_gradio_client_endpoints()
    
    if result:
        logger.info("🎉 测试完成，至少有一个端点可用!")
        sys.exit(0)
    else:
        logger.error("❌ 测试失败，无法获取有效端点")
        sys.exit(1) 