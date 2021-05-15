import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
           )

@app.route("/api/v1.0/precipitation")
def precipitation():
     (
        previous = dt.date(2017, 8, 23) - dt.timedelta(days=365)
        results = session.query(Measurement.date, Measurement.prcp).\
            filter(Measurement.date >= previous).all()
       return jsonify() 
           )

if __name__ == '__main__':
    app.run(debug=True)