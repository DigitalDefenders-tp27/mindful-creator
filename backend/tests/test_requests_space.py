#!/usr/bin/env python
"""
测试脚本：尝试使用requests库连接Space API
尝试各种可能的API端点和请求格式
"""

import os
import sys
import time
import json
import logging
import traceback
from typing import List, Dict, Any, Optional

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

def get_gradio_api_info():
    """
    获取Gradio API信息
    尝试获取Gradio API配置，以便了解可用的端点
    """
    import requests
    
    logger.info("获取Gradio API信息")
    
    # 尝试获取config信息
    try:
        config_url = f"{SPACE_API_URL}/config"
        logger.info(f"请求配置信息: {config_url}")
        
        response = requests.get(config_url, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ 成功获取配置信息")
            config_data = response.json()
            logger.info(f"配置信息键: {list(config_data.keys())}")
            
            # 打印一些有用的配置信息
            if "version" in config_data:
                logger.info(f"Gradio版本: {config_data.get('version')}")
            
            if "dev_mode" in config_data:
                logger.info(f"开发模式: {config_data.get('dev_mode')}")
                
            if "components" in config_data:
                components = config_data.get("components", [])
                logger.info(f"组件数量: {len(components)}")
                
                # 查看组件信息
                for i, comp in enumerate(components):
                    if isinstance(comp, dict):
                        comp_id = comp.get("id")
                        comp_type = comp.get("type")
                        logger.info(f"组件 {i}: ID={comp_id}, 类型={comp_type}")
        else:
            logger.warning(f"❌ 获取配置失败: {response.status_code}")
    except Exception as e:
        logger.error(f"获取配置异常: {str(e)}")
    
    # 尝试获取API信息
    try:
        api_url = f"{SPACE_API_URL}/gradio_api/info?serialize=False"
        logger.info(f"请求API信息: {api_url}")
        
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ 成功获取API信息")
            api_data = response.json()
            
            logger.info(f"API信息键: {list(api_data.keys()) if isinstance(api_data, dict) else 'Not a dict'}")
            
            try:
                # 提取API端点信息
                if "endpoints" in api_data:
                    endpoints = api_data.get("endpoints", [])
                    logger.info(f"端点数量: {len(endpoints)}")
                    
                    for i, endpoint in enumerate(endpoints):
                        if isinstance(endpoint, dict):
                            endpoint_name = endpoint.get("name")
                            endpoint_fn_index = endpoint.get("fn_index")
                            endpoint_inputs = endpoint.get("inputs")
                            logger.info(f"端点 {i}: 名称={endpoint_name}, fn_index={endpoint_fn_index}, 输入数量={len(endpoint_inputs) if endpoint_inputs else 0}")
            except Exception as parse_err:
                logger.error(f"解析API信息异常: {str(parse_err)}")
        else:
            logger.warning(f"❌ 获取API信息失败: {response.status_code}")
    except Exception as e:
        logger.error(f"获取API信息异常: {str(e)}")
    
    return None

def try_standard_request(endpoint: str, comments: List[str]) -> bool:
    """
    尝试标准的REST请求
    
    Args:
        endpoint: API端点
        comments: 评论列表
        
    Returns:
        是否成功
    """
    import requests
    
    logger.info(f"尝试标准REST请求: {endpoint}")
    
    # 准备评论数据
    comments_text = "\n".join(comments)
    
    # 准备请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    # 准备请求体
    payload = {
        "data": [comments_text]
    }
    
    # 发送请求
    url = f"{SPACE_API_URL}{endpoint}"
    logger.info(f"发送请求到: {url}")
    logger.info(f"请求体: {json.dumps(payload)}")
    
    try:
        start_time = time.time()
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )
        duration = time.time() - start_time
        
        logger.info(f"状态码: {response.status_code}, 耗时: {duration:.2f}秒")
        
        if response.status_code == 200:
            logger.info("✅ 请求成功!")
            
            # 解析响应
            try:
                result = response.json()
                logger.info(f"响应类型: {type(result)}")
                logger.info(f"响应内容: {json.dumps(result)[:200]}...")
                
                if isinstance(result, dict):
                    logger.info(f"响应键: {list(result.keys())}")
                    
                    # 如果有data字段，提取数据
                    if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
                        data = result["data"][0]
                        logger.info(f"提取的数据类型: {type(data)}")
                        
                        if isinstance(data, dict):
                            logger.info(f"数据键: {list(data.keys())}")
                
                return True
            except Exception as parse_err:
                logger.error(f"解析响应异常: {str(parse_err)}")
                logger.info(f"原始响应内容: {response.text[:200]}...")
        else:
            logger.warning(f"❌ 请求失败: {response.status_code}")
            logger.info(f"响应内容: {response.text[:200]}...")
            
        return False
    except Exception as e:
        logger.error(f"请求异常: {str(e)}")
        return False

def try_queue_request(fn_index: int, comments: List[str]) -> bool:
    """
    尝试队列请求（模拟gradio_client的请求方式）
    
    Args:
        fn_index: 函数索引
        comments: 评论列表
        
    Returns:
        是否成功
    """
    import requests
    import uuid
    
    logger.info(f"尝试队列请求: fn_index={fn_index}")
    
    # 准备评论数据
    comments_text = "\n".join(comments)
    
    # 创建会话ID
    session_hash = str(uuid.uuid4())
    logger.info(f"会话ID: {session_hash}")
    
    # 准备请求头
    headers = {
        "Content-Type": "application/json"
    }
    
    # 准备请求体
    payload = {
        "fn_index": fn_index,
        "data": [comments_text],
        "session_hash": session_hash
    }
    
    # 发送加入队列请求
    join_url = f"{SPACE_API_URL}/gradio_api/queue/join"
    logger.info(f"发送加入队列请求到: {join_url}")
    
    try:
        start_time = time.time()
        join_response = requests.post(
            join_url,
            json=payload,
            headers=headers,
            timeout=10
        )
        join_duration = time.time() - start_time
        
        logger.info(f"加入队列状态码: {join_response.status_code}, 耗时: {join_duration:.2f}秒")
        
        if join_response.status_code != 200:
            logger.warning(f"❌ 加入队列失败: {join_response.status_code}")
            logger.info(f"响应内容: {join_response.text[:200]}...")
            return False
            
        # 解析加入队列响应
        join_data = join_response.json()
        logger.info(f"加入队列响应: {json.dumps(join_data)[:200]}...")
        
        # 获取数据（轮询）
        data_url = f"{SPACE_API_URL}/gradio_api/queue/data?session_hash={session_hash}"
        logger.info(f"获取数据请求到: {data_url}")
        
        # 最多尝试10次，每次等待1秒
        for i in range(10):
            logger.info(f"第 {i+1} 次轮询...")
            
            try:
                data_response = requests.get(
                    data_url,
                    headers=headers,
                    timeout=10
                )
                
                logger.info(f"获取数据状态码: {data_response.status_code}")
                
                if data_response.status_code == 200:
                    data = data_response.json()
                    logger.info(f"数据响应: {json.dumps(data)[:200]}...")
                    
                    # 检查状态
                    if data and "status" in data:
                        status = data["status"]
                        logger.info(f"状态: {status}")
                        
                        # 如果已完成，获取结果
                        if status == "complete" and "data" in data:
                            result = data["data"]
                            logger.info(f"结果类型: {type(result)}")
                            
                            if isinstance(result, list) and len(result) > 0:
                                result_data = result[0]
                                logger.info(f"结果数据类型: {type(result_data)}")
                                
                                if isinstance(result_data, dict):
                                    logger.info(f"结果数据键: {list(result_data.keys())}")
                                    
                                    # 检查是否有关键字段
                                    if "sentiment_counts" in result_data:
                                        logger.info(f"情感统计: {result_data['sentiment_counts']}")
                                        
                                    if "toxicity_counts" in result_data:
                                        logger.info(f"毒性统计: {result_data['toxicity_counts']}")
                                
                                return True
                # 等待1秒再轮询
                time.sleep(1)
            except Exception as poll_err:
                logger.error(f"轮询异常: {str(poll_err)}")
                break
                
        logger.warning("❌ 轮询超时，未能获取结果")
        return False
    except Exception as e:
        logger.error(f"请求异常: {str(e)}")
        return False

def try_all_methods():
    """
    尝试所有可能的请求方法
    """
    # 获取API信息
    get_gradio_api_info()
    
    # 尝试各种标准REST端点
    standard_endpoints = [
        "/api/predict",
        "/predict",
        "/run/predict",
        "/gradio/predict",
        "/gradio_api/predict"
    ]
    
    for endpoint in standard_endpoints:
        logger.info("\n" + "=" * 50)
        logger.info(f"测试标准REST端点: {endpoint}")
        logger.info("=" * 50)
        
        success = try_standard_request(endpoint, TEST_COMMENTS)
        logger.info(f"标准REST请求 {endpoint}: {'✅ 成功' if success else '❌ 失败'}")
    
    # 尝试队列请求（模拟gradio_client）
    fn_indexes = [0, 1, 2, 3, 4]  # 尝试不同的函数索引
    
    for index in fn_indexes:
        logger.info("\n" + "=" * 50)
        logger.info(f"测试队列请求: fn_index={index}")
        logger.info("=" * 50)
        
        success = try_queue_request(index, TEST_COMMENTS)
        logger.info(f"队列请求 fn_index={index}: {'✅ 成功' if success else '❌ 失败'}")

if __name__ == "__main__":
    logger.info("开始使用requests库测试Space API")
    
    try:
        # 确保已安装requests库
        import requests
        
        # 尝试所有方法
        try_all_methods()
        
        logger.info("\n🎉 测试完成")
    except ImportError:
        logger.error("❌ 未安装requests库，请先安装: pip install requests")
        sys.exit(1)
    except Exception as e:
        logger.error(f"❌ 测试过程中发生异常: {str(e)}")
        traceback.print_exc()
        sys.exit(1) 