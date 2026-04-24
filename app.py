from flask import Flask, jsonify, request

app = Flask(__name__)

# Model class required by tests
class Event:
    def __init__(self, id, title, description="", date="", location=""):
        self.id = id
        self.title = title
        self.description = description
        self.date = date
        self.location = location

# In-memory database
events = []
next_id = 1

def find_event(event_id):
    for event in events:
        if event["id"] == event_id:
            return event
    return None

@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Events API"}), 200

@app.route("/events", methods=["GET"])
def get_events():
    return jsonify(events), 200

@app.route("/events/<int:event_id>", methods=["GET"])
def get_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(event), 200

@app.route("/events", methods=["POST"])
def create_event():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title is required"}), 400
    new_event = {
        "id": next_id,
        "title": data["title"],
        "description": data.get("description", ""),
        "date": data.get("date", ""),
        "location": data.get("location", "")
    }
    events.append(new_event)
    next_id += 1
    return jsonify(new_event), 201

@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "No update data provided"}), 400
    allowed = ["title", "description", "date", "location"]
    for field in allowed:
        if field in data:
            event[field] = data[field]
    return jsonify(event), 200

@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = find_event(event_id)
    if event is None:
        return jsonify({"error": "Event not found"}), 404
    events.remove(event)
    return jsonify({"message": "Event deleted successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)