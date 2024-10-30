from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

database_path = "/app/data/datarooms.db"

def get_db_connection():
    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    return conn


#GET room_price by room_type and season
@app.route('/rooms/<room_type>/<season>', methods=['GET'])
def get_room_price(room_type, season):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT dayly_price FROM room_pricing WHERE room_type = ? AND season = ?
        """, 
        (room_type, season))
        row = cur.fetchone()
        conn.close()
    
        if get_room_price:
            return jsonify({
                 "room_type": room_type,
                 "season": season,
                 "dayly_price": row("dayly_price")}), 200
        else:
             return jsonify({"error": "Price not found"}), 404



#Change price for a specific room in a specific season.
@app.route('/rooms/<room_type>/<season>', methods=['PUT'])
def update_room_price(room_type, season):
     data = request.get_json()
     new_price =data.get("dayly_price")

     #Connect to database and change price
     conn = get_db_connection()
     cur = conn.cursor()
     cur.execute("""
        UPDATE room_pricing SET dayly_price = ? WHERE room_type = ? AND season = ?
""", (new_price, room_type, season))
     conn.commit()

     if cur.rowcount > 0:
          response = jsonify({"message": "Dayly prices updated"}), 200
     else:
          response = jsonify({"error":"error"}), 404
     conn.close()

     return response


app.run(debug=True, host='0.0.0.0', port=5002)
     

# docker build -t kong_arthur_room_price .    -> Først skrives den her nede i terminalen
# docker run -it -p 5002:5002 -v miniprojekt:/app/data kong_arthur_room_price    -> Derefter køres denne i terminalen



  