from flask import Flask, render_template, request, jsonify
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Apna password daalein agar hai
        database="flaskdb"
    )

# Main page route
@app.route('/')
def index():
    return render_template('index.html')

# Get all leads
@app.route('/get-leads', methods=['GET'])
def get_leads():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user ORDER BY value DESC")
        leads = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(leads)
    except Error as e:
        return jsonify({"error": str(e)}), 500

# Submit new lead
@app.route('/submit-form', methods=['POST'])
def submit_form():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        address = request.form.get('address')
        city = request.form.get('city')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            INSERT INTO user (name, email, gender, address, city)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (name, email, gender, address, city)
        
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Lead saved successfully!"})
    except Error as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Update lead
@app.route('/update-lead/<int:id>', methods=['POST'])
def update_lead(id):
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        address = request.form.get('address')
        city = request.form.get('city')

        conn = get_db_connection()
        cursor = conn.cursor()
        
        query = """
            UPDATE user 
            SET name=%s, email=%s, gender=%s, address=%s, city=%s
            WHERE value=%s
        """
        values = (name, email, gender, address, city, id)
        
        cursor.execute(query, values)
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Lead updated successfully!"})
    except Error as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Delete lead
@app.route('/delete-lead/<int:id>', methods=['DELETE'])
def delete_lead(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM user WHERE value=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"success": True, "message": "Lead deleted successfully!"})
    except Error as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

