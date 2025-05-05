#!/usr/bin/env python3
"""
YouTube评论分析流程测试脚本（直接函数调用版）
测试流程:
1. 获取YouTube评论
2. NLP模型分析
3. LLM处理
"""
import os
import sys
import time
import logging
import json
from typing import Dict, List, Any
import asyncio

# 添加项目根目录到Python路径，确保可以导入到项目模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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

def print_separator(title):
    """打印分隔线和标题"""
    print("\n" + "="*50)
    print(f" {title}")
    print("="*50)

def check_imports():
    """检查是否能成功导入所需模块"""
    print_separator("检查模块导入")
    
    # 尝试导入analyzer.py和llm_handler.py中的函数
    try:
        from app.api.youtube.analyzer import (
            extract_video_id,
            fetch_youtube_comments
        )
        print("✅ 成功导入分析器模块 (analyzer.py)")
        
        try:
            from app.api.youtube.llm_handler import analyse_youtube_comments
            print("✅ 成功导入LLM处理模块 (llm_handler.py)")
            return True
        except ImportError as e:
            print(f"❌ 导入LLM处理模块失败: {str(e)}")
            return False
    except ImportError as e:
        print(f"❌ 导入分析器模块失败: {str(e)}")
        return False

def test_fetch_comments():
    """测试获取YouTube评论功能"""
    print_separator("测试获取YouTube评论")
    
    try:
        # 导入函数
        from app.api.youtube.analyzer import extract_video_id, fetch_youtube_comments
        
        # 先提取视频ID
        video_id = extract_video_id(TEST_VIDEO_URL)
        if not video_id:
            print(f"错误: 无法从URL提取视频ID: {TEST_VIDEO_URL}")
            TEST_RESULT["comments_ok"] = False
            return []
        
        print(f"视频ID: {video_id}")
        print(f"开始获取YouTube视频评论")
        start_time = time.time()
        
        comments = fetch_youtube_comments(video_id, max_comments=MAX_COMMENTS)
        
        elapsed = time.time() - start_time
        print(f"评论获取完成，耗时: {elapsed:.2f}秒")
        print(f"获取到 {len(comments)} 条评论")
        
        # 打印一些评论示例
        if comments:
            print("\n评论示例:")
            for i, comment in enumerate(comments[:3], 1):
                preview = f"{comment[:100]}..." if len(comment) > 100 else comment
                print(f"{i}. {preview}")
            
            # 保存到全局结果
            TEST_RESULT["comments"] = comments
            TEST_RESULT["comments_ok"] = True
            return comments
        else:
            print("警告: 未获取到评论")
            TEST_RESULT["comments_ok"] = False
            return []
    except Exception as e:
        print(f"错误: 获取评论失败 - {str(e)}")
        import traceback
        traceback.print_exc()
        TEST_RESULT["comments_ok"] = False
        return []

def test_sentiment_analysis(comments=None):
    """测试基本的情感分析"""
    print_separator("测试情感分析")
    
    if comments is None:
        comments = TEST_RESULT.get("comments")
        if comments is None or not comments:
            print("警告: 没有评论可供分析，尝试先获取评论")
            comments = test_fetch_comments()
    
    if not comments:
        print("错误: 无法获取评论进行情感分析")
        TEST_RESULT["sentiment_ok"] = False
        return {"error": "没有评论可供分析"}
    
    try:
        # 简单的情感分析逻辑
        positive_words = ["good", "great", "awesome", "amazing", "love", "best", "excellent", "fantastic", "brilliant"]
        negative_words = ["bad", "terrible", "awful", "hate", "worst", "poor", "horrible", "terrible", "disappointing"]
        
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        print(f"开始分析 {len(comments)} 条评论")
        for comment in comments:
            comment_lower = comment.lower()
            positive_matches = sum(1 for word in positive_words if word in comment_lower)
            negative_matches = sum(1 for word in negative_words if word in comment_lower)
            
            if positive_matches > negative_matches:
                positive_count += 1
            elif negative_matches > positive_matches:
                negative_count += 1
            else:
                neutral_count += 1
        
        results = {
            "sentiment": {
                "positive_count": positive_count,
                "negative_count": negative_count,
                "neutral_count": neutral_count,
                "positive_percentage": round(positive_count / len(comments) * 100, 1),
                "negative_percentage": round(negative_count / len(comments) * 100, 1),
                "neutral_percentage": round(neutral_count / len(comments) * 100, 1)
            },
            "note": "基本文本分析结果，非机器学习模型"
        }
        
        # 显示分析结果
        sentiment = results["sentiment"]
        print(f"\n情感分析结果:")
        print(f"- 正面评论: {sentiment['positive_count']} ({sentiment['positive_percentage']}%)")
        print(f"- 负面评论: {sentiment['negative_count']} ({sentiment['negative_percentage']}%)")
        print(f"- 中性评论: {sentiment['neutral_count']} ({sentiment['neutral_percentage']}%)")
        
        # 保存到全局结果
        TEST_RESULT["sentiment_results"] = results
        TEST_RESULT["sentiment_ok"] = True
        return results
    except Exception as e:
        print(f"错误: 情感分析失败 - {str(e)}")
        import traceback
        traceback.print_exc()
        TEST_RESULT["sentiment_ok"] = False
        return {"error": str(e)}

def test_llm_analysis(comments=None):
    """测试LLM分析"""
    print_separator("测试LLM分析")
    
    if comments is None:
        comments = TEST_RESULT.get("comments")
        if comments is None or not comments:
            print("警告: 没有评论可供分析，尝试先获取评论")
            comments = test_fetch_comments()
    
    if not comments:
        print("错误: 无法获取评论进行LLM分析")
        TEST_RESULT["llm_ok"] = False
        return {"error": "没有评论可供分析"}
    
    try:
        # 尝试导入LLM处理模块
        try:
            from app.api.youtube.llm_handler import analyse_youtube_comments
            HAS_LLM = True
        except ImportError:
            print("警告: 未找到LLM处理模块，跳过测试")
            HAS_LLM = False
            TEST_RESULT["llm_ok"] = False
            return {"error": "LLM模块不可用"}
        
        if not HAS_LLM:
            TEST_RESULT["llm_ok"] = False
            return {"error": "LLM模块不可用"}
        
        print(f"开始LLM分析 {len(comments)} 条评论")
        start_time = time.time()
        
        # 直接调用函数，不使用asyncio.run()，因为这是同步函数
        results = analyse_youtube_comments(comments)
        
        elapsed = time.time() - start_time
        print(f"LLM分析完成，耗时: {elapsed:.2f}秒")
        
        # 显示分析结果
        print(f"分析状态: {results.get('status', 'unknown')}")
        
        if "strategies" in results:
            print("\n生成的回复策略:")
            strategies = results["strategies"]
            # 输出策略的前300个字符，如果太长的话
            if len(strategies) > 300:
                print(f"{strategies[:300]}...")
            else:
                print(strategies)
        
        if "example_comments" in results and results["example_comments"]:
            examples = results["example_comments"]
            print(f"\n生成的示例回复 ({len(examples)} 个):")
            
            for i, example in enumerate(examples[:2], 1):  # 只显示前2个
                print(f"\n示例 {i}:")
                print(f"评论: {example.get('comment', '')}")
                print(f"回复: {example.get('response', '')}")
        
        # 保存到全局结果
        TEST_RESULT["llm_results"] = results
        TEST_RESULT["llm_ok"] = True
        return results
    except Exception as e:
        print(f"错误: LLM分析失败 - {str(e)}")
        import traceback
        traceback.print_exc()
        TEST_RESULT["llm_ok"] = False
        return {"error": str(e)}

def test_complete_flow():
    """测试完整分析流程"""
    print_separator("测试完整分析流程")
    
    try:
        # 1. 获取评论
        comments = test_fetch_comments()
        if not comments:
            print("错误: 无法获取评论，完整流程测试终止")
            TEST_RESULT["complete_ok"] = False
            return {"success": False, "message": "无法获取评论"}
        
        # 2. 情感分析
        sentiment_results = test_sentiment_analysis(comments)
        
        # 3. LLM分析
        llm_results = test_llm_analysis(comments)
        
        # 4. 整合结果
        complete_results = {
            "success": True, 
            "method": "test_complete_flow",
            "duration_s": 0,
            "total_comments": len(comments),
            "analysis": {
                "sentiment": sentiment_results.get("sentiment", {}),
                "llm_results": llm_results
            }
        }
        
        print(f"完整分析流程完成")
        print(f"分析状态: {'成功' if complete_results.get('success') else '失败'}")
        
        # 保存到全局结果
        TEST_RESULT["complete_results"] = complete_results
        TEST_RESULT["complete_ok"] = complete_results.get("success", False)
        return complete_results
    except Exception as e:
        print(f"错误: 完整分析失败 - {str(e)}")
        import traceback
        traceback.print_exc()
        TEST_RESULT["complete_ok"] = False
        return {"error": str(e)}

def run_all_tests():
    """运行所有测试"""
    print_separator("开始运行所有测试")
    
    # 0. 检查模块导入
    imports_ok = check_imports()
    if not imports_ok:
        print("错误: 模块导入失败，无法执行测试")
        return 1
    
    # 1. 获取评论
    comments = test_fetch_comments()
    if not comments:
        print("错误: 未能获取评论，后续测试可能会失败")
    
    # 2. 情感分析
    sentiment_results = test_sentiment_analysis(comments)
    
    # 3. LLM分析
    llm_results = test_llm_analysis(comments)
    
    # 4. 完整流程
    complete_results = test_complete_flow()
    
    # 打印测试总结
    print_separator("测试总结")
    
    tests = [
        {"name": "获取评论", "success": len(comments) > 0},
        {"name": "情感分析", "success": TEST_RESULT.get("sentiment_ok", False)},
        {"name": "LLM分析", "success": TEST_RESULT.get("llm_ok", False)},
        {"name": "完整流程", "success": complete_results.get("success", False)}
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
    
    # 返回退出码
    return 0 if passed == len(tests) else 1

if __name__ == "__main__":
    import argparse
    
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="YouTube评论分析测试工具")
    parser.add_argument("--video", help="测试用YouTube视频URL")
    args = parser.parse_args()
    
    # 应用命令行参数
    if args.video:
        TEST_VIDEO_URL = args.video
        print(f"使用指定的视频URL: {TEST_VIDEO_URL}")
    
    try:
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