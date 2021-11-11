from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from log import log, Log

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

def add_value(value: float):
    date = datetime.now()
    dateStr = date.strftime("%Y-%m-%d %H:%M:%S")
    if value is not None:
        data = SensorData(sensor_value=value, date_added=dateStr)
        db.session.add(data)
        db.session.commit()
        return 0
    return 1


def get_value(id: int) -> SensorData:
    data = SensorData.query.filter_by(id=id).first()
    if data:
        log(Log.LOG, f"data found: {data}")
        return data
    else:
        log(Log.ERR, "make sure id already exists")
        return None

def get_all() -> list[SensorData]:
    datas = SensorData.query.all()
    if datas:
        return datas
    else:
        log(Log.LOG, "the list is empty")
        return []

def update_value(id: int, value: float):
    date = datetime.now()
    dateStr = date.strftime("%Y-%m-%d %H:%M:%S")
    data = SensorData.query.filter_by(id=id).first()
    if data:
        if value is not None:
            data.sensor_value = value
            data.date_added = dateStr
            db.session.add(data)
            db.session.commit()
            log(Log.LOG, "record successfully updated.")
            return 0
        else:
            log(Log.ERR, "pass not null value")
            return 1
    else:
        log(Log.ERR, "the given id doesn't exist.")
        return 2

def delete_value(id: int):
    data = SensorData.query.filter_by(id=id).first()
    if data:
        db.session.delete(data)
        db.session.commit()
        log(Log.LOG, f"record {id} successfully deleted.")
        return 0
    else:
        log(Log.ERR, "the given id doesn't exist.")
        return 1

@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    print("Sensor2Cloud DEMO")
    print("-" * 12)
    db.create_all()

    # add_value(5.2)

    # print(get_value(3))

    # update_value(3, 2.9)

    # delete_value(3)

    print()
    datas = get_all()
    for data in datas:
        print(data)

    # app.run(debug=True, host="0.0.0.0", port=5000)