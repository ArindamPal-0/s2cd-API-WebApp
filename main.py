from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_value = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)
    date_added = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"{self.id}| {self.sensor_value} | {self.date_added}"
    
    def serialize(self):
        return {
            'id': int(self.id),
            'sensor value': self.sensor_value,
            'date added': self.date_added
        }

@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    print("Sensor2Cloud DEMO")
    print("-" * 12)
    db.create_all()
    # app.run(debug=True, host="0.0.0.0", port=5000)