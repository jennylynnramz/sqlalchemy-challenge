import numpy as np
import sqlalchemy
from flask import Flask, jsonify, request
from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


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
        
        f"<body style='background-color:#618f47;'>"
        f"<b><center><h2><font face=Arial color=#cd141e>&#127802; Hawaii Weather Data! &#127802;</h2></font></b>"
        f"<u><h3><font face=Arial color=#cd141e>Available Data:</u></h3></font>"
        f"<a href='/api/v1.0/precipitation'><font face=Arial>Precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'><font face=Arial>Stations</a><br/>"
        f"<a href='/api/v1.0/tobs'><font face=Arial>Temperature Observations</a><br/>"
        f"<a href='/api/v1.0/start'><font face=Arial>Temperature on a date</a><br/>"
        f"<a href='/api/v1.0/start_end'><font face=Arial>Temperature Between Two Dates</a><br/>"
        f"<a href='humuhumunukunukuapuaa'><font face=Arial color=#618f47>Humuhumunukunukuapua'a</a><br/>"

        f"<img src='https://www.hawaiinewsnow.com/resizer/V7K4u3jb7910e_D5Yu5578GGKJ8=/1200x600/arc-anglerfish-arc2-prod-raycom.s3.amazonaws.com/public/CYYLZOEQHBDBHGHVTZFM6FZ4DI.jpg'>"
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

@app.route("/api/v1.0/start")
def start():
    return """
        <html><body>
        <font face=Arial>
        <center>
             <form action="/start_date">
                 <label>Date:</label><input type="date" id="date_start" name="date_start" max="2017-08-23" min="2010-01-01"><br>
                 <input type='submit' value='Continue'>
             </form>
        </font></center>
         </body></html>
         """
    
@app.route("/start_date")   
def start_date(): 
    date_start = request.args.get('date_start')
    #return (date_start)
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= date_start).order_by(Measurement.date).all()
    session.close()
    start_temp_data = list(np.ravel(results))
    return jsonify(start_temp_data)

@app.route("/api/v1.0/start_end")
def start_end():
    return """
         <html><body><center>
         <body style='background-color:#618f47;'>
             <form action="/start_end_date">
                <font face=Arial>
                <label>Start Date:</label><input type="date" id="date_start" name="date_start" max="2017-08-23" min="2010-01-01"><br>
                <label>End Date:</label><input type="date" id="date_end" name="date_end" max="2017-08-23" min="2010-01-01"><br>
                <input type='submit' value='Continue'>
             </form>
             </font></center>
         </body></html>
         """

@app.route("/start_end_date")   
def start_end_date(): 
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    #return (date_start)
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date.between(date_start, date_end)).all()
    session.close()
    start_end_temp_data = list(np.ravel(results))
    return jsonify(start_end_temp_data)

@app.route("/humuhumunukunukuapuaa")
def humuhumunukunukuapuaa():
    return f"<body style='background-color:#618f47;'><center><img src='https://meme.xyz/uploads/posts/t/59116-people-who-were-sleeping-in-titanic-fish-helo.jpg'></center>"


if __name__ == "__main__":
    app.run(debug=True)
