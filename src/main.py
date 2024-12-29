from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, ValidationError, validator, root_validator#, field_serializer, model_serializer

from datetime import datetime
from sklearn import preprocessing
from sklearn.feature_extraction.text import CountVectorizer
from typing import List

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis

import joblib
import numpy as np
import json

class Houses(BaseModel):
    income: float
    house_age: float
    avg_room: float
    avg_bedroom: float
    population: float
    avg_occup: float
    longitude: float
    lattitude: float

    @validator('longitude')
    def check_longitude(cls, v):
        if v < -180.0 or v > 180.0:
            raise ValueError('longitude must be between -180 and 180')
        return v
    
    @validator('lattitude')
    def check_lattitude(cls, v):
        if v < -90.0 or v > 90.0:
            raise ValueError('lattitude must be between -90 and 90')
        return v
    
    @root_validator(pre=True)
    def check_non_neg(cls, values):
        income, house_age, avg_room, avg_bedroom, pop, avg_occup = \
        values.get('income'), values.get('house_age'), values.get('avg_room'), \
        values.get('avg_bedroom'), values.get('population'), values.get('avg_occup')

        if income < 0.0 or house_age < 0 or avg_room < 0.0 or avg_bedroom < 0.0 or \
            pop < 0.0 or avg_occup < 0.0:
            raise ValueError('all values (except long/lat) must be non-negative')
        return values

class Request(BaseModel):
    houses: List[Houses]
    '''
    @field_serializer('houses')
    def serialize_list(self, house: list):
        l = [[h.income, h.house_age, h.avg_room, h.avg_bedroom, h.population, h.avg_occup, h.longitude, h.lattitude] for h in house]
    '''

class Response(BaseModel):
    pred_price: List[float]

app = FastAPI()

model = joblib.load("trainer/model_pipeline.pkl")

@cache()
async def get_cache():
    return 1

@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://redis:6379", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")


@app.get("/", status_code=501)
async def root():
    raise HTTPException(status_code=501)

@app.get("/hello")
async def hello(name: str = ''):
    if name:
        return {"message": "Hello " + name}
    else:
        raise HTTPException(status_code=400, detail="No value passed")
    
@app.get("/health")
async def health():
    today = datetime.now()
    return {"time":today.isoformat()}

@app.post("/predict")
@cache(expire=60)
async def predict(req: Request):
    house_values = [list(dict(house_obj).values()) for house_obj in req.houses]
    x_values = np.array(house_values)
    x_norm = preprocessing.normalize(x_values)
    predictions = model.predict(x_norm)
    print(predictions)
    print(type(predictions))
    print(predictions.tolist())
    result = Response(pred_price=predictions.tolist())
    return {"prediction":result.pred_price}
