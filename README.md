# Sensor Data Store API + WebApp

## Setup
| Windows Powershell
```Powershell
    > python -m venv venv
    > venv/Scripts/Activate.ps1
    (venv)> pip install -r requirements.txt
    (venv)> python main.py
```

<br><br><br>

## **API Documentation**

<br>

### **Test API conn**
Returns a simple message to check API conn
* **URL**<br>
    /api
* **Methods:**<br>
    `GET`
* **URL Params:**<br>
    None
* **Data Params:**<br>
    None
* **Success Response:**<br>
    * **Code:** 200<br>
    **Content:**<br>
    `{ msg: "This is Sensor Data Store API..." }`
* **Error Response:**<br>
    None
* **Sample Call:**<br>
    ```JavaScript
        fetch('/api')
        .then(response => response.json())
        .then(data => console.log('success', data))
        .catch(err => console.error('Error:', err));
    ```

<br>

### **Show Values**
Returns json data of list of values
* **URL**<br>
    /api/sensor_values
* **Methods:**<br>
    `GET`
* **URL Params:**<br>
    None
* **Data Params:**<br>
    None
* **Success Response:**<br>
    * **Code:** 200<br>
    **Content:**<br> 
    `{ data: [ { id: 2, sensor_value: 5.62, data_added: "2022-02-26 02:03:58" }, ... ], msg: "all the data fetched." }`
* **Error Response:**<br>
    None
* **Sample Call:**<br>
    ```JavaScript
        fetch('/api/sensor_values')
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(err => console.error(err));
    ```

<br>

### **Show Value**
Returns json data of a single value
* **URL**<br>
    /api/sensor_values/:id
* **Method:**<br>
    `GET`
* **URL Params:**<br>
    **Required:**<br>
    `id=[integer]`
* **Data Params:**<br>
    None
* **Success Response:**<br>
    * **Code:** 200<br>
    **Content:**<br> 
    `{ data: { "date added": "2021-11-11 18:36:56", id: 1, "sensor value": 0.2 }, msg: "data with id 1 fetched." }`
* **Error Response:**<br>
    * **Code:** 404<br>
    **Content:**<br>
    `{ msg: "no such id exist." }`

    OR

    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: "something went wrong." }`
* **Sample Call:**<br>
    ```JavaScript
        fetch('/api/sensor_values/1'})
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(err => console.error(err));
    ```

<br>

### **Add Value**
Adds a new record with passed value
* **URL**<br>
    /api/sensor_values
* **Method:**<br>
    `POST`
* **URL Params:**<br>
    None
* **Data Params:**<br>
    **Required:**<br>
    value=[Float]
* **Success Response:**<br>
    * **Code:** 201<br>
    **Content:**<br>
    `{ id: 3, msg: "record successfully added." }`
* **Error Response:**<br>
    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: "record not created. send valid sensor value." }`

    OR

    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: "record not created. send the sensor value in json object with 'value' as key." }`

    OR

    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: "record not created. send json objects, set Content-Type to application/json" }`

    OR

    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: "something went wrong." }`
* **Sample Call:**
    ```JavaScript
        fetch('/api/sensor_values', {
            method: 'POST',
            header: {
                'Content-Type': 'application/json',
            },
            body: {
                'value': 3.29,
            }
        })
        .then(response => response.json())
        .then(data => console.log('success', data))
        .catch(err => console.error('Error:', err));

    ```

<br>

### Update Value
Updates previously added record of id with the passed value
* **URL**<br>
    /api/sensor_values
* **Method:**<br>
    `PUT`
* **URL Params:**<br>
    **Required:**<br>
    id=[Integer]
* **Data Params:**<br>
    **Required:**<br>
    value=[Float]
* **Success Response:**
    * **Code:** 200<br>
    **Content:**<br>
    `{ msg: "record with id 2 successfully updated." }`
* **Error Response:**<br>
    * **Code:** 404<br>
    **Content:**<br>
    `{ msg: "record not updated. the sent id does not exist" }`

    OR

    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: "record not updated. send valid sensor value." }`

    OR

    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: "record not updated. send the sensor value in json object with 'value' as key." }`

    OR

    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: "record not updated. send json objects, set Content-Type to application/json" }`

    OR

    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: "something went wrong." }`
* **Sample Call:**
    ```JavaScript
        fetch('/api/sensor_values/2', {
            method: 'PUT',
            header: {
                'Content-Type': 'applicaiton/json',
            },
            body: {
                'value': 2.89,
            }
        })
        .then(response => response.json())
        .then(data => console.log('success', data))
        .catch(err => console.error('Error: ', err));
    ```


<br>

### Delete Value
Deletes the record with passed id
* **URL**<br>
    /api/sensor_values
* **Method:**<br>
    `DELETE`
* **URL Params:**<br>
    **Required:**<br>
    id=[Integer]
* **Data Params:**<br>
    None
* **Success Response:**
    * **Code:** 200<br>
    **Content:**<br>
    `{ id: 3, msg: "record successfully deleted." }`
* **Error Response:**
    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: 'record not deleted. The passed id does not exist. }`

    OR

    * **Code:** 400<br>
    **Content:**<br>
    `{ msg: "something went wrong." }`
* **Sample Call:**
    ```JavaScript
        fetch('/api/sensor_values/3', {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => console.log('success', data))
        .catch(err => console.error('Error:', err));
    ```