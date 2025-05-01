#!/usr/bin/env python
"""
Space API HTTP 连接测试脚本
测试直接HTTP方式连接到Space API

运行方式:
python -m backend.tests.test_http_space
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

# 测试评论
TEST_COMMENTS = [
    "G'day mate! Brilliant video, absolute ripper content!",
    "So helpful, thanks for sharing these tips!",
    "Crikey! This content is rubbish, total waste of time.",
    "I'm absolutely loving your videos, keep up the good work!",
    "Not sure why anyone would watch this garbage."
]

def run_direct_http_test():
    """使用直接HTTP请求测试与Space API的连接"""
    logger.info("=" * 50)
    logger.info("测试直接HTTP连接到Space API")
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

def run_manual_http_test():
    """手动使用requests库测试Space API"""
    logger.info("=" * 50)
    logger.info("使用requests库手动测试Space API")
    logger.info("=" * 50)
    
    try:
        import requests
        
        # 准备请求
        space_url = "https://jet-12138-commentresponse.hf.space"
        api_endpoints = [
            "/api/predict",
            "/run/predict",
            "/predict"
        ]
        
        # 准备评论数据
        comments_text = "\n".join(TEST_COMMENTS)
        
        # 尝试每个端点
        for endpoint in api_endpoints:
            api_url = f"{space_url}{endpoint}"
            logger.info(f"尝试连接到: {api_url}")
            
            # 准备请求数据
            if "/api/" in endpoint:
                payload = {"data": [comments_text]}
            else:
                payload = {"data": [comments_text]}
                
            headers = {"Content-Type": "application/json"}
            
            # 发送请求
            start_time = time.time()
            try:
                response = requests.post(
                    api_url,
                    json=payload,
                    headers=headers,
                    timeout=60
                )
                duration = time.time() - start_time
                
                logger.info(f"状态码: {response.status_code}, 耗时: {duration:.2f}秒")
                
                if response.status_code == 200:
                    logger.info("✅ 请求成功")
                    try:
                        result = response.json()
                        logger.info(f"响应类型: {type(result)}")
                        
                        # 处理不同的响应格式
                        if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
                            data = result["data"][0]
                            logger.info("从data字段提取结果")
                        else:
                            data = result
                            
                        # 检查结果中的关键字段
                        if "sentiment_counts" in data:
                            logger.info(f"情感统计: {data['sentiment_counts']}")
                        if "toxicity_counts" in data:
                            logger.info(f"毒性统计: {data['toxicity_counts']}")
                        if "comments_with_any_toxicity" in data:
                            logger.info(f"有毒性的评论数: {data['comments_with_any_toxicity']}")
                            
                        logger.info(f"✅ 端点 {endpoint} 测试成功")
                        return True
                    except Exception as parse_err:
                        logger.error(f"❌ 无法解析响应: {str(parse_err)}")
                        logger.info(f"原始响应: {response.text[:500]}...")
                else:
                    logger.warning(f"❌ 请求失败: {response.status_code}")
                    logger.info(f"响应内容: {response.text[:500]}...")
            except Exception as req_err:
                logger.error(f"❌ 请求异常: {str(req_err)}")
                
        logger.error("❌ 所有端点测试失败")
        return False
        
    except ImportError:
        logger.error("❌ 未安装requests库")
        return False
    except Exception as e:
        logger.error(f"❌ 测试过程中发生异常: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("开始Space API HTTP连接测试")
    
    # 测试1: 使用我们的函数进行测试
    logger.info("\n运行集成函数测试...")
    integrated_test_result = run_direct_http_test()
    
    # 测试2: 手动HTTP请求测试
    logger.info("\n运行手动HTTP请求测试...")
    manual_test_result = run_manual_http_test()
    
    # 输出结果
    logger.info("\n=" * 50)
    logger.info("测试结果摘要")
    logger.info("=" * 50)
    logger.info(f"集成函数测试: {'✅ 成功' if integrated_test_result else '❌ 失败'}")
    logger.info(f"手动HTTP请求测试: {'✅ 成功' if manual_test_result else '❌ 失败'}")
    
    if integrated_test_result and manual_test_result:
        logger.info("🎉 两项测试均成功，HTTP连接方式正常工作!")
        sys.exit(0)
    else:
        logger.error("❌ 部分或全部测试失败")
        sys.exit(1) 