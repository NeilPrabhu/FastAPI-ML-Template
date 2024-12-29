import pytest
from fastapi.testclient import TestClient
from datetime import datetime

from src.main import app
import json

data = {"houses" : [{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":12.29,"longitude":37.82,"population":100000},{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":12.29,"longitude":37.82,"population":100000}]}
data_some_outputs = {"houses" : [{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3},{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"population":100000}]}
data_incorrect_long = {"houses" : [{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":12.29,"longitude":37.82,"population":100000},{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":12.29,"longitude":32227.82,"population":100000}]}
data_incorrect_lat = {"houses" : [{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":12.29,"longitude":37.82,"population":100000},{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":33333.29,"longitude":32227.82,"population":100000}]}
data_incorrect_datatype = {"houses" : [{"income":'abcd',"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":12.29,"longitude":37.82,"population":100000},{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":33333.29,"longitude":32227.82,"population":100000}]}
data_incorrect_datatype = {"houses" : [{"income":2222,"house_age":20.2,"avg_room":2.3,"avg_bedroom":-3,"avg_occup":4,"lattitude":12.29,"longitude":37.82,"population":100000},{"income":12000.0,"house_age":20.2,"avg_room":2.3,"avg_bedroom":3,"avg_occup":4,"lattitude":33333.29,"longitude":32227.82,"population":100000}]}


client = TestClient(app)
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def test_read_main_root():
    response = client.get("/")
    assert response.status_code == 501
    assert response.json() == {"detail":"Not Implemented"}

def test_read_main_hello_null():
    response = client.get("/hello")
    assert response.status_code == 400
    assert response.json() == {"detail":"No value passed"}

def test_read_main_hello():
    response = client.get("/hello?name=test")
    assert response.status_code == 200
    assert response.json() == {"message":"Hello test"}

def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200

def test_dne():
    response = client.get("/dne")
    assert response.status_code == 404

def test_predict_all_outputs():
    response = client.post("/predict", json = data )
    assert response.status_code == 200
    response_json = response.json()
    assert is_float(response_json["prediction"][0])
    assert is_float(response_json["prediction"][1])

def test_predict_some_outputs():
    response = client.post("/predict", json = data )    
    assert response.status_code == 200
    response_json = response.json()
    assert is_float(response_json["prediction"][0])
    assert is_float(response_json["prediction"][1])

def test_predict_null():
    response = client.post("/predict")
    assert response.status_code == 422

def test_predict_incorrect_datatype():
    response = client.post("/predict", json = data_incorrect_datatype)
    assert response.status_code == 422

def test_predict_incorrect_lattitude():
    response = client.post("/predict", json = data_incorrect_lat)    
    assert response.status_code == 422

def test_predict_incorrect_longitude():
    response = client.post("/predict", json = data_incorrect_long)   
    assert response.status_code == 422

def test_predict_negative_value():
    response = client.post("/predict", json = data_incorrect_long)   
    assert response.status_code == 422

'''
def test_health_check():
    response = client.get("/health")
    response_json = response.json()
    response_json["time"] = datetime.fromisoformat(response_json["time"])
    assert isinstance(response_json["time"], datetime)

'''