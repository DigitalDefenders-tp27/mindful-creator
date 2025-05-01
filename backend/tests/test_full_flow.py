#!/usr/bin/env python
"""
完整流程测试脚本
测试从获取YouTube评论到发送到Spaces和OpenRouter的完整流程

运行方式:
python -m backend.tests.test_full_flow YOUR_YOUTUBE_URL
"""

import os
import sys
import time
import json
import logging
import traceback
import argparse
from typing import List, Dict, Any

# 设置日志
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_argparse():
    """设置命令行参数"""
    parser = argparse.ArgumentParser(description="测试YouTube评论分析完整流程")
    parser.add_argument("youtube_url", help="YouTube视频URL")
    parser.add_argument("--max-comments", type=int, default=20, help="最大评论数 (默认: 20)")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示详细日志")
    parser.add_argument("--spaces-only", action="store_true", help="仅测试Spaces API")
    return parser.parse_args()

def test_fetch_comments(youtube_url: str, max_comments: int) -> List[str]:
    """测试从YouTube获取评论"""
    logger.info("=" * 50)
    logger.info("1. 测试从YouTube获取评论")
    logger.info("=" * 50)
    
    logger.info(f"获取评论，视频URL: {youtube_url}")
    
    try:
        # 导入YouTube评论获取功能
        from backend.app.api.youtube.analyzer import extract_video_id, fetch_youtube_comments
        
        # 提取视频ID
        video_id = extract_video_id(youtube_url)
        if not video_id:
            logger.error("❌ 无法提取视频ID")
            return []
            
        logger.info(f"视频ID: {video_id}")
        
        # 获取评论
        start_time = time.time()
        comments = fetch_youtube_comments(youtube_url, max_comments)
        duration = time.time() - start_time
        
        # 记录结果
        if comments:
            logger.info(f"✅ 成功获取 {len(comments)} 条评论，耗时: {duration:.2f}秒")
            
            # 显示几条评论示例
            sample_size = min(3, len(comments))
            for i in range(sample_size):
                preview = comments[i][:100] + "..." if len(comments[i]) > 100 else comments[i]
                logger.info(f"评论样例 #{i+1}: {preview}")
                
            return comments
        else:
            logger.error("❌ 未找到评论")
            return []
            
    except Exception as e:
        logger.error(f"❌ 获取评论异常: {str(e)}")
        logger.error(traceback.format_exc())
        return []

def test_spaces_analysis(comments: List[str]) -> Dict[str, Any]:
    """测试将评论发送到Spaces进行分析"""
    logger.info("=" * 50)
    logger.info("2. 测试Spaces评论分析")
    logger.info("=" * 50)
    
    if not comments:
        logger.error("❌ 没有评论可供分析")
        return {}
        
    logger.info(f"向Spaces发送 {len(comments)} 条评论进行分析")
    
    try:
        # 导入Spaces分析功能
        from backend.app.api.youtube.analyzer import analyse_comments_with_space_api
        
        # 设置环境变量
        os.environ["GRADIO_CLIENT_REQUEST_TIMEOUT"] = "60" # 设置60秒超时
        
        logger.info(f"GRADIO_CLIENT_TEMP_DIR: {os.environ.get('GRADIO_CLIENT_TEMP_DIR', 'Not set')}")
        logger.info(f"GRADIO_CLIENT_REQUEST_TIMEOUT: {os.environ.get('GRADIO_CLIENT_REQUEST_TIMEOUT', 'Not set')}")
        
        # 发送评论到Spaces
        start_time = time.time()
        result = analyse_comments_with_space_api(comments)
        duration = time.time() - start_time
        
        # 检查结果
        if "error" in result:
            logger.error(f"❌ Spaces分析失败: {result['error']}")
            logger.error(f"结果内容: {json.dumps(result, indent=2)}")
            return result
            
        # 记录成功结果
        logger.info(f"✅ Spaces分析成功，耗时: {duration:.2f}秒")
        
        # 显示结果摘要
        if "sentiment" in result:
            sentiment = result["sentiment"]
            logger.info("情感分析结果:")
            logger.info(f"  积极评论: {sentiment.get('positive_count', 0)}")
            logger.info(f"  中性评论: {sentiment.get('neutral_count', 0)}")
            logger.info(f"  消极评论: {sentiment.get('negative_count', 0)}")
            
        if "toxicity" in result:
            toxicity = result["toxicity"]
            logger.info("毒性分析结果:")
            logger.info(f"  毒性评论总数: {toxicity.get('toxic_count', 0)}")
            logger.info(f"  毒性百分比: {toxicity.get('toxic_percentage', 0):.2f}%")
            
            if "toxic_types" in toxicity:
                logger.info("毒性类型分布:")
                for t_type, count in toxicity["toxic_types"].items():
                    logger.info(f"  {t_type}: {count}")
                    
        return result
        
    except Exception as e:
        logger.error(f"❌ Spaces分析异常: {str(e)}")
        logger.error(traceback.format_exc())
        return {"error": str(e)}

def test_llm_analysis(comments: List[str]) -> Dict[str, Any]:
    """测试将评论发送到OpenRouter/LLM进行分析"""
    logger.info("=" * 50)
    logger.info("3. 测试LLM评论分析")
    logger.info("=" * 50)
    
    if not comments:
        logger.error("❌ 没有评论可供分析")
        return {}
        
    logger.info(f"向LLM发送 {len(comments)} 条评论进行分析")
    
    try:
        # 导入LLM分析功能
        from backend.app.api.youtube.llm_handler import analyse_youtube_comments
        
        # 发送评论到LLM
        start_time = time.time()
        result = analyse_youtube_comments(comments)
        duration = time.time() - start_time
        
        # 记录结果
        logger.info(f"✅ LLM分析成功，耗时: {duration:.2f}秒")
        
        # 显示结果摘要
        if "strategies" in result:
            strategies_preview = result["strategies"][:200] + "..." if len(result["strategies"]) > 200 else result["strategies"]
            logger.info(f"策略摘要: {strategies_preview}")
            
        if "example_comments" in result:
            logger.info(f"示例评论数: {len(result['example_comments'])}")
            
            # 显示一个示例
            if result["example_comments"]:
                example = result["example_comments"][0]
                logger.info("示例评论与回复:")
                logger.info(f"  评论: {example.get('comment', '')[:100]}...")
                logger.info(f"  回复: {example.get('response', '')[:100]}...")
                
        return result
        
    except Exception as e:
        logger.error(f"❌ LLM分析异常: {str(e)}")
        logger.error(traceback.format_exc())
        return {"error": str(e)}

def test_integrated_analysis(youtube_url: str, max_comments: int) -> Dict[str, Any]:
    """测试完整的集成分析流程"""
    logger.info("=" * 50)
    logger.info("4. 测试集成分析流程")
    logger.info("=" * 50)
    
    try:
        from backend.app.api.youtube.analyzer import analyze_youtube_video
        
        logger.info(f"调用集成分析函数，URL: {youtube_url}")
        
        # 调用集成分析函数
        start_time = time.time()
        result = analyze_youtube_video(youtube_url)
        duration = time.time() - start_time
        
        if "status" in result and result["status"] == "error":
            logger.error(f"❌ 集成分析失败: {result.get('message', 'Unknown error')}")
            return result
            
        logger.info(f"✅ 集成分析成功，耗时: {duration:.2f}秒")
        logger.info(f"分析结果摘要: {json.dumps(result, indent=2)[:300]}...")
        
        return result
        
    except Exception as e:
        logger.error(f"❌ 集成分析异常: {str(e)}")
        logger.error(traceback.format_exc())
        return {"status": "error", "message": str(e)}

def test_full_api_call(youtube_url: str, max_comments: int) -> Dict[str, Any]:
    """测试通过API端点的完整调用流程"""
    logger.info("=" * 50)
    logger.info("5. 测试API端点调用")
    logger.info("=" * 50)
    
    try:
        import requests
        
        # API URL
        api_url = "https://mindful-creator-production-e20c.up.railway.app/api/youtube/analyze"
        
        # 准备请求数据
        request_data = {
            "video_url": youtube_url,
            "max_comments": max_comments
        }
        
        logger.info(f"发送API请求到: {api_url}")
        logger.info(f"请求数据: {request_data}")
        
        # 发送请求
        start_time = time.time()
        response = requests.post(
            api_url,
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=60  # 60秒超时
        )
        duration = time.time() - start_time
        
        # 检查响应
        logger.info(f"响应状态码: {response.status_code}")
        logger.info(f"响应耗时: {duration:.2f}秒")
        
        if response.status_code != 200:
            logger.error(f"❌ API请求失败! 状态码: {response.status_code}")
            logger.error(f"响应内容: {response.text[:300]}...")
            return {"status": "error", "message": f"API request failed with status {response.status_code}"}
            
        # 解析响应
        result = response.json()
        
        if result.get("status") == "error":
            logger.error(f"❌ API返回错误: {result.get('message', 'Unknown error')}")
            return result
            
        # 记录成功结果
        logger.info(f"✅ API请求成功!")
        
        # 检查评论数
        total_comments = result.get("total_comments", 0)
        logger.info(f"获取到 {total_comments} 条评论")
        
        # 检查是否使用了模拟数据
        analysis = result.get("analysis", {})
        if analysis and isinstance(analysis, dict) and "note" in analysis:
            note = analysis["note"]
            if "simulated" in note.lower():
                logger.warning(f"⚠️ API使用了模拟数据: {note}")
            else:
                logger.info(f"API备注: {note}")
                
        return result
        
    except Exception as e:
        logger.error(f"❌ API请求异常: {str(e)}")
        logger.error(traceback.format_exc())
        return {"status": "error", "message": str(e)}

def main():
    """主函数"""
    # 解析命令行参数
    args = setup_argparse()
    
    # 设置日志级别
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("=" * 60)
    logger.info("YouTube评论分析完整流程测试")
    logger.info("=" * 60)
    
    # 记录测试信息
    logger.info(f"测试URL: {args.youtube_url}")
    logger.info(f"最大评论数: {args.max_comments}")
    
    # 获取YouTube评论
    comments = test_fetch_comments(args.youtube_url, args.max_comments)
    
    # 如果没有评论，无法继续测试
    if not comments:
        logger.error("❌ 没有获取到评论，无法继续测试")
        sys.exit(1)
    
    # 测试Spaces分析
    spaces_result = test_spaces_analysis(comments)
    
    # 如果仅测试Spaces，到此结束
    if args.spaces_only:
        logger.info("仅测试Spaces模式，测试完成")
        
        if "error" in spaces_result:
            logger.error("❌ Spaces测试失败")
            sys.exit(1)
        else:
            logger.info("✅ Spaces测试成功")
            sys.exit(0)
    
    # 测试LLM分析
    llm_result = test_llm_analysis(comments)
    
    # 测试集成分析
    integrated_result = test_integrated_analysis(args.youtube_url, args.max_comments)
    
    # 测试API调用
    api_result = test_full_api_call(args.youtube_url, args.max_comments)
    
    # 检查所有测试结果
    has_error = False
    
    if "error" in spaces_result:
        logger.error("❌ Spaces分析测试失败")
        has_error = True
        
    if "error" in llm_result:
        logger.error("❌ LLM分析测试失败")
        has_error = True
        
    if integrated_result.get("status") == "error":
        logger.error("❌ 集成分析测试失败")
        has_error = True
        
    if api_result.get("status") == "error":
        logger.error("❌ API调用测试失败")
        has_error = True
    
    # 输出结果摘要
    logger.info("=" * 60)
    logger.info("测试结果摘要")
    logger.info("=" * 60)
    logger.info(f"YouTube评论获取: {'✅ 成功' if comments else '❌ 失败'}")
    logger.info(f"Spaces分析: {'✅ 成功' if 'error' not in spaces_result else '❌ 失败'}")
    logger.info(f"LLM分析: {'✅ 成功' if 'error' not in llm_result else '❌ 失败'}")
    logger.info(f"集成分析: {'✅ 成功' if integrated_result.get('status') != 'error' else '❌ 失败'}")
    logger.info(f"API调用: {'✅ 成功' if api_result.get('status') != 'error' else '❌ 失败'}")
    
    if not has_error:
        logger.info("🎉 所有测试成功完成!")
        sys.exit(0)
    else:
        logger.error("❌ 部分测试失败")
        sys.exit(1)

if __name__ == "__main__":
    main() 