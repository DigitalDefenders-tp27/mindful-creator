from flask import Blueprint, jsonify
from database import get_connection   # ← Import properly

main = Blueprint('main', __name__)

@main.route('/api/train_cleaned', methods=['GET'])
def get_train_cleaned():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM train_cleaned")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    
    data = [dict(zip(columns, row)) for row in rows]
    response = Response(json.dumps(data), mimetype='application/json')
    return response

@main.route('/api/smmh_cleaned', methods=['GET'])
def get_smmh_cleaned():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM smmh_cleaned")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return jsonify([dict(zip(columns, row)) for row in rows])

@main.route('/api/screen_time_data', methods=['GET'])
def get_screen_time_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM screen_time_data ORDER BY date")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return jsonify([dict(zip(columns, row)) for row in rows])

@main.route('/api/music_mental_health_data', methods=['GET'])
def get_music_mental_health_data():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM music_mental_health_data")
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    cur.close()
    conn.close()
    return jsonify([dict(zip(columns, row)) for row in rows])
