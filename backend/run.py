from app import create_app, db

# Create Flask app using factory
app = create_app()

# Create all tables within the application context
with app.app_context():
    db.create_all()

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True, port=8000)
