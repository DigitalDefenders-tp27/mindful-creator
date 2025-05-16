const express = require('express');
const router = express.Router();
const ratingController = require('../controllers/ratingController');

// 提交新评分
router.post('/', ratingController.submitRating);

// 获取特定活动的评分统计
router.get('/:activityType', ratingController.getActivityStats);

// 获取所有活动的评分统计
router.get('/', ratingController.getAllStats);

module.exports = router; 