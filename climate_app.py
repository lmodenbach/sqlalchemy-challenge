import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt

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
        f"Available Routes:<br/><br/>"
        f"See most recent 12 months of precipitation data:<br/>"
        f"/api/v1.0/precipitation<br/><br/>"
        f"See station information:<br/>"
        f"/api/v1.0/stations<br/><br/>"
        f"See second most recent 12 months of temperature data from the most active station:<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"You choose the start date (yyyy-mm-dd) which ends at most recent measurements, see minimum/maximum/average temperatures:<br/>"
        f"/api/v1.0/start<br/><br/>"
        f"You choose the start and end date(yyyy-mm-dd/yyyy-mm-dd), see minimum/maximum/average temperatures:<br/>"
        f"/api/v1.0/start/end"
        )


@app.route("/api/v1.0/precipitation")
def precipitation():
    
    previous = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp, Station.name).\
        filter(Measurement.date >= previous).all()

    precip = []    
    for date, prcp, name in results:
        precip_dict = {}
        precip_dict["Date"] = date
        precip_dict["Precipitation"] = prcp
        precip_dict["Name"] = name
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
    
    previous = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    pre_previous = previous - dt.timedelta(days=365)
    temps_and_station = session.query(Measurement.station, func.count(Measurement.tobs)).\
                  filter(Measurement.date >= previous).\
                  group_by(Measurement.station).\
                  order_by(func.count(Measurement.tobs).desc()).first()
    
    results = session.query(Measurement.tobs).\
              filter(Measurement.station == temps_and_station[0]).\
              filter(Measurement.date >= pre_previous).\
              filter(Measurement.date < previous).all()

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