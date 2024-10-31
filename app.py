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
        with sqlite3.connect(database_path) as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT daily_price FROM rooms_pricing WHERE room_type = ? AND season = ?
            """, 
            (room_type, season))
            result = cur.fetchone()

            return jsonify({
                 "room_type": room_type,
                 "season": season,
                 "daily_price": result[0]}), 200
        


#Change price for a specific room in a specific season.
@app.route('/rooms/<room_type>/<season>', methods=['PUT'])
def update_room_price(room_type, season):
     data = request.get_json()
     new_price =data.get("daily_price")

     #Connect to database and change price
     conn = get_db_connection()
     cur = conn.cursor()
     cur.execute("""
        UPDATE rooms_pricing SET daily_price = ? WHERE room_type = ? AND season = ?
""", (new_price, room_type, season))
     conn.commit()

     if cur.rowcount > 0:
          response = jsonify({"message": "Daily prices updated"}), 200
     else:
          response = jsonify({"error":"error"}), 404
     conn.close()

     return response



#Send all data
@app.route('/room-pricing/data', methods=["GET"])
def get_bookings_data():
    with sqlite3.connect('/app/data/datarooms.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM datarooms")
        data = cur.fetchall()

        #Check the response
        if not data:
            #response is empty
            return "There was an error trying to retrieve price from a specific room!", 400
        return data






app.run(debug=True, host='0.0.0.0')
     

# docker build -t kong_arthur_room_price .    -> Først skrives den her nede i terminalen
# docker run -it -p 5002:5002 -v miniprojekt:/app/data kong_arthur_room_price    -> Derefter køres denne i terminalen



  
