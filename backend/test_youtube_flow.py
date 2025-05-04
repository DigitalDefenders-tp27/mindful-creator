#!/usr/bin/env python3
"""
YouTube评论分析流程测试脚本 (服务器版)
通过API请求测试:
1. 获取YouTube评论
2. NLP模型分析
3. LLM处理
"""
import os
import sys
import time
import logging
import requests
import json
import argparse
from typing import Dict, Any

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("youtube-test")

# 测试配置
TEST_VIDEO_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Rick Astley视频
MAX_COMMENTS = 10  # 最多获取的评论数
TEST_RESULT = {"success": False}  # 全局测试结果

# 从环境变量读取API地址，如果未设置则使用Railway提供的地址
# Railway.app 会自动设置 PORT 环境变量
PORT = os.environ.get("PORT", "8080")
API_BASE_URL = os.environ.get("API_BASE_URL", f"http://0.0.0.0:{PORT}")

# 测试模式设置
MOCK_MODE = False  # 设置为True启用模拟数据测试

def print_separator(title):
    """打印分隔线和标题"""
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)

def check_api_connectivity():
    """检查API连接性"""
    print_separator("检查API连接")
    print(f"尝试连接API: {API_BASE_URL}")
    
    try:
        response = requests.get(
            f"{API_BASE_URL}/api/health", 
            timeout=5
        )
        print(f"API连接成功! 状态码: {response.status_code}")
        return True
    except requests.exceptions.ConnectionError as e:
        print("API连接失败 - 连接被拒绝")
        print(f"错误详情: {str(e)}")
        
        # 尝试解析错误中的主机名和端口
        error_str = str(e)
        if "NewConnectionError" in error_str:
            parts = error_str.split("(host='")
            if len(parts) > 1:
                host_port = parts[1].split("', port=")
                if len(host_port) > 1:
                    host = host_port[0]
                    port = host_port[1].split(")")[0]
                    print(f"\n可能的解决方案:")
                    print(f"1. 确认API服务器在 {host}:{port} 运行")
                    print(f"2. 使用 --api 参数指定正确的API地址")
                    print(f"3. 使用 --mock 参数启用模拟数据测试模式")
        return False
    except Exception as e:
        print(f"API连接检查失败: {str(e)}")
        return False

def get_mock_comments():
    """返回模拟的YouTube评论"""
    return [
        "This video is amazing! I've watched it multiple times.",
        "I don't agree with the points made in this video.",
        "Could you explain the concept at 2:15 a bit more?",
        "Your content is great but the audio quality needs improvement.",
        "Best explanation of this topic I've seen so far!",
        "Bloody ripper of a video, mate! Thanks heaps for sharing!",
        "Fair dinkum, I reckon some of these points are a bit off.",
        "Deadset good content as always! Can't wait for your next upload.",
        "G'day! Could you explain that bit at 3:45 a bit more? Got a bit confused there.",
        "Crikey, the sound quality could be better on this one."
    ]

def test_health():
    """测试API健康状态"""
    print_separator("测试API健康状态")
    
    if MOCK_MODE:
        print("模拟模式: 返回模拟的健康状态")
        mock_result = {
            "status": "healthy",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "message": "API运行正常 (模拟数据)"
        }
        TEST_RESULT["health"] = mock_result
        TEST_RESULT["health_ok"] = True
        print("API状态: healthy (模拟)")
        print(f"时间戳: {mock_result['timestamp']}")
        print(f"消息: {mock_result['message']}")
        return True
    
    try:
        # 发送请求到健康检查端点
        start_time = time.time()
        response = requests.get(
            f"{API_BASE_URL}/api/health", 
            timeout=10
        )
        elapsed = time.time() - start_time
        
        print(f"健康检查请求完成，耗时: {elapsed:.2f}秒")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"API状态: {result.get('status', 'unknown')}")
                print(f"时间戳: {result.get('timestamp', 'unknown')}")
                if 'message' in result:
                    print(f"消息: {result['message']}")
                
                # 保存到全局结果
                TEST_RESULT["health"] = result
                TEST_RESULT["health_ok"] = True
                return True
            except json.JSONDecodeError:
                print(f"返回内容不是有效的JSON: {response.text}")
                TEST_RESULT["health_ok"] = False
                return False
        else:
            print(f"健康检查失败: {response.status_code}")
            print(f"响应: {response.text}")
            TEST_RESULT["health_ok"] = False
            return False
    except Exception as e:
        print(f"错误: 健康检查失败 - {str(e)}")
        TEST_RESULT["health_ok"] = False
        return False

def test_fetch_comments():
    """测试通过API获取YouTube评论"""
    print_separator("测试获取YouTube评论")
    
    if MOCK_MODE:
        print("模拟模式: 返回模拟的YouTube评论")
        mock_comments = get_mock_comments()
        print(f"获取到 {len(mock_comments)} 条评论 (模拟)")
        
        # 打印一些评论示例
        print("\n评论示例:")
        for i, comment in enumerate(mock_comments[:3], 1):
            print(f"{i}. {comment[:100]}")
        
        # 保存到全局结果
        TEST_RESULT["comments"] = mock_comments
        TEST_RESULT["comments_ok"] = True
        return mock_comments
    
    try:
        # 构建请求
        payload = {
            "video_url": TEST_VIDEO_URL,
            "max_comments": MAX_COMMENTS
        }
        
        # 发送请求获取评论
        print(f"开始通过API获取YouTube视频评论: {TEST_VIDEO_URL}")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/api/youtube/comments",
            json=payload,
            timeout=30  # 30秒超时
        )
        
        elapsed = time.time() - start_time
        print(f"请求完成，耗时: {elapsed:.2f}秒")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            comments = result.get("comments", [])
            print(f"获取到 {len(comments)} 条评论")
            
            # 打印一些评论示例
            if comments:
                print("\n评论示例:")
                for i, comment in enumerate(comments[:3], 1):  # 只显示前3条
                    comment_text = comment if isinstance(comment, str) else comment.get("text", "")
                    preview = f"{comment_text[:100]}..." if len(comment_text) > 100 else comment_text
                    print(f"{i}. {preview}")
                
                # 保存到全局结果
                TEST_RESULT["comments"] = comments
                TEST_RESULT["comments_ok"] = True
                return comments
            else:
                print("警告: API返回了空评论列表")
                TEST_RESULT["comments_ok"] = False
                return []
        else:
            print(f"获取评论失败: {response.status_code}")
            print(f"响应: {response.text}")
            TEST_RESULT["comments_ok"] = False
            return []
    except Exception as e:
        print(f"错误: 获取评论失败 - {str(e)}")
        TEST_RESULT["comments_ok"] = False
        return []

def test_nlp_analysis():
    """测试NLP分析API"""
    print_separator("测试NLP分析API")
    
    # 首先获取评论
    comments = TEST_RESULT.get("comments")
    if not comments:
        print("警告: 没有评论可供分析，尝试先获取评论")
        comments = test_fetch_comments()
    
    if not comments:
        print("错误: 无法获取评论进行分析")
        TEST_RESULT["nlp_ok"] = False
        return {"error": "无评论可供分析"}
    
    if MOCK_MODE:
        print("模拟模式: 返回模拟的NLP分析结果")
        total = len(comments)
        positive = max(1, round(total * 0.6))
        negative = max(1, round(total * 0.2))
        neutral = total - positive - negative
        toxic_count = max(1, round(total * 0.15))
        
        mock_result = {
            "sentiment": {
                "positive_count": positive,
                "negative_count": negative,
                "neutral_count": neutral,
                "positive_percentage": round(positive/total*100, 1),
                "negative_percentage": round(negative/total*100, 1),
                "neutral_percentage": round(neutral/total*100, 1)
            },
            "toxicity": {
                "toxic_count": toxic_count,
                "non_toxic_count": total - toxic_count,
                "toxic_percentage": round(toxic_count/total*100, 1),
                "toxic_types": {
                    "toxic": max(1, round(toxic_count * 0.7)),
                    "severe_toxic": round(toxic_count * 0.1),
                    "obscene": round(toxic_count * 0.4),
                    "threat": round(toxic_count * 0.05),
                    "insult": round(toxic_count * 0.3),
                    "identity_hate": round(toxic_count * 0.1)
                }
            },
            "note": "这是模拟数据，非实际NLP分析结果"
        }
        
        # 显示分析结果
        sentiment = mock_result["sentiment"]
        print(f"\n情感分析结果 (模拟):")
        print(f"- 正面评论: {sentiment['positive_count']} ({sentiment['positive_percentage']}%)")
        print(f"- 负面评论: {sentiment['negative_count']} ({sentiment['negative_percentage']}%)")
        print(f"- 中性评论: {sentiment['neutral_count']} ({sentiment['neutral_percentage']}%)")
        
        toxicity = mock_result["toxicity"]
        print(f"\n毒性分析结果 (模拟):")
        print(f"- 毒性评论数量: {toxicity['toxic_count']}")
        print(f"- 毒性评论百分比: {toxicity['toxic_percentage']}%")
        
        print(f"\n注意: {mock_result['note']}")
        
        TEST_RESULT["nlp_results"] = mock_result
        TEST_RESULT["nlp_ok"] = True
        return mock_result
    
    try:
        # 构建请求
        payload = {
            "comments": comments[:MAX_COMMENTS]  # 限制评论数量
        }
        
        # 发送NLP分析请求
        print(f"开始NLP分析请求，评论数: {len(payload['comments'])}")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/api/youtube/process_comments",
            json=payload,
            timeout=60  # 60秒超时
        )
        
        elapsed = time.time() - start_time
        print(f"NLP分析请求完成，耗时: {elapsed:.2f}秒")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # 显示分析结果
            if "sentiment" in result:
                sentiment = result["sentiment"]
                print(f"\n情感分析结果:")
                print(f"- 正面评论: {sentiment.get('positive_count', 0)}")
                print(f"- 负面评论: {sentiment.get('negative_count', 0)}")
                print(f"- 中性评论: {sentiment.get('neutral_count', 0)}")
            
            if "toxicity" in result:
                toxicity = result["toxicity"]
                print(f"\n毒性分析结果:")
                print(f"- 毒性评论数量: {toxicity.get('toxic_count', 0)}")
                print(f"- 毒性评论百分比: {toxicity.get('toxic_percentage', 0):.1f}%")
            
            if "note" in result:
                print(f"\n注意: {result['note']}")
            
            # 保存到全局结果
            TEST_RESULT["nlp_results"] = result
            TEST_RESULT["nlp_ok"] = True
            return result
        else:
            print(f"NLP分析请求失败: {response.status_code}")
            print(f"响应: {response.text}")
            TEST_RESULT["nlp_ok"] = False
            return {"error": f"API返回状态码 {response.status_code}"}
    except Exception as e:
        print(f"错误: NLP分析失败 - {str(e)}")
        TEST_RESULT["nlp_ok"] = False
        return {"error": str(e)}

def test_llm_analysis():
    """测试LLM分析API"""
    print_separator("测试LLM分析API")
    
    # 首先获取评论
    comments = TEST_RESULT.get("comments")
    if not comments:
        print("警告: 没有评论可供分析，尝试先获取评论")
        comments = test_fetch_comments()
    
    if not comments:
        print("错误: 无法获取评论进行分析")
        TEST_RESULT["llm_ok"] = False
        return {"error": "无评论可供分析"}
    
    if MOCK_MODE:
        print("模拟模式: 返回模拟的LLM分析结果")
        
        mock_result = {
            "status": "success",
            "strategies": """• Keep your cool when responding to negative comments - no need to get defensive or worked up
• Focus on the fair dinkum feedback while ignoring the personal attacks
• Show appreciation for constructive criticism even when it's delivered a bit harshly
• Set clear boundaries by moderating truly toxic or harmful comments
• Remember you don't have to respond to every negative comment - sometimes it's best to let it go""",
            "example_comments": [
                {
                    "comment": "This video is absolutely terrible. You clearly don't know what you're talking about!",
                    "response": "Thanks for your feedback. I'm always looking to improve my content. If you have specific points, I'd be happy to address them in future videos."
                },
                {
                    "comment": "The audio quality is awful, I can barely understand what you're saying.",
                    "response": "I appreciate you pointing this out. I've been working on upgrading my recording equipment. Next video should be much better!"
                }
            ]
        }
        
        # 显示分析结果
        print(f"分析状态: {mock_result['status']} (模拟)")
        
        print("\n生成的回复策略 (模拟):")
        print(mock_result["strategies"])
        
        examples = mock_result["example_comments"]
        print(f"\n生成的示例回复 ({len(examples)} 个) (模拟):")
        
        for i, example in enumerate(examples, 1):
            print(f"\n示例 {i}:")
            print(f"评论: {example['comment']}")
            print(f"回复: {example['response']}")
        
        TEST_RESULT["llm_results"] = mock_result
        TEST_RESULT["llm_ok"] = True
        return mock_result
    
    try:
        # 构建请求
        payload = {
            "comments": comments[:5]  # 限制评论数量为5，减轻LLM负担
        }
        
        # 发送LLM分析请求
        print(f"开始LLM分析请求，评论数: {len(payload['comments'])}")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/api/youtube/generate_strategies",
            json=payload,
            timeout=120  # 较长超时时间
        )
        
        elapsed = time.time() - start_time
        print(f"LLM分析请求完成，耗时: {elapsed:.2f}秒")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            # 显示分析结果
            print(f"分析状态: {result.get('status', 'unknown')}")
            
            if "strategies" in result:
                print("\n生成的回复策略:")
                strategies = result["strategies"]
                # 输出策略的前300个字符，如果太长的话
                if len(strategies) > 300:
                    print(f"{strategies[:300]}...")
                else:
                    print(strategies)
            
            if "example_comments" in result and result["example_comments"]:
                examples = result["example_comments"]
                print(f"\n生成的示例回复 ({len(examples)} 个):")
                
                for i, example in enumerate(examples[:2], 1):  # 只显示前2个
                    print(f"\n示例 {i}:")
                    print(f"评论: {example.get('comment', '')}")
                    print(f"回复: {example.get('response', '')}")
            
            # 保存到全局结果
            TEST_RESULT["llm_results"] = result
            TEST_RESULT["llm_ok"] = True
            return result
        else:
            print(f"LLM分析请求失败: {response.status_code}")
            print(f"响应: {response.text}")
            TEST_RESULT["llm_ok"] = False
            return {"error": f"API返回状态码 {response.status_code}"}
    except Exception as e:
        print(f"错误: LLM分析失败 - {str(e)}")
        TEST_RESULT["llm_ok"] = False
        return {"error": str(e)}

def test_complete_analysis():
    """测试完整YouTube分析API"""
    print_separator("测试完整YouTube分析流程")
    
    if MOCK_MODE:
        print("模拟模式: 返回模拟的完整分析结果")
        
        # 创建模拟评论
        mock_comments = get_mock_comments()
        total = len(mock_comments)
        
        # 模拟分析结果
        positive = max(1, round(total * 0.6))
        negative = max(1, round(total * 0.2))
        neutral = total - positive - negative
        toxic_count = max(1, round(total * 0.15))
        
        mock_result = {
            "status": "success",
            "total_comments": total,
            "analysis": {
                "sentiment": {
                    "positive_count": positive,
                    "negative_count": negative,
                    "neutral_count": neutral,
                    "positive_percentage": round(positive/total*100, 1),
                    "negative_percentage": round(negative/total*100, 1),
                    "neutral_percentage": round(neutral/total*100, 1)
                },
                "toxicity": {
                    "toxic_count": toxic_count,
                    "non_toxic_count": total - toxic_count,
                    "toxic_percentage": round(toxic_count/total*100, 1)
                },
                "note": "这是模拟数据，非实际分析结果"
            }
        }
        
        print(f"分析状态: {mock_result['status']} (模拟)")
        print(f"获取到 {mock_result['total_comments']} 条评论 (模拟)")
        
        if "analysis" in mock_result:
            analysis = mock_result["analysis"]
            
            if "sentiment" in analysis:
                sentiment = analysis["sentiment"]
                print(f"\n情感分析 (模拟):")
                print(f"- 正面评论: {sentiment['positive_count']} ({sentiment['positive_percentage']}%)")
                print(f"- 负面评论: {sentiment['negative_count']} ({sentiment['negative_percentage']}%)")
                print(f"- 中性评论: {sentiment['neutral_count']} ({sentiment['neutral_percentage']}%)")
            
            if "toxicity" in analysis:
                toxicity = analysis["toxicity"]
                print(f"\n毒性分析 (模拟):")
                print(f"- 毒性评论: {toxicity['toxic_count']}")
                print(f"- 毒性比例: {toxicity['toxic_percentage']}%")
            
            if "note" in analysis:
                print(f"\n注意: {analysis['note']}")
        
        TEST_RESULT["complete_results"] = mock_result
        TEST_RESULT["complete_ok"] = True
        return mock_result
    
    try:
        # 构建请求
        payload = {
            "video_url": TEST_VIDEO_URL,
            "max_comments": MAX_COMMENTS
        }
        
        # 发送请求到完整分析API
        print(f"开始完整YouTube视频分析: {TEST_VIDEO_URL}")
        start_time = time.time()
        
        response = requests.post(
            f"{API_BASE_URL}/api/youtube/analyze",
            json=payload,
            timeout=180  # 3分钟超时，完整分析需要更长时间
        )
        
        elapsed = time.time() - start_time
        print(f"完整分析请求完成，耗时: {elapsed:.2f}秒")
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"分析状态: {result.get('status', 'unknown')}")
            
            if result.get("status") == "success":
                print(f"获取到 {result.get('total_comments', 0)} 条评论")
                
                if "analysis" in result:
                    analysis = result["analysis"]
                    
                    if "sentiment" in analysis:
                        sentiment = analysis["sentiment"]
                        print(f"\n情感分析:")
                        print(f"- 正面评论: {sentiment.get('positive_count', 0)}")
                        print(f"- 负面评论: {sentiment.get('negative_count', 0)}")
                        print(f"- 中性评论: {sentiment.get('neutral_count', 0)}")
                    
                    if "toxicity" in analysis:
                        toxicity = analysis["toxicity"]
                        print(f"\n毒性分析:")
                        print(f"- 毒性评论: {toxicity.get('toxic_count', 0)}")
                        print(f"- 毒性比例: {toxicity.get('toxic_percentage', 0):.1f}%")
                    
                    if "note" in analysis:
                        print(f"\n注意: {analysis['note']}")
            else:
                print(f"分析失败: {result.get('message', '未知错误')}")
            
            # 保存到全局结果
            TEST_RESULT["complete_results"] = result
            TEST_RESULT["complete_ok"] = "status" in result and result.get("status") == "success"
            return result
        else:
            print(f"完整分析请求失败: {response.status_code}")
            print(f"响应: {response.text}")
            TEST_RESULT["complete_ok"] = False
            return {"error": f"API返回状态码 {response.status_code}"}
    except Exception as e:
        print(f"错误: 完整分析失败 - {str(e)}")
        TEST_RESULT["complete_ok"] = False
        return {"error": str(e)}

def run_all_tests():
    """运行所有测试"""
    print_separator(f"开始运行所有测试 (API: {API_BASE_URL}{'，模拟模式' if MOCK_MODE else ''})")
    
    # 0. 检查API连接
    if not MOCK_MODE:
        connectivity = check_api_connectivity()
        if not connectivity:
            print(f"\n警告: API连接测试失败 ({API_BASE_URL})")
            print("如果确认API地址正确，请使用 --mock 参数启用模拟模式")
            print("或者使用 --api 参数指定正确的API地址")
    
    # 1. 健康检查
    health_ok = test_health()
    if not health_ok and not MOCK_MODE:
        print("警告: API健康检查失败，但仍将继续其他测试")
    
    # 2. 获取评论
    test_fetch_comments()
    
    # 3. NLP分析
    test_nlp_analysis()
    
    # 4. LLM分析
    test_llm_analysis()
    
    # 5. 完整分析
    test_complete_analysis()
    
    # 打印测试总结
    print_separator("测试总结")
    
    tests = [
        {"name": "API健康检查", "success": TEST_RESULT.get("health_ok", False)},
        {"name": "获取评论", "success": TEST_RESULT.get("comments_ok", False)},
        {"name": "NLP分析", "success": TEST_RESULT.get("nlp_ok", False)},
        {"name": "LLM分析", "success": TEST_RESULT.get("llm_ok", False)},
        {"name": "完整分析流程", "success": TEST_RESULT.get("complete_ok", False)}
    ]
    
    passed = 0
    for test in tests:
        result = "通过" if test["success"] else "失败"
        status_color = "\033[92m" if test["success"] else "\033[91m"  # 绿色或红色
        print(f"{status_color}{test['name']}: {result}\033[0m")
        
        if test["success"]:
            passed += 1
    
    success_rate = (passed / len(tests)) * 100
    print(f"\n通过率: {success_rate:.1f}% ({passed}/{len(tests)})")
    
    if MOCK_MODE:
        print("\n注意：测试在模拟模式下运行，结果不代表实际API功能")
    
    # 返回退出码
    return 0 if passed == len(tests) else 1

def run_single_test(test_name):
    """运行单个指定的测试"""
    print_separator(f"运行单个测试: {test_name} (API: {API_BASE_URL}{'，模拟模式' if MOCK_MODE else ''})")
    
    # 检查API连接
    if not MOCK_MODE:
        connectivity = check_api_connectivity()
        if not connectivity:
            print(f"\n警告: API连接测试失败 ({API_BASE_URL})")
            print("如果确认API地址正确，请使用 --mock 参数启用模拟模式")
    
    if test_name == "health":
        test_health()
    elif test_name == "comments":
        test_fetch_comments()
    elif test_name == "nlp":
        test_nlp_analysis()
    elif test_name == "llm":
        test_llm_analysis()
    elif test_name == "complete":
        test_complete_analysis()
    else:
        print(f"错误: 未知的测试名称 '{test_name}'")
        return 1
    
    return 0

if __name__ == "__main__":
    try:
        # 解析命令行参数
        parser = argparse.ArgumentParser(description="YouTube评论分析API测试工具")
        parser.add_argument("--api", help="API基础URL，例如 https://api.tiezhu.org")
        parser.add_argument("--test", help="运行单个测试 (health, comments, nlp, llm, complete)")
        parser.add_argument("--video", help="测试用YouTube视频URL")
        parser.add_argument("--mock", action="store_true", help="启用模拟模式，不需要实际API")
        args = parser.parse_args()
        
        # 应用命令行参数
        if args.api:
            API_BASE_URL = args.api
            print(f"使用命令行指定的API URL: {API_BASE_URL}")
        
        if args.video:
            TEST_VIDEO_URL = args.video
            print(f"使用命令行指定的视频URL: {TEST_VIDEO_URL}")
        
        if args.mock:
            MOCK_MODE = True
            print("已启用模拟模式: 测试将使用模拟数据，不需要实际API连接")
        
        # 根据参数运行测试
        if args.test:
            exit_code = run_single_test(args.test)
        else:
            exit_code = run_all_tests()
        
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n测试被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n测试过程中发生未处理的异常: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 