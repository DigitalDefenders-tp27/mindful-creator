const Rating = require('../models/Rating');

// 提交新评分
exports.submitRating = async (req, res) => {
  try {
    const { activity_type, rating_value } = req.body;
    
    const rating = new Rating({
      activity_type,
      rating_value,
      timestamp: new Date()
    });

    await rating.save();

    // 获取更新后的统计信息
    const stats = await Rating.getActivityStats(activity_type);

    res.status(201).json({
      message: 'Rating submitted successfully',
      stats
    });
  } catch (error) {
    res.status(500).json({
      message: 'Error submitting rating',
      error: error.message
    });
  }
};

// 获取特定活动的评分统计
exports.getActivityStats = async (req, res) => {
  try {
    const { activityType } = req.params;
    const stats = await Rating.getActivityStats(activityType);

    res.json(stats);
  } catch (error) {
    res.status(500).json({
      message: 'Error fetching activity stats',
      error: error.message
    });
  }
};

// 获取所有活动的评分统计
exports.getAllStats = async (req, res) => {
  try {
    const stats = await Rating.getActivityStats();
    const totalCount = stats.reduce((sum, stat) => sum + stat.count, 0);
    const totalRating = stats.reduce((sum, stat) => sum + (stat.average_rating * stat.count), 0);
    const averageRating = totalCount > 0 ? totalRating / totalCount : 0;

    res.json({
      total_count: totalCount,
      average_rating: averageRating,
      stats_by_activity: stats
    });
  } catch (error) {
    res.status(500).json({
      message: 'Error fetching all stats',
      error: error.message
    });
  }
}; 