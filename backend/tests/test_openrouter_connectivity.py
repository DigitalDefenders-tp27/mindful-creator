#!/usr/bin/env python3
"""
测试脚本：验证OpenRouter API连接性和评论分析功能
此脚本测试：
1. 连接到OpenRouter API并验证API密钥有效性
2. 生成100个测试评论并通过LLM分析
3. 验证返回结果的结构和内容
"""

import os
import sys
import logging
import time
import random
import json
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

# 加载环境变量
load_dotenv(os.path.join(proj_root, '.env'))

# 导入LLM处理器功能
try:
    from app.api.youtube.llm_handler import (
        identify_critical_comments,
        analyse_youtube_comments
    )
    logger.info("成功导入LLM处理器功能")
except ImportError as e:
    logger.error(f"导入LLM处理器功能失败: {e}")
    sys.exit(1)

# 测试评论样本
SAMPLE_COMMENTS = {
    "positive": [
        "这个视频太有帮助了！谢谢分享。",
        "我一直在关注你的频道，你的内容越来越好了！",
        "解释得很清楚，容易理解。", 
        "这正是我今天需要听到的。谢谢！",
        "你的视频对我的学习帮助很大。继续加油！",
    ],
    "neutral": [
        "我看完了整个视频，学到了新东西。",
        "有趣的观点，我以前没这么想过。",
        "刚发现你的频道，会看更多视频的。",
        "你用什么相机拍摄的？",
        "你什么时候发下一个视频？",
    ],
    "negative": [
        "这个视频对这么简单的主题来说太长了。",
        "你显然不知道你在说什么。",
        "我不敢相信居然有人看这种垃圾。",
        "你的声音太烦人了，我看不完这个视频。",
        "别再做标题党了，真的很烦人。",
    ],
    "toxic": [
        "这个视频里的信息完全错误。下次做好研究再说。",
        "这是我见过最糟糕的教程。完全浪费时间。",
        "如果这是你能做到的最好水平，你应该退出YouTube。",
        "你怎么能有这么多订阅者却制作如此糟糕的内容？",
        "我讨厌你假装的热情。做真实的自己吧。",
    ]
}

def generate_test_comments(count: int = 100):
    """
    生成测试评论的二维列表，通过随机选择样本评论并添加变化
    
    参数:
        count: 要生成的评论数量
        
    返回:
        生成的评论二维列表
    """
    logger.info(f"生成{count}条测试评论")
    
    all_categories = list(SAMPLE_COMMENTS.keys())
    generated_comments = []
    
    # 生成随机评论
    for _ in range(count):
        # 随机选择一个类别
        category = random.choice(all_categories)
        # 从该类别随机选择一条评论
        base_comment = random.choice(SAMPLE_COMMENTS[category])
        generated_comments.append([base_comment])
    
    return generated_comments

def test_openrouter_connectivity():
    """测试OpenRouter API的连接性"""
    logger.info("测试OpenRouter API连接...")
    
    if not os.environ.get("OPENROUTER_API_KEY"):
        logger.error("❌ 未找到OPENROUTER_API_KEY环境变量")
        return False
    
    test_comment = ["这是一条测试评论，请分析它的情感。"]
    
    try:
        # 调用LLM处理器识别关键评论
        logger.info("尝试连接OpenRouter API...")
        start_time = time.time()
        
        # 使用简单的评论进行初始连接测试
        result = identify_critical_comments(test_comment)
        
        duration = time.time() - start_time
        logger.info(f"OpenRouter API响应在{duration:.2f}秒内完成")
        
        # 详细记录返回结果的类型和内容
        logger.info(f"返回结果类型: {type(result)}")
        if isinstance(result, list):
            logger.info(f"列表长度: {len(result)}")
            logger.info(f"列表内容: {result}")
            # 如果是列表，但符合预期，则依然表示成功
            if len(result) > 0:
                logger.info("✅ OpenRouter API连接成功 (返回列表格式)")
                return True
        elif result and isinstance(result, dict):
            logger.info(f"字典键: {result.keys()}")
            logger.info("✅ OpenRouter API连接成功 (返回字典格式)")
            return True
        else:
            logger.error(f"❌ OpenRouter API返回了意外结果类型: {type(result)}")
            return False
            
    except Exception as e:
        logger.error(f"❌ OpenRouter API连接测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

def test_llm_comment_analysis():
    """测试LLM评论分析功能"""
    logger.info("测试LLM评论分析功能...")
    
    # 生成100条测试评论
    comments_2d = generate_test_comments(100)
    logger.info(f"生成了{len(comments_2d)}条评论")
    
    try:
        # 调用LLM分析评论
        logger.info("调用LLM分析评论...")
        start_time = time.time()
        
        result = analyse_youtube_comments(comments_2d)
        
        duration = time.time() - start_time
        logger.info(f"LLM分析在{duration:.2f}秒内完成")
        
        # 检查结果
        if not result or not isinstance(result, dict):
            logger.error(f"LLM返回了意外结果类型: {type(result)}")
            return False
            
        # 输出分析结果摘要
        logger.info("=== LLM分析结果 ===")
        for key, value in result.items():
            if isinstance(value, dict):
                logger.info(f"{key}:")
                for sub_key, sub_value in value.items():
                    logger.info(f"  {sub_key}: {sub_value}")
            else:
                logger.info(f"{key}: {value}")
        
        logger.info("✅ LLM评论分析测试通过")
        return True
            
    except Exception as e:
        logger.error(f"❌ LLM评论分析测试失败: {e}")
        import traceback
        logger.error(traceback.format_exc())
        return False

# 主入口点
if __name__ == "__main__":
    logger.info("=" * 50)
    logger.info("运行OpenRouter API测试")
    logger.info("=" * 50)
    
    # 首先测试连接性
    connectivity_success = test_openrouter_connectivity()
    
    if connectivity_success:
        # 如果连接成功，测试评论分析
        analysis_success = test_llm_comment_analysis()
        
        if analysis_success:
            logger.info("🎉 所有测试通过")
            sys.exit(0)
        else:
            logger.error("❌ LLM评论分析测试失败")
            sys.exit(1)
    else:
        logger.error("❌ OpenRouter API连接测试失败，跳过评论分析测试")
        sys.exit(1) 