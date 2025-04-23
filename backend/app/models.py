from . import db

class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    youtube_url = db.Column(db.Text)
    video_title = db.Column(db.Text)
    uploaded_at = db.Column(db.DateTime)
    analysed = db.Column(db.Boolean, default=False)
    comments = db.relationship('Comment', backref='video', lazy=True)

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
    comment_text = db.Column(db.Text)
    generated_at = db.Column(db.DateTime)

class ToxicityScore(db.Model):
    __tablename__ = 'toxicity_scores'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    toxic = db.Column(db.Boolean)
    severe_toxic = db.Column(db.Boolean)
    obscene = db.Column(db.Boolean)
    threat = db.Column(db.Boolean)
    insult = db.Column(db.Boolean)
    identity_hate = db.Column(db.Boolean)

class SentimentScore(db.Model):
    __tablename__ = 'sentiment_scores'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    sentiment_label = db.Column(db.String(10))  # Positive, Neutral, Negative
    confidence_score = db.Column(db.Float)

class PrivacyFlag(db.Model):
    __tablename__ = 'privacy_flags'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'))
    risk_type = db.Column(db.Text)  # e.g. Child Face, Address
    confidence_score = db.Column(db.Float)

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('videos.id'))
    alert_type = db.Column(db.String(50))  # e.g. burnout-risk
    message = db.Column(db.Text)
    triggered_at = db.Column(db.DateTime)

class ResourceFeedback(db.Model):
    __tablename__ = 'resource_feedback'
    id = db.Column(db.Integer, primary_key=True)
    resource_name = db.Column(db.Text)
    rating = db.Column(db.Integer)
    feedback = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime)
