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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"YOU CHOOSE START OF PERIOD<br/>"
        f"/api/v1.0/start<br/>"
        f"YOU CHOOSE START AND END OF PERIOD<br/>"
        f"/api/v1.0/start/end"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    results = session.query(Measurement.date, Measurement.prcp).all()

    precip = []    
    for date, prcp in results:
        precip_dict = {}
        precip_dict["date"] = date
        precip_dict["prcp"] = prcp
        precip.append(precip_dict)

    return jsonify(precip)
    session.close()
       


@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(Station.name).all()
    
    return jsonify(results)
    session.close()



@app.route("/api/v1.0/tobs")
def tobs():
    
    most_temps_and_station = session.query(Measurement.station, func.count(Measurement.tobs)).\
                  group_by(Measurement.station).\
                  order_by(func.count(Measurement.tobs).desc()).first()
    
    results = session.query(Measurement.tobs).\
              filter(Measurement.station == most_temps_and_station[0]).all()

    return jsonify(results)
    session.close()



@app.route("/api/v1.0/<start>")
def start(start):
    
    min = session.query(func.min(Measurement.tobs)).\
           filter(Measurement.date >= start).all()
    
    max = session.query(func.max(Measurement.tobs)).\
           filter(Measurement.date >= start).all()

    avg = session.query(func.avg(Measurement.tobs)).\
           filter(Measurement.date >= start).all()

    stats = [{"Min Temp: ":min}, {"Max Temp: ":max}, {"Avg Temp: ":avg}]    
    
    return jsonify(stats)
    session.close()



@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    
    min = session.query(func.min(Measurement.tobs)).\
           filter(Measurement.date >= start).\
           filter(Measurement.date <= end).all()

    max = session.query(func.max(Measurement.tobs)).\
           filter(Measurement.date >= start).\
           filter(Measurement.date <= end).all()

    avg = session.query(func.avg(Measurement.tobs)).\
           filter(Measurement.date >= start).\
           filter(Measurement.date <= end).all()

    stats = [{"Min Temp: ":min}, {"Max Temp: ":max}, {"Avg Temp: ":avg}]    
    
    return jsonify(stats)
    session.close()



if __name__ == '__main__':
    app.run(debug=True)