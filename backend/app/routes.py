from flask import Blueprint, jsonify, request

main = Blueprint('main', __name__)

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

@main.route('/api/analyze-comment', methods=['POST'])
def analyze_comment():
    data = request.get_json()

    # 👇 Add this line here to see the comment in your terminal
    print(">>> Received request:", data)

    comment = data.get('comment', '')

    if not comment.strip():
        return jsonify({'error': 'Empty comment received.'}), 400

    comment_lower = comment.lower()

    positive_keywords = ['thank', 'great', 'good', 'awesome', 'well done', 'love', 'appreciate']
    negative_keywords = ['stupid', 'hate', 'worst', 'bitch', 'terrible', 'bad', 'awful', 'sucks']

    if any(word in comment_lower for word in positive_keywords):
        return jsonify({'type': 'Positive Feedback'})
    elif any(word in comment_lower for word in negative_keywords):
        return jsonify({'type': 'Negative Feedback'})
    else:
        return jsonify({'error': 'Unable to determine the nature of the comment. Please provide more context.'}), 200