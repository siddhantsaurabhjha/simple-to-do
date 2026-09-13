from flask import Flask, request, jsonify
from flask_cors import CORS
import database
app = Flask(__name__)
CORS(app)
database.init_db()
@app.route("/", methods=["GET"])
def home():
    """Root endpoint: Simple confirmation that backend server is running."""
    return jsonify({
        "success": True,
        "message": "Student / Task Management Portal Backend API is running successfully!",
        "endpoints": {
            "get_all_records": "GET /api/records",
            "get_record_by_id": "GET /api/records/<id>",
            "create_record": "POST /api/records",
            "update_record": "POST/PUT /api/records/<id>",
            "delete_record": "DELETE /api/records/<id>"
        }
    }), 200

@app.route("/api/records", methods=["GET"])
def get_records():
    """Endpoint: Fetch all student/task records."""
    try:
        records = database.get_all_records()
        return jsonify({
            "success": True,
            "records": records
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500


@app.route("/api/records/<int:record_id>", methods=["GET"])
def get_record(record_id):
    """Endpoint: Fetch a single record by ID."""
    try:
        record = database.get_record_by_id(record_id)
        if not record:
            return jsonify({
                "success": False,
                "message": "Record not found"
            }), 404

        return jsonify({
            "success": True,
            "record": record
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Server error: {str(e)}"
        }), 500

@app.route("/api/records", methods=["POST"])
def create_record():
    """Endpoint: Add a new record to SQLite."""
    try:
        data = request.get_json() or {}
        name = data.get("name", "").strip()
        roll_number = data.get("roll_number", "").strip()

        task = data.get("task", "").strip()
        category = data.get("category", "").strip()
        status = data.get("status", "Pending").strip()

        if not name or not roll_number or not task or not category or not status:
            return jsonify({
                "success": False,
                "message": "All fields (Name, Roll Number, Task, Category, Status) are required."
            }), 400
        new_record = database.add_record(name, roll_number, task, category, status)
        return jsonify({
            "success": True,
            "message": "Record added successfully!",
            "record": new_record
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Failed to add record: {str(e)}"
        }), 500

@app.route("/api/records/<int:record_id>", methods=["PUT"])
def update_record_api(record_id):
    """Endpoint: Update an existing record by ID."""
    try:
      
        existing = database.get_record_by_id(record_id)
        if not existing:
            return jsonify({
                "success": False,

                "message": "Record not found"                                                                                                                            
            }), 404

        data = request.get_json() or {}

        # Validate required fields
        name = data.get("name", "").strip()
        roll_number = data.get("roll_number", "").strip()
        task = data.get("task", "").strip()
        category = data.get("category", "").strip()
        status = data.get("status", "").strip()

        if not name or not roll_number or not task or not category or not status:
            return jsonify({
                "success": False,
                "message": "All fields (Name, Roll Number, Task, Category, Status) are required."
            }), 400

        # Update record in database
        updated_record = database.update_record(record_id, name, roll_number, task, category, status)
        return jsonify({
            "success": True,
            "message": "Record updated successfully!",
            "record": updated_record
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Failed to update record: {str(e)}"
        }), 500


@app.route("/api/records/<int:record_id>", methods=["DELETE"])
def delete_record_api(record_id):
    """Endpoint: Delete a record by ID."""
    try:
        existing = database.get_record_by_id(record_id)
        if not existing:
            return jsonify({
                "success": False,
                "message": "Record not found"
            }), 404

        database.delete_record(record_id)
        return jsonify({
            "success": True,
            "message": "Record deleted successfully!"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "message": f"Failed to delete record: {str(e)}"
        }), 500


if __name__ == "__main__":

    print("Starting Flask Backend Server on http://127.0.0.1:5000...")
    app.run(host="127.0.0.1", port=5000, debug=True)
