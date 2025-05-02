#!/usr/bin/env python
"""
连接性测试脚本
测试从本地到Railway后端以及从Railway到Spaces的连接

运行方式: 
python -m backend.tests.test_connectivity
"""

import os
import sys
import time
import json
import logging
import requests
from urllib.parse import urlparse
import socket
import traceback

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 测试配置
RAILWAY_URL = "https://gleaming-celebration.railway.internal"
SPACES_URL = "https://jet-12138-commentresponse.hf.space"
TEST_COMMENTS = [
    "G'day mate! Brilliant video, absolute ripper content!",
    "Crikey! This content is rubbish, total waste of time."
]

def test_local_to_railway():
    """测试本地到Railway的连接性"""
    logger.info("=" * 50)
    logger.info("测试本地到Railway的连接性")
    logger.info("=" * 50)
    
    # 测试点1: 基本连接性
    try:
        logger.info(f"测试基本连接性到 {RAILWAY_URL}...")
        start_time = time.time()
        response = requests.get(
            f"{RAILWAY_URL}/api/health", 
            timeout=10
        )
        duration = time.time() - start_time
        
        logger.info(f"响应状态码: {response.status_code}")
        logger.info(f"连接耗时: {duration:.2f}秒")
        
        if response.status_code == 200:
            logger.info("✅ 基本连接测试成功!")
            logger.info(f"响应内容: {response.text[:200]}...")
        else:
            logger.error(f"❌ 基本连接测试失败! 状态码: {response.status_code}")
            logger.error(f"响应内容: {response.text[:200]}...")
            return False
            
    except Exception as e:
        logger.error(f"❌ 基本连接测试异常: {str(e)}")
        return False
        
    # 测试点2: WebSocket端点检查
    try:
        logger.info("测试WebSocket测试端点...")
        ws_check_resp = requests.get(f"{RAILWAY_URL}/ws-test", timeout=10)
        
        if ws_check_resp.status_code == 200:
            logger.info("✅ WebSocket测试端点可用!")
        else:
            logger.warning(f"⚠️ WebSocket测试端点返回非200状态码: {ws_check_resp.status_code}")
    except Exception as ws_e:
        logger.warning(f"⚠️ WebSocket测试端点异常: {str(ws_e)}")
    
    # 测试点3: 一个简单的API调用
    try:
        logger.info("测试API调用 (/api/relaxation)...")
        api_resp = requests.get(f"{RAILWAY_URL}/api/relaxation", timeout=10)
        
        if api_resp.status_code == 200:
            logger.info("✅ API调用测试成功!")
            logger.info(f"API响应: {api_resp.json()}")
        else:
            logger.warning(f"⚠️ API调用测试返回非200状态码: {api_resp.status_code}")
    except Exception as api_e:
        logger.warning(f"⚠️ API调用测试异常: {str(api_e)}")
    
    logger.info("✅ 本地到Railway连接测试完成")
    return True

def test_railway_to_spaces():
    """通过Railway测试与Spaces的连接性"""
    logger.info("=" * 50)
    logger.info("测试Railway到Spaces的连接性")
    logger.info("=" * 50)
    
    logger.info("向Railway API发送测试请求，要求其连接Spaces...")
    
    try:
        test_data = {
            "test_type": "spaces_connection",
            "comments": TEST_COMMENTS
        }
        
        start_time = time.time()
        response = requests.post(
            f"{RAILWAY_URL}/api/youtube/test-spaces",
            json=test_data,
            timeout=30  # 更长的超时时间
        )
        duration = time.time() - start_time
        
        logger.info(f"响应状态码: {response.status_code}")
        logger.info(f"响应耗时: {duration:.2f}秒")
        
        if response.status_code == 200:
            result = response.json()
            logger.info("✅ Space连接测试请求成功!")
            
            if result.get("status") == "success":
                logger.info("✅ Railway成功连接到Spaces!")
                logger.info(f"Connection details: {result.get('details', {})}")
                return True
            else:
                logger.error(f"❌ Railway无法连接到Spaces: {result.get('message', 'Unknown error')}")
                logger.error(f"错误详情: {result.get('error_details', 'No details')}")
                return False
        else:
            logger.error(f"❌ Space连接测试请求失败! 状态码: {response.status_code}")
            logger.error(f"响应内容: {response.text[:200]}...")
            return False
            
    except Exception as e:
        logger.error(f"❌ Space连接测试异常: {str(e)}")
        return False

def test_direct_spaces_connection():
    """直接测试本地到Spaces的连接（用于对比）"""
    logger.info("=" * 50)
    logger.info("测试本地直接到Spaces的连接性")
    logger.info("=" * 50)
    
    try:
        # 先测试基本网络连接
        spaces_host = urlparse(SPACES_URL).netloc
        logger.info(f"测试到 {spaces_host} 的TCP连接...")
        
        start_time = time.time()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10)
        s.connect((spaces_host, 443))
        s.close()
        duration = time.time() - start_time
        
        logger.info(f"TCP连接成功，耗时: {duration:.2f}秒")
        
        # 测试HTTP连接
        logger.info(f"测试HTTP连接到 {SPACES_URL}...")
        start_time = time.time()
        response = requests.get(f"{SPACES_URL}/", timeout=15)
        duration = time.time() - start_time
        
        logger.info(f"HTTP响应状态码: {response.status_code}")
        logger.info(f"HTTP连接耗时: {duration:.2f}秒")
        
        # 使用直接HTTP请求测试API
        logger.info("尝试使用直接HTTP请求连接Space API...")
        
        # 定义要尝试的API端点
        api_endpoints = [
            "/api/predict",  # 标准API端点
            "/run/predict",  # 替代运行端点
            "/predict"       # 简单端点
        ]
        
        # 准备测试数据
        test_input = "\n".join(TEST_COMMENTS)
        
        # 尝试每个端点
        for endpoint in api_endpoints:
            api_url = f"{SPACES_URL}{endpoint}"
            logger.info(f"测试端点: {api_url}")
            
            # 准备请求数据
            if "/api/" in endpoint:
                payload = {"data": [test_input]}
            else:
                payload = {"data": [test_input]}
                
            headers = {"Content-Type": "application/json"}
            
            # 添加授权（如果有HF_TOKEN）
            hf_token = os.environ.get("HF_TOKEN")
            if hf_token:
                headers["Authorization"] = f"Bearer {hf_token}"
                logger.info("使用HF_TOKEN进行身份验证")
            
            # 发送请求
            try:
                predict_start = time.time()
                response = requests.post(
                    api_url,
                    json=payload,
                    headers=headers,
                    timeout=60  # 60秒超时
                )
                predict_duration = time.time() - predict_start
                
                logger.info(f"端点 {endpoint} 响应状态码: {response.status_code}")
                logger.info(f"请求耗时: {predict_duration:.2f}秒")
                
                if response.status_code == 200:
                    logger.info(f"✅ 端点 {endpoint} 请求成功!")
                    
                    # 解析响应
                    try:
                        result = response.json()
                        
                        # 处理不同的响应格式
                        if "data" in result and isinstance(result["data"], list) and len(result["data"]) > 0:
                            result = result["data"][0]
                            
                        logger.info(f"结果类型: {type(result)}")
                        
                        if isinstance(result, dict):
                            logger.info(f"结果键: {list(result.keys())}")
                            
                            if "sentiment_counts" in result:
                                logger.info(f"情感分析结果: {result['sentiment_counts']}")
                            
                            if "toxicity_counts" in result:
                                logger.info(f"毒性分析结果: {result['toxicity_counts']}")
                        
                        logger.info(f"Beauty! 端点 {endpoint} 测试成功!")
                        return True
                    except Exception as parse_err:
                        logger.error(f"❌ 无法解析响应: {str(parse_err)}")
                        logger.info(f"原始响应: {response.text[:200]}...")
                else:
                    logger.warning(f"❌ 请求失败: {response.status_code}")
                    if response.text:
                        logger.info(f"响应内容: {response.text[:200]}...")
            except Exception as req_err:
                logger.error(f"❌ 请求异常: {str(req_err)}")
                
        # 如果gradio_client可用，也尝试使用它（保留为比较）
        try:
            from gradio_client import Client
            logger.info("作为比较，尝试使用gradio_client...")
            
            # 设置超时环境变量
            os.environ["GRADIO_CLIENT_REQUEST_TIMEOUT"] = "60"
            
            client_start = time.time()
            client = Client(SPACES_URL)
            client_duration = time.time() - client_start
            
            logger.info(f"✅ gradio_client连接成功，耗时: {client_duration:.2f}秒")
            
            # 尝试一次预测调用
            logger.info("尝试一次gradio_client预测调用...")
            
            predict_start = time.time()
            result = client.predict(test_input, api_name="/predict")
            predict_duration = time.time() - predict_start
            
            logger.info(f"✅ gradio_client预测调用成功，耗时: {predict_duration:.2f}秒")
            
        except ImportError:
            logger.info("gradio_client不可用，跳过比较测试")
        except Exception as client_err:
            logger.warning(f"gradio_client测试失败: {str(client_err)}")
        
        logger.error("❌ 所有HTTP端点测试均失败")
        return False
            
    except socket.error as socket_err:
        logger.error(f"❌ TCP连接失败: {str(socket_err)}")
        return False
        
    except Exception as e:
        logger.error(f"❌ 直接Spaces连接测试异常: {str(e)}")
        logger.error(traceback.format_exc())
        return False

def display_network_info():
    """显示网络配置相关的信息"""
    logger.info("=" * 50)
    logger.info("网络配置信息")
    logger.info("=" * 50)
    
    # 获取本地IP地址
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        logger.info(f"本地IP地址: {local_ip}")
    except:
        logger.warning("无法获取本地IP地址")
    
    # 检查HTTP代理设置
    http_proxy = os.environ.get("HTTP_PROXY", "未设置")
    https_proxy = os.environ.get("HTTPS_PROXY", "未设置")
    no_proxy = os.environ.get("NO_PROXY", "未设置")
    
    logger.info(f"HTTP_PROXY: {http_proxy}")
    logger.info(f"HTTPS_PROXY: {https_proxy}")
    logger.info(f"NO_PROXY: {no_proxy}")
    
    # 测试DNS解析
    spaces_host = urlparse(SPACES_URL).netloc
    railway_host = urlparse(RAILWAY_URL).netloc
    
    try:
        spaces_ip = socket.gethostbyname(spaces_host)
        logger.info(f"Spaces主机 {spaces_host} 解析到IP: {spaces_ip}")
    except:
        logger.warning(f"无法解析Spaces主机 {spaces_host}")
    
    try:
        railway_ip = socket.gethostbyname(railway_host)
        logger.info(f"Railway主机 {railway_host} 解析到IP: {railway_ip}")
    except:
        logger.warning(f"无法解析Railway主机 {railway_host}")

if __name__ == "__main__":
    logger.info("=" * 60)
    logger.info("连接性测试工具")
    logger.info("=" * 60)
    
    # 显示网络信息
    display_network_info()
    
    # 测试1: 本地到Railway
    local_to_railway = test_local_to_railway()
    
    # 测试2: Railway到Spaces (通过Railway API)
    railway_to_spaces = test_railway_to_spaces()
    
    # 测试3: 本地直接到Spaces (用于对比)
    direct_to_spaces = test_direct_spaces_connection()
    
    # 输出总结
    logger.info("=" * 60)
    logger.info("测试结果总结")
    logger.info("=" * 60)
    logger.info(f"本地到Railway连接: {'✅ 成功' if local_to_railway else '❌ 失败'}")
    logger.info(f"Railway到Spaces连接: {'✅ 成功' if railway_to_spaces else '❌ 失败'}")
    logger.info(f"本地直接到Spaces连接: {'✅ 成功' if direct_to_spaces else '❌ 失败'}")
    
    if local_to_railway and not railway_to_spaces and direct_to_spaces:
        logger.info("👉 结论: Railway服务器可能存在网络限制，无法连接到Spaces")
    elif local_to_railway and not railway_to_spaces and not direct_to_spaces:
        logger.info("👉 结论: Spaces服务可能不可用或存在通用访问问题")
    elif not local_to_railway:
        logger.info("👉 结论: Railway服务器可能不可用或存在访问问题")
    elif local_to_railway and railway_to_spaces:
        logger.info("👉 结论: 所有连接正常，问题可能在于应用逻辑或配置") 