#!/usr/bin/env python
"""
测试脚本：测试Space API连接
测试使用gradio_client和HTTP请求连接到Space API
"""

import os
import sys
import time
import json
import logging
from typing import List

# 确保项目根目录在Python路径中
proj_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Space URLs
SPACE_PUBLIC_URL = "https://huggingface.co/spaces/Jet-12138/CommentResponse"
SPACE_API_URL = "https://jet-12138-commentresponse.hf.space"

# 测试评论
TEST_COMMENTS = [
    "G'day mate! Brilliant video, absolute ripper content!",
    "So helpful, thanks for sharing these tips!",
    "Crikey! This content is rubbish, total waste of time.",
    "I'm absolutely loving your videos, keep up the good work!",
    "Not sure why anyone would watch this garbage."
]

def test_analyze_function():
    """测试Space分析函数"""
    logger.info("=" * 50)
    logger.info("测试分析函数 (analyse_comments_with_space_api)")
    logger.info("=" * 50)
    
    try:
        # 导入分析函数
        from backend.app.api.youtube.analyzer import analyse_comments_with_space_api
        
        # 运行分析
        logger.info(f"发送 {len(TEST_COMMENTS)} 条评论进行分析")
        start_time = time.time()
        result = analyse_comments_with_space_api(TEST_COMMENTS)
        duration = time.time() - start_time
        
        # 检查结果
        logger.info(f"API调用耗时: {duration:.2f}秒")
        
        if "error" in result:
            logger.error(f"❌ 分析失败: {result['error']}")
            logger.info(f"完整结果: {json.dumps(result, indent=2)}")
            return False
        
        # 检查结果是否包含预期字段
        if "sentiment" in result and "toxicity" in result:
            logger.info("✅ 成功获取分析结果")
            
            # 显示情感分析结果
            sentiment = result["sentiment"]
            logger.info("情感分析结果:")
            logger.info(f"  积极: {sentiment.get('positive_count', 0)}")
            logger.info(f"  中性: {sentiment.get('neutral_count', 0)}")
            logger.info(f"  消极: {sentiment.get('negative_count', 0)}")
            
            # 显示毒性分析结果
            toxicity = result["toxicity"]
            logger.info("毒性分析结果:")
            logger.info(f"  毒性评论总数: {toxicity.get('toxic_count', 0)}")
            logger.info(f"  毒性百分比: {toxicity.get('toxic_percentage', 0):.2f}%")
            
            if result.get("note"):
                logger.info(f"备注: {result['note']}")
                
            return True
        else:
            logger.error("❌ 结果缺少预期的字段")
            logger.info(f"完整结果: {json.dumps(result, indent=2)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ 测试过程中发生异常: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_gradio_client():
    """测试使用gradio_client连接到Space"""
    logger.info("\n" + "=" * 50)
    logger.info("测试gradio_client连接")
    logger.info("=" * 50)
    
    try:
        from gradio_client import Client
        
        # 创建客户端连接
        logger.info(f"尝试连接到 {SPACE_API_URL}")
        start_time = time.time()
        client = Client(SPACE_API_URL)
        connection_time = time.time() - start_time
        
        logger.info(f"✅ 连接成功，耗时: {connection_time:.2f}秒")
        
        # 准备测试数据
        comments_text = "\n".join(TEST_COMMENTS)
        
        # 调用预测
        logger.info("调用predict端点...")
        start_time = time.time()
        result = client.predict(comments_text, api_name="/predict")
        predict_time = time.time() - start_time
        
        logger.info(f"✅ 预测调用成功，耗时: {predict_time:.2f}秒")
        logger.info(f"结果类型: {type(result)}")
        
        if isinstance(result, dict):
            logger.info(f"结果键: {list(result.keys())}")
            
            if "sentiment_counts" in result:
                logger.info(f"情感统计: {result['sentiment_counts']}")
            
            if "toxicity_counts" in result:
                logger.info(f"毒性统计: {result['toxicity_counts']}")
        
        return True
        
    except ImportError:
        logger.error("❌ gradio_client库未安装")
        return False
    except Exception as e:
        logger.error(f"❌ gradio_client测试失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_http_request():
    """测试使用HTTP请求连接到Space"""
    logger.info("\n" + "=" * 50)
    logger.info("测试HTTP请求连接")
    logger.info("=" * 50)
    
    try:
        import requests
        
        # 尝试不同的API端点
        api_endpoints = [
            "/api/predict",
            "/predict"
        ]
        
        # 准备测试数据
        comments_text = "\n".join(TEST_COMMENTS)
        
        # 尝试每个端点
        for endpoint in api_endpoints:
            api_url = f"{SPACE_API_URL}{endpoint}"
            logger.info(f"尝试连接到: {api_url}")
            
            # 准备请求
            headers = {"Content-Type": "application/json"}
            payload = {"data": [comments_text]}
            
            # 发送请求
            try:
                start_time = time.time()
                response = requests.post(
                    api_url,
                    json=payload,
                    headers=headers,
                    timeout=60
                )
                duration = time.time() - start_time
                
                logger.info(f"状态码: {response.status_code}, 耗时: {duration:.2f}秒")
                
                if response.status_code == 200:
                    logger.info("✅ HTTP请求成功!")
                    
                    # 解析响应
                    try:
                        result = response.json()
                        logger.info(f"响应类型: {type(result)}")
                        
                        # 处理不同的响应格式
                        if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
                            result = result["data"][0]
                        
                        if isinstance(result, dict):
                            logger.info(f"结果键: {list(result.keys())}")
                            
                            if "sentiment_counts" in result:
                                logger.info(f"情感统计: {result['sentiment_counts']}")
                            
                            if "toxicity_counts" in result:
                                logger.info(f"毒性统计: {result['toxicity_counts']}")
                        
                        return True
                        
                    except Exception as parse_err:
                        logger.error(f"❌ 无法解析响应: {str(parse_err)}")
                        
                else:
                    logger.warning(f"❌ HTTP请求失败: {response.status_code}")
                    if response.text:
                        logger.info(f"响应内容: {response.text[:200]}...")
                        
            except Exception as req_err:
                logger.error(f"❌ 请求异常: {str(req_err)}")
        
        logger.error("❌ 所有HTTP端点都失败")
        return False
        
    except ImportError:
        logger.error("❌ requests库未安装")
        return False
    except Exception as e:
        logger.error(f"❌ HTTP请求测试失败: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("开始Space API连接测试")
    
    # 设置环境变量
    os.environ["GRADIO_CLIENT_TEMP_DIR"] = "/tmp/gradio_client_cache"
    os.environ["GRADIO_CLIENT_REQUEST_TIMEOUT"] = "60"
    
    # 运行测试
    test_results = {
        "分析函数": test_analyze_function(),
        "Gradio客户端": test_gradio_client(),
        "HTTP请求": test_http_request()
    }
    
    # 输出结果摘要
    logger.info("\n" + "=" * 50)
    logger.info("测试结果摘要")
    logger.info("=" * 50)
    
    for test_name, success in test_results.items():
        logger.info(f"{test_name}: {'✅ 成功' if success else '❌ 失败'}")
    
    # 决定退出码
    all_success = all(test_results.values())
    if all_success:
        logger.info("🎉 所有测试均成功!")
        sys.exit(0)
    else:
        logger.error("❌ 部分测试失败")
        sys.exit(1) 