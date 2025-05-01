#!/usr/bin/env python3
"""
测试脚本: 验证从YouTube获取评论并使用Space API和LLM进行分析的功能
此脚本测试:
1. 从Rick Astley - Never Gonna Give You Up视频获取评论
2. 调用Space API分析这些评论
3. 调用LLM分析评论并生成回复策略
4. 验证返回结果的结构和内容
"""

import os
import sys
import logging
import time
from typing import List, Dict, Any
from dotenv import load_dotenv

# 确保项目根目录在Python路径中
proj_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if proj_root not in sys.path:
    sys.path.insert(0, proj_root)

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 导入必要的函数
try:
    from app.api.youtube.analyzer import (
        analyze_youtube_video,
        extract_video_id,
        fetch_youtube_comments,
        analyse_comments_with_space_api
    )
    from app.api.youtube.llm_handler import analyse_youtube_comments
    
    logger.info("成功导入所需功能")
except ImportError as e:
    logger.error(f"导入功能失败: {e}")
    sys.exit(1)

# 加载环境变量
load_dotenv(os.path.join(proj_root, '.env'))

# Rick Astley视频URL
RICK_ASTLEY_URL = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

async def test_youtube_comment_fetch():
    """测试从YouTube获取评论的功能"""
    logger.info("测试从YouTube获取评论...")
    
    video_id = extract_video_id(RICK_ASTLEY_URL)
    logger.info(f"提取的视频ID: {video_id}")
    assert video_id == "dQw4w9WgXcQ", "视频ID提取错误"
    
    # 获取评论
    try:
        start_time = time.time()
        comments = fetch_youtube_comments(RICK_ASTLEY_URL, max_comments=50)
        duration = time.time() - start_time
        
        logger.info(f"获取评论完成，耗时 {duration:.2f} 秒")
        logger.info(f"获取到 {len(comments)} 条评论")
        
        # 显示前5条评论
        for i, comment in enumerate(comments[:5]):
            preview = comment[:70] + "..." if len(comment) > 70 else comment
            logger.info(f"评论 {i+1}: {preview}")
            
        assert len(comments) > 0, "未能获取任何评论"
        return comments
        
    except Exception as e:
        logger.error(f"获取评论失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return []

async def test_space_api_analysis(comments):
    """测试使用Space API分析评论"""
    if not comments:
        logger.error("无评论可供分析")
        return False
        
    logger.info(f"使用Space API分析 {len(comments)} 条评论...")
    
    try:
        start_time = time.time()
        result = analyse_comments_with_space_api(comments)
        duration = time.time() - start_time
        
        logger.info(f"Space API分析完成，耗时 {duration:.2f} 秒")
        
        # 检查结果
        if "error" in result:
            logger.error(f"Space API返回错误: {result['error']}")
            return False
            
        # 验证结果结构
        if not result.get("sentiment") or not result.get("toxicity"):
            logger.error(f"Space API返回的结果结构不正确: {result.keys()}")
            return False
            
        # 输出分析结果摘要
        sentiment = result["sentiment"]
        toxicity = result["toxicity"]
        
        logger.info("=== 情感分析结果 ===")
        logger.info(f"积极评论: {sentiment.get('positive_count', 0)}")
        logger.info(f"中性评论: {sentiment.get('neutral_count', 0)}")
        logger.info(f"消极评论: {sentiment.get('negative_count', 0)}")
        
        logger.info("=== 毒性分析结果 ===")
        logger.info(f"总毒性评论数: {toxicity.get('toxic_count', 0)}")
        logger.info(f"毒性评论百分比: {toxicity.get('toxic_percentage', 0):.2f}%")
        
        logger.info("=== 毒性类型分布 ===")
        toxic_types = toxicity.get("toxic_types", {})
        for t_type, count in toxic_types.items():
            logger.info(f"{t_type}: {count}")
            
        logger.info("✅ Space API测试通过")
        return True
            
    except Exception as e:
        logger.error(f"❌ Space API测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

async def test_llm_analysis(comments):
    """测试使用LLM分析评论并生成回复策略"""
    if not comments:
        logger.error("无评论可供分析")
        return False
        
    logger.info(f"使用LLM分析 {len(comments)} 条评论...")
    
    try:
        start_time = time.time()
        result = analyse_youtube_comments(comments)
        duration = time.time() - start_time
        
        logger.info(f"LLM分析完成，耗时 {duration:.2f} 秒")
        
        # 检查结果
        if result.get("status") == "error":
            logger.error(f"LLM返回错误: {result.get('message', 'Unknown error')}")
            return False
            
        # 输出策略和示例回复
        strategies = result.get("strategies", "")
        example_comments = result.get("example_comments", [])
        
        logger.info("=== 回复策略 ===")
        logger.info(strategies)
        
        logger.info("=== 示例回复 ===")
        for i, example in enumerate(example_comments):
            comment = example.get("comment", "")
            response = example.get("response", "")
            
            comment_preview = comment[:50] + "..." if len(comment) > 50 else comment
            logger.info(f"评论 {i+1}: {comment_preview}")
            logger.info(f"回复: {response}")
            logger.info("-" * 30)
            
        logger.info("✅ LLM分析测试通过")
        return True
            
    except Exception as e:
        logger.error(f"❌ LLM分析测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

async def run_full_test():
    """运行完整的测试流程"""
    logger.info("开始完整测试流程")
    
    # 第1步: 获取YouTube评论
    comments = await test_youtube_comment_fetch()
    if not comments:
        logger.error("获取评论失败，测试终止")
        return False
        
    # 第2步: Space API分析
    space_success = await test_space_api_analysis(comments)
    if not space_success:
        logger.warning("Space API分析失败，但测试将继续")
        
    # 第3步: LLM分析
    llm_success = await test_llm_analysis(comments)
    if not llm_success:
        logger.warning("LLM分析失败，但测试将继续")
        
    overall_success = space_success and llm_success
    if overall_success:
        logger.info("🎉 所有测试通过!")
    else:
        logger.warning("⚠️ 部分测试失败，请检查日志")
        
    return overall_success

# 主入口点
if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("运行Rick Astley YouTube评论分析测试")
    logger.info("=" * 50)
    
    # 运行异步测试
    import asyncio
    loop = asyncio.get_event_loop()
    success = loop.run_until_complete(run_full_test())
    
    sys.exit(0 if success else 1) 