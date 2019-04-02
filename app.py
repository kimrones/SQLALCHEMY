import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///titanic.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger

# Create our session (link) from Python to the DB
session = Session(engine)


app = Flask(_name_)



@app.route("/")
def home():
    return (
        f"Welcome!<br/>"
        f"Available routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    precip_data = session.query(Measurement.prcp, Measurement.date).filter(Measurement.date >= '2016-01-01').filter(Measurement.date <= '2016-31-12').all()
     
    results = [] 
    for prcp, date in precip_data:
        prcp_dict = {}
        prcp_dict["prcp"] = prcp
        prcp_dict["date"] = date
        results.append(prcp_dict)

    return jsonify(results)

@app.route("/api/v1.0/stations")
def stations():
        station_data = session.query(Station.station).all()

        results = list(np.ravel(station_data))

        return jsonify(results)

@app.route("/api/v1.0/tobs")
def tobs():
   tobs_data = session.query(Measurement.tobs).filter(Measurement.date >= '2016-01-01').filter(Measurement.date <= '2016-31-12').all() 

   results = list(np.ravel(tobs_data))

   return jsonify(results)


@app.route("/api/v1.0/<start>")
def start(begin):
    start_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= begin).all()
    
    results = list(np.ravel(start_data))

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def start_end(begin, end):
    start_end_data = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= begin).filter(Measurement.date <= end).all()

    results = list(np.ravel(start_end_data))

    return jsonify(results)


if _name_ == "_main_":
    app.run(debug=True)


