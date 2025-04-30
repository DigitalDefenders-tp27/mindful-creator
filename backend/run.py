from app import create_app

# Create Flask app using factory
app = create_app()

# No more db.create_all() needed ❌

# Start the Flask server
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=False)
