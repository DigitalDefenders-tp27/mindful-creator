from flask import Blueprint, jsonify, request
from .models import db, Video, Comment, ToxicityScore, SentimentScore
from datetime import datetime

main = Blueprint('main', __name__)

# ---------------------- Static Data Endpoints ----------------------

@main.route('/api/influencer-guide', methods=['GET'])
def get_influencer_guide():
    return jsonify({
        'title': 'Ethical Influencer Guide',
        'sections': [
            {
                'title': 'Digital Responsibility',
                'content': 'Learn how to be a responsible digital citizen and influencer.'
            },
            {
                'title': 'Best Practices',
                'content': 'Follow these guidelines to maintain ethical standards in your digital presence.'
            }
        ]
    })


@main.route('/api/best-practices', methods=['GET'])
def get_best_practices():
    return jsonify({
        'practices': [
            'Share authentic and accurate information',
            'Respect others\' opinions and privacy',
            'Avoid spreading harmful content',
            'Set a positive example',
            'Engage in constructive discussions',
            'Verify information before sharing',
            'Maintain transparency in sponsored content'
        ]
    })

# ---------------------- Database Interaction Endpoint ----------------------

@main.route('/api/save-comment', methods=['POST'])
def save_comment():
    data = request.get_json()

    if not data or 'video_id' not in data or 'comment' not in data:
        return jsonify({'error': 'Missing video_id or comment'}), 400

    try:
        new_comment = Comment(
            video_id=data['video_id'],
            comment_text=data['comment']
        )
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({"message": "Comment saved successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to save comment: {str(e)}"}), 500


@main.route('/api/add-video', methods=['POST'])
def add_video():
    data = request.get_json()
    try:
        new_video = Video(
            youtube_url=data['youtube_url'],
            video_title=data['video_title']
        )
        db.session.add(new_video)
        db.session.commit()
        return jsonify({
            "status": "video added",
            "video_id": new_video.id
        }), 201
    except Exception as e:
        return jsonify({"error": f"Failed to add video: {str(e)}"}), 500


@main.route('/api/comments/<int:video_id>', methods=['GET'])
def get_comments(video_id):
    comments = Comment.query.filter_by(video_id=video_id).all()
    comment_list = [{"id": c.id, "comment_text": c.comment_text} for c in comments]
    return jsonify(comment_list)



@main.route('/api/analyze-comment', methods=['POST'])
def analyze_comment():
    data = request.get_json()
    comment_id = data['comment_id']
    sentiment = data['sentiment']       # e.g., "Positive"
    sentiment_conf = data['sentiment_confidence']
    toxicity_flags = data['toxicity']   # dict with keys: toxic, insult, threat, etc.

    # Save sentiment
    sentiment_entry = SentimentScore(
        comment_id=comment_id,
        sentiment_label=sentiment,
        confidence_score=sentiment_conf
    )
    db.session.add(sentiment_entry)

    # Save toxicity
    toxicity_entry = ToxicityScore(
        comment_id=comment_id,
        toxic=toxicity_flags.get('toxic', False),
        severe_toxic=toxicity_flags.get('severe_toxic', False),
        obscene=toxicity_flags.get('obscene', False),
        threat=toxicity_flags.get('threat', False),
        insult=toxicity_flags.get('insult', False),
        identity_hate=toxicity_flags.get('identity_hate', False)
    )
    db.session.add(toxicity_entry)

    db.session.commit()
    return jsonify({"message": "Analysis saved successfully"})




@main.route('/api/comments-with-sentiment', methods=['GET'])
def get_comments_with_sentiment():
    from .models import Comment, SentimentScore

    results = db.session.query(
        Comment.id,
        Comment.comment_text,
        SentimentScore.sentiment_label,
        SentimentScore.confidence_score
    ).join(SentimentScore, Comment.id == SentimentScore.comment_id).all()

    response = [
        {
            "comment_id": row.id,
            "text": row.comment_text,
            "sentiment": row.sentiment_label,
            "confidence": row.confidence_score
        }
        for row in results
    ]

    return jsonify(response)

@main.route('/api/sentiment-summary', methods=['GET'])
def sentiment_summary():
    from .models import SentimentScore

    results = db.session.query(
        SentimentScore.sentiment_label,
        db.func.count(SentimentScore.sentiment_label)
    ).group_by(SentimentScore.sentiment_label).all()

    response = [
        {"sentiment": row[0], "count": row[1]}
        for row in results
    ]
    return jsonify(response)

@main.route('/api/toxicity-summary', methods=['GET'])
def toxicity_summary():
    from .models import ToxicityScore

    toxic_count = db.session.query(ToxicityScore).filter(
        (ToxicityScore.toxic == True) |
        (ToxicityScore.severe_toxic == True) |
        (ToxicityScore.obscene == True) |
        (ToxicityScore.threat == True) |
        (ToxicityScore.insult == True) |
        (ToxicityScore.identity_hate == True)
    ).count()

    clean_count = db.session.query(ToxicityScore).filter(
        (ToxicityScore.toxic == False) &
        (ToxicityScore.severe_toxic == False) &
        (ToxicityScore.obscene == False) &
        (ToxicityScore.threat == False) &
        (ToxicityScore.insult == False) &
        (ToxicityScore.identity_hate == False)
    ).count()

    return jsonify([
        {"label": "Toxic", "count": toxic_count},
        {"label": "Non-Toxic", "count": clean_count}
    ])

@main.route('/api/comment-lengths', methods=['GET'])
def comment_lengths():
    from .models import Comment

    comments = Comment.query.all()

    response = [
        {"length": len(c.comment_text)} for c in comments
    ]
    return jsonify(response)

