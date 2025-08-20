# app.py

from flask import Flask
from flask_cors import CORS
from auth.routes import auth_bp
from routes.hospital_routes import hospital_bp
from routes.doctor_routes import doctor_bp
from routes.appointment_routes import appointment_bp
from routes.slot_routes import slot_bp


app = Flask(__name__)

# Enable CORS for all origins
CORS(app)

# Register authentication routes
app.register_blueprint(auth_bp)
app.register_blueprint(hospital_bp)
app.register_blueprint(doctor_bp)
app.register_blueprint(appointment_bp)
app.register_blueprint(slot_bp)



if __name__ == "__main__":
    app.run(debug=True, port=5000)
