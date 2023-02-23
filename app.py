#import dependencies
import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve last 12 months of precipitation data"""
    # Query last 12 months of precipitation data
    last_date = dt.date(2017, 8, 23)
    last_year = dt.date(last_date.year -1, last_date.month, last_date.day)
    data = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()

    session.close()

    # Create a dictionary using date as the key and prcp as the value
    all_precipitation = []
    for date, prcp in data:
        prcp_dict = {}
        prcp_dict["Date"] = date
        prcp_dict["Precipitation"] = prcp
        all_precipitation.append(prcp_dict)

    return jsonify(all_precipitation)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve list of stations"""
    # Query list of stations
    stations = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary using station
    all_stations = []
    for station, name in stations:
        station_dict = {}
        station_dict["Station"] = station
        station_dict["Name"] = name
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve last 12 months of temperature observations from USC00519281"""
    # Query the dates and temperature observations of the most-active station for the previous year of data
    last_date = dt.date(2017, 8, 23)
    last_year = dt.date(last_date.year -1, last_date.month, last_date.day)
    temp = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= last_year, Measurement.station == 'USC00519281').all()

    session.close()

    # Create a dictionary using date as the key and tobs as the value
    all_tobs = []
    for date, tobs in temp:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Tobs"] = tobs
        all_tobs.append(tobs_dict)

    return jsonify(all_tobs)

@app.route("/api/v1.0/<start>")
def start_date(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve min, avg, and max temperature for a specified start date"""
    # Query min, avg, and max temperature for a specified start date
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    session.close()

    # Create a dictionary 
    all_stats = []
    for min, avg, max in results:
        stats_dict = {}
        stats_dict["Min"] = min
        stats_dict["Avg"] = avg
        stats_dict["Max"] = max
        all_stats.append(stats_dict)

    return jsonify(all_stats)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Retrieve min, avg, and max temperature for a specified start date"""
    # Query min, avg, and max temperature for a specified start and end date
    range = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    session.close()

    # Create a dictionary 
    all_stats = []
    for min, avg, max in range:
        stats_dict = {}
        stats_dict["Min"] = min
        stats_dict["Avg"] = avg
        stats_dict["Max"] = max
        all_stats.append(stats_dict)

    return jsonify(all_stats)

if __name__ == '__main__':
    app.run(debug=True)
