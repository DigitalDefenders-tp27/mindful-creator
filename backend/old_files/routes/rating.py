from flask import Blueprint, request, jsonify
from flask_login import current_user
from ..models.rating import Rating
from .. import db

rating_bp = Blueprint('rating', __name__)

@rating_bp.route('/api/ratings', methods=['POST'])
def submit_rating():
    """提交新的评分"""
    data = request.get_json()
    
    if not data or 'activity_type' not in data or 'rating_value' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # 验证评分值
    rating_value = data['rating_value']
    if not isinstance(rating_value, int) or rating_value < 1 or rating_value > 5:
        return jsonify({'error': 'Invalid rating value'}), 400
    
    # 创建新的评分记录
    new_rating = Rating(
        activity_type=data['activity_type'],
        rating_value=rating_value,
        user_id=current_user.id if not current_user.is_anonymous else None
    )
    
    try:
        db.session.add(new_rating)
        db.session.commit()
        
        # 返回更新后的统计信息
        stats = Rating.get_activity_stats(data['activity_type'])
        return jsonify({
            'message': 'Rating submitted successfully',
            'stats': stats
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@rating_bp.route('/api/ratings/<activity_type>', methods=['GET'])
def get_activity_ratings(activity_type):
    """获取特定活动的评分统计"""
    try:
        stats = Rating.get_activity_stats(activity_type)
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@rating_bp.route('/api/ratings', methods=['GET'])
def get_all_ratings():
    """获取所有活动的评分统计"""
    try:
        stats = Rating.get_all_activities_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500 