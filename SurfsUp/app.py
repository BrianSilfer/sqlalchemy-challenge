# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session, query
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import json
#################################################
# Database Setup
#################################################
# create engine to hawaii.sqlite
#engine = create_engine("sqlite:///Resources/hawaii.sqlite")
engine = create_engine("sqlite://///Users/briansilfer/Desktop/Desktop/git/sqlalchemy-challenge/SurfsUp/Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement

Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def Homepage():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start>/<end>"

    )

@app.route("/api/v1.0/precipitation")
def precipitation_measurements():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Convert results from precipitaion analysis"""
    # Query all last 12 months of precipitation data
    results = session.query(Measurement).filter(Measurement.date >= "2016-08-23",Measurement.date <= "2017-07-23").all()
    #setup empty dictionary
    last_12_dict = []
    #for loop to collect each row of the query results to create a list of dictionaries
    for row in results:
        #define empty dictionary for precipitation results
        row_dict = {}
        # Extract date and precipitation values from the row
        date = row.date
        precipitation = row.prcp
        # Set date as key and Precipitation as value in row_dict
        row_dict[date] = precipitation
        #append dict to list of dictinoaries
        last_12_dict.append(row_dict)
    #Convert python object into json object
    json_data = json.dumps(last_12_dict)
    #return Json data
    return jsonify(json_data)
    #close session
    session.close()

@app.route("/api/v1.0/stations")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #query to find all station names
    active_stations = session.query(Measurement.station).group_by(Measurement.station).all()
    # Extracting Data from Query
    station_list = [station[0] for station in active_stations]
    #Convert python object into json object
    json_stations = json.dumps(station_list)
    #return JSON list
    return jsonify(json_stations)
    #close session
    session.close()

@app.route("/api/v1.0/tobs")
def temps():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    #Query to return data after 2016 -11-09
    query = session.query(Measurement.tobs).filter(Measurement.date >= "2016-11-09").all()
    
    tobs = [row[0] for row in query]
    json_temp = json.dumps(tobs)
    #return JSON list
    return jsonify(json_temp)
    #close session
    session.close()

@app.route("/api/v1.0/<start>/<end>")
def temp_dates(start,end):
    # Create our session (link) from Python to the DB
    session = Session(engine)
     # Set Start and end Dates

    #Query the dates and temperature observations of the most-active station for the previous year of data.
    #find Min, max, avg from each date
    most_active = session.query(Measurement.date,\
    func.min(Measurement.tobs).label('TMIN'),
    func.avg(Measurement.tobs).label('TAVG'),
    func.max(Measurement.tobs).label('TMAX'))\
    .filter(Measurement.date >= start, Measurement.date <= end).all()
    #extract query data
    temps_list = [{'date': row.date, 'TMIN': row.TMIN,'TAVG': row.TAVG, 'TMAX': row.TMAX} for row in most_active]
    #Convert python object into json object
    json_list = json.dumps(temps_list)
    #return JSON list
    return jsonify(json_list)
    #close session
    session.close()

if __name__ == "__main__":
    app.run(debug=True)