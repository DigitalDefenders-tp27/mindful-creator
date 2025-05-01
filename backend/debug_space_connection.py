#!/usr/bin/env python
"""
Space 连接调试工具
此脚本列出所有可用的Space API端点并测试基本连接

运行方式:
python -m backend.debug_space_connection
"""

import os
import sys
import json
import logging

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def debug_space_connection():
    """查看Space API详细信息"""
    try:
        from gradio_client import Client
        
        space_url = "https://jet-12138-commentresponse.hf.space/"
        logger.info(f"Connecting to Space: {space_url}")
        
        client = Client(space_url)
        logger.info("Connected successfully!")
        
        # 显示所有可用端点
        logger.info("=" * 50)
        logger.info("AVAILABLE API ENDPOINTS:")
        logger.info("=" * 50)
        
        try:
            # 检查endpoints的类型和结构
            logger.info(f"Endpoints type: {type(client.endpoints)}")
            
            # 如果是字典、列表或其他可迭代对象
            if hasattr(client.endpoints, "__iter__") and not isinstance(client.endpoints, str):
                for i, endpoint in enumerate(client.endpoints):
                    logger.info(f"Endpoint #{i} type: {type(endpoint)}")
                    # 尝试不同的属性访问方式
                    if hasattr(endpoint, "name"):
                        logger.info(f"  Name: {endpoint.name}")
                    if hasattr(endpoint, "description"):
                        logger.info(f"  Description: {endpoint.description}")
                    if hasattr(endpoint, "input_types"):
                        logger.info(f"  Input types: {endpoint.input_types}")
                    # 如果是字典，直接访问键
                    if isinstance(endpoint, dict):
                        logger.info(f"  Dict keys: {list(endpoint.keys())}")
                        for key, value in endpoint.items():
                            logger.info(f"  {key}: {value}")
                    logger.info("  --")
            else:
                # 单个端点情况
                logger.info(f"Client has a single endpoint, value: {client.endpoints}")
                
            # 显示API信息
            if hasattr(client, "api_info"):
                logger.info("API Info:")
                logger.info(f"{client.api_info}")
                
        except Exception as endpoints_err:
            logger.error(f"Error inspecting endpoints: {str(endpoints_err)}")
        
        # 获取第一个端点的完整信息（使用更安全的方式）
        try:
            logger.info("=" * 50)
            logger.info("FIRST ENDPOINT DETAILS:")
            logger.info("=" * 50)
            
            if hasattr(client, "endpoints") and client.endpoints:
                # 尝试安全地访问第一个端点
                first_endpoint = client.endpoints[0] if isinstance(client.endpoints, list) else client.endpoints
                
                logger.info(f"First endpoint type: {type(first_endpoint)}")
                
                # 尝试提取端点信息
                if hasattr(first_endpoint, "name"):
                    logger.info(f"API Name: {first_endpoint.name}")
                if hasattr(first_endpoint, "api_path"):
                    logger.info(f"API Path: {first_endpoint.api_path}")
                
                # 显示client信息
                if hasattr(client, "root_url"):
                    logger.info(f"Root URL: {client.root_url}")
                if hasattr(client, "session_hash"):
                    logger.info(f"Session Hash: {client.session_hash}")
                
            # 测试基本调用
            logger.info("=" * 50)
            logger.info("TESTING CALL WITH fn_index=2 (KNOWN WORKING ENDPOINT)")
            logger.info("=" * 50)
            
            sample_comment = "G'day mate! Testing the connection."
            logger.info(f"Input: '{sample_comment}'")
            
            try:
                # 使用已知的工作端点
                logger.info("Calling predict with fn_index=2...")
                result = client.predict(sample_comment, fn_index=2)
                
                logger.info(f"Result type: {type(result)}")
                
                # 根据结果类型显示详情
                if isinstance(result, dict):
                    logger.info(f"Result dict keys: {list(result.keys())}")
                    
                    # 检查关键字段
                    if "sentiment_counts" in result:
                        logger.info(f"Sentiment counts: {result['sentiment_counts']}")
                    
                    if "toxicity_counts" in result:
                        logger.info(f"Toxicity counts: {result['toxicity_counts']}")
                    
                    if "comments_with_any_toxicity" in result:
                        logger.info(f"Toxic comments: {result['comments_with_any_toxicity']}")
                    
                    # 打印部分结果
                    logger.info(json.dumps(result, indent=2)[:1000] + "...")
                else:
                    logger.info(f"Result: {str(result)[:1000]}...")
                    
                logger.info("✅ Test call successful!")
                
            except Exception as call_err:
                logger.error(f"❌ Test call failed: {str(call_err)}")
                
        except Exception as endpoint_err:
            logger.error(f"Error accessing endpoint details: {str(endpoint_err)}")
                
        return True
        
    except Exception as e:
        logger.error(f"Debug failed: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return False

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("SPACE CONNECTION DEBUGGER")
    logger.info("=" * 60)
    
    # 环境信息
    logger.info(f"Python version: {sys.version}")
    logger.info(f"Current working directory: {os.getcwd()}")
    logger.info(f"HF_TOKEN set: {bool(os.environ.get('HF_TOKEN'))}")
    logger.info(f"GRADIO_CLIENT_TEMP_DIR: {os.environ.get('GRADIO_CLIENT_TEMP_DIR', 'Not set')}")
    
    # 运行调试
    debug_space_connection() 