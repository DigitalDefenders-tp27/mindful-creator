const { Model, DataTypes } = require('sequelize');
const sequelize = require('../config/database');

class Rating extends Model {
  static async getActivityStats(activityType) {
    const query = {
      attributes: [
        'activity_type',
        [sequelize.fn('COUNT', sequelize.col('id')), 'count'],
        [sequelize.fn('AVG', sequelize.col('rating_value')), 'average_rating'],
        [sequelize.fn('COUNT', sequelize.col('id')), 'total_ratings']
      ],
      group: ['activity_type']
    };

    if (activityType) {
      query.where = { activity_type: activityType };
    }

    const stats = await this.findAll(query);

    if (activityType) {
      if (stats.length === 0) {
        return {
          activity_type: activityType,
          count: 0,
          average_rating: 0,
          total_ratings: 0
        };
      }
      return stats[0];
    }

    return stats;
  }
}

Rating.init({
  id: {
    type: DataTypes.INTEGER,
    primaryKey: true,
    autoIncrement: true
  },
  activity_type: {
    type: DataTypes.ENUM(
      'breathing',
      'meditation',
      'grounding',
      'nature',
      'stretching',
      'color-breathing',
      'affirmation'
    ),
    allowNull: false
  },
  rating_value: {
    type: DataTypes.INTEGER,
    allowNull: false,
    validate: {
      min: 1,
      max: 5
    }
  },
  timestamp: {
    type: DataTypes.DATE,
    defaultValue: DataTypes.NOW
  }
}, {
  sequelize,
  modelName: 'Rating',
  tableName: 'ratings',
  timestamps: true,
  createdAt: 'timestamp',
  updatedAt: false
});

module.exports = Rating; 