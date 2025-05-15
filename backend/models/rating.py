from datetime import datetime
from . import db

class Rating(db.Model):
    __tablename__ = 'ratings'

    id = db.Column(db.Integer, primary_key=True)
    activity_type = db.Column(db.String(50), nullable=False)
    rating_value = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 可选的用户关联

    @staticmethod
    def get_activity_stats(activity_type):
        """获取活动的评分统计"""
        from sqlalchemy import func
        stats = db.session.query(
            func.avg(Rating.rating_value).label('average'),
            func.count(Rating.id).label('count')
        ).filter(Rating.activity_type == activity_type).first()
        
        return {
            'average': float(stats.average) if stats.average else 0.0,
            'count': stats.count
        }

    @staticmethod
    def get_all_activities_stats():
        """获取所有活动的评分统计"""
        from sqlalchemy import func
        stats = db.session.query(
            Rating.activity_type,
            func.avg(Rating.rating_value).label('average'),
            func.count(Rating.id).label('count')
        ).group_by(Rating.activity_type).all()
        
        return {
            activity_type: {
                'average': float(avg) if avg else 0.0,
                'count': count
            }
            for activity_type, avg, count in stats
        } 