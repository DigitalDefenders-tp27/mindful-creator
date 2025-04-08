from flask import Blueprint, jsonify

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
