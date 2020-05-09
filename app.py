from flask import Flask, jsonify
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

#Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station




@app.route("/")
def index():
    return (
        f"<b>Welcome to Hawaii! <font-size = 50>&#127802;</font></b><br/>"
        f"<u>Available Routes:</u><br/>"
        f"<a href='/api/v1.0/precipitation'>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>Temperature Observations</a><br/>"
        f"<a href='/api/v1.0/<start>'>Start</a><br/>"
        f"<a href='/api/v1.0/<start>/<end>'>Start and End</a><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query date and precipitation
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
    session.close()
    # Create a dictionary from the row data and append to a list of date_prcp
    date_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        date_prcp.append(prcp_dict)
    return jsonify(date_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    # Query all stations
    results = session.query(Station.name, Station.station).all()
    session.close()
    # Convert list of tuples into normal list
    station_names = list(np.ravel(results))
    return jsonify(station_names)

@app.route("/api/v1.0/tobs")
def temp_observations():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == 'USC00519281').\
    order_by(Measurement.date).all()
    session.close()
    station_activity = list(np.ravel(results))
    return jsonify(station_activity)

#@app.route("/api/v1.0/<start>")
#def start():





if __name__ == "__main__":
    app.run(debug=True)