from flask import Flask, Blueprint, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from log import log, Log

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sensor_value = db.Column(db.Float(precision=2, asdecimal=True), nullable=False)
    date_added = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"{self.id}| {float(self.sensor_value)} | {self.date_added}"
    
    def serialize(self):
        return {
            'id': int(self.id),
            'sensor value': float(self.sensor_value),
            'date added': self.date_added
        }

def add_value(value: float):
    date = datetime.now()
    dateStr = date.strftime("%Y-%m-%d %H:%M:%S")
    if value is not None:
        data = SensorData(sensor_value=value, date_added=dateStr)
        db.session.add(data)
        db.session.commit()
        return 0, data.id
    return 1, None


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
            log(Log.ERR, "pass a not null value")
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
        return 0, data.id
    else:
        log(Log.ERR, "the given id doesn't exist.")
        return 1, None


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/')
def test_api_conn():
    response = make_response(jsonify({'msg': 'This is Sensor Data Store API...'}), 200, {'content-type': 'application/json'})
    return response

@api.route('/sensor_values')
def get_all_data():
    datas = get_all()

    responseData = dict({'msg': 'all the data fetched.'})
    responseData['data'] = [data.serialize() for data in datas]
    response = make_response(jsonify(responseData), 200, {'content-type': 'application/json'})
    return response

@api.route('/sensor_values/<int:id>')
def get_data(id: int):
    data = get_value(id)

    responseData = dict({'msg': 'something went wrong.'})
    statusCode = 400
    if data is not None:
        responseData['msg'] = f'data with id {id} fetched.'
        responseData['data'] = data.serialize()
        statusCode = 200
    else:
        statusCode = 404
        responseData['msg'] = 'no such id exist.'
    
    response = make_response(jsonify(responseData), statusCode, {'content-type': 'application/json'})
    return response

@api.route('/sensor_values', methods=['POST'])
def add_data():
    responseData = dict({'msg': 'something went wrong.'})
    statusCode = 400
    if request.json:
        if 'value' in request.json:
            value = request.json.get('value')
            status, id = add_value(value)
            if status == 0:
                responseData['msg'] = 'record successfully added.'
                if id is not None:
                    responseData['id'] = id
                statusCode = 201
            else:
                responseData['msg'] = 'record not created. send valid sensor value.'
                statusCode = 400
        else:
            responseData['msg'] = "record not created. send the sensor value in json object with 'value' as key."
            statusCode = 400
    else:
        responseData['msg'] = 'record not created. send json objects, set Content-Type to application/json'
        statusCode = 400
    
    response = make_response(jsonify(responseData), statusCode, {'content-type': 'application/json'})
    return response

@api.route('/sensor_values/<int:id>', methods=['PUT'])
def update_data(id: int):
    responseData = dict({'msg': 'something went wrong.'})
    statusCode = 400
    if request.json:
        if 'value' in request.json:
            value = request.json.get('value')
            status = update_value(id, value)
            if status == 0:
                responseData['msg'] = f'record with id {id} successfully updated.'
                statusCode = 200
            elif status == 1:
                responseData['msg'] = 'record not updated. send valid sensor value.'
                statusCode = 400
            elif status == 2:
                responseData['msg'] = 'record not updated. the sent id does not exist'
                statusCode = 404
        else:
            responseData['msg'] = "record not updated. send the sensor value in json object with 'value' as key."
            statusCode = 400
    else:
        responseData['msg'] = 'record not updated. send json objects, set Content-Type to application/json'
        statusCode = 400
    
    response = make_response(jsonify(responseData), statusCode, {'content-type': 'application/json'})
    return response


@api.route('/sensor_values/<int:id>', methods=['DELETE'])
def delete_data(id: int):
    status, id = delete_value(id)

    responseData = dict({'msg': 'something went wrong.'})
    statusCode = 400

    if status == 0:
        responseData['msg'] = 'record successfully deleted.'
        responseData['id'] = id
        statusCode = 200
    elif status == 1:
        responseData['msg'] = 'record not deleted. The passed id does not exist.'
    
    response = make_response(jsonify(responseData), statusCode, {'content-type': 'application/json'})
    return response

app.register_blueprint(api)

@app.route('/')
def index():
    return 'Hello, World!'


if __name__ == '__main__':
    print("Sensor2Cloud DEMO")
    print("-" * 12)
    db.create_all()

    app.run(debug=True, host="0.0.0.0", port=5000)