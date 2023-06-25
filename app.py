# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

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

# Save references to the measurement and station tables in the database
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

#################################################
# TASK: Create welcome route, then list all available api routes
# Create a welcome route
@app.route("/")
def welcome():
    # List all available api routes as hyperlinks, annotated for clarity
    return (
        "<h2>Available API Routes:</h2>"
        "<ul>"
        "<li><a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation</a></li>"
        "<li><a href=\"/api/v1.0/stations\">/api/v1.0/stations</a></li>"
        "<li><a href=\"/api/v1.0/tobs\">/api/v1.0/tobs</a></li>"
        "<li><a href=\"/api/v1.0/start\">/api/v1.0/start</a></li>"
        "</ul>"
        "<ul>"
        "<li>/api/v1.0/<strong>[start]</strong>/<strong>[end]</strong></li>"
        "</ul>"
        "<p><small><strong>Note:</strong> for the last route, replace <strong>[start]</strong> and <strong>[end]</strong> with start and end dates using the format: <strong>YYYY-mm-dd/YYYY-mm-dd</strong>.<br/>Copy and paste the result into your browser, preceded by '<strong>http://localhost:5000/</strong>'.<br/><em>Example:</em> <a href=\"/api/v1.0/2016-08-23/2017-08-23\">http://localhost:5000/api/v1.0/2016-08-23/2017-08-23</a>.</small></p>"

        "<p><small><strong>Note:</strong> All the links assume the user employs <strong>port 5000</strong> for Flask output.<br/>If not, the links won't work, and you'll have to paste each route into your browser preceded by '<strong>http://localhost:XXXX/</strong>', where '<strong>XXXX</strong>' is your port of choice.<br/><em>Example:</em> <a href=\"/api/v1.0/2016-08-23/2017-08-23\">http://localhost:XXXX/api/v1.0/start</a>.</small></p>"
    )

#################################################
'''TASK: Convert the query results from the precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using [date] as the key and [prcp] as the value. Return the JSON representation of the dictionary.'''
# Create a precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():

    # Establish session
    session = Session(engine)

    # Design a query to retrieve the last 12 months of precipitation data
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Close session
    session.close() 

    # Calculate the date one year from the last date in data set
    latest_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d')
    start_date = latest_date - dt.timedelta(days=365)

    # Query the Measurement table for precipitation data within the last 12 months
    precipitation_query_results = session.query(Measurement.prcp, Measurement.date).\
        filter(Measurement.date >= start_date).all()

    # Create a dictionary from the row data and append to a list of precipitation_query_values
    precipitaton_query_values = []
    for prcp, date in precipitation_query_results:
        precipitation_dict = {}
        precipitation_dict["precipitation"] = prcp
        precipitation_dict["date"] = date
        precipitaton_query_values.append(precipitation_dict)

    # Return a JSON list of precipitation_query_values
    return jsonify(precipitaton_query_values)

#################################################
# TASK: Return a JSON list of stations from the dataset
# Create a station route
@app.route("/api/v1.0/stations")
def station(): 

    # Establish session
    session = Session(engine)

    # Return a list of stations from the database
    station_query_results = session.query(Station.station,Station.id).all()

    # Close session
    session.close()  

    # Create a dictionary from the row data and append to a list of stations_values   
    stations_values = []
    for station, id in station_query_results:
        stations_values_dict = {}
        stations_values_dict['station'] = station
        stations_values_dict['id'] = id
        stations_values.append(stations_values_dict)

    # Return a JSON list of stations_values
    return jsonify (stations_values) 

#################################################
'''TASK: Query the dates and temperature observations of the most-active station for the previous year of data. Return a JSON list of temperature observations for the previous year.'''
# Create a tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Establish session
    session = Session(engine)

    # Retrieve the most recent date in the dataset
    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    latest_date = dt.datetime.strptime(latest_date[0], "%Y-%m-%d").date()

    # Calculate the date one year ago from the most recent date
    one_year_ago = latest_date - dt.timedelta(days=365)

    # Query the most active station for the temperature observations within the last year
    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()

    # Retrieve the temperature observations for the most active station within the last year
    tobs_results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station[0]).\
        filter(Measurement.date >= one_year_ago).all()

    session.close()

    # Create a list of dictionaries to store the date and temperature observations
    tobs_list = []
    for date, tobs in tobs_results:
        tobs_dict = {"date": date, "tobs": tobs}
        tobs_list.append(tobs_dict)

    # Return the JSON representation of the temperature observations
    return jsonify(tobs_list)

#################################################
# Create a route that when given the start date only, returns the minimum, average, and maximum temperature observed for all dates greater than or equal to the start date entered by a user

@app.route("/api/v1.0/<start>")
# Define function, set "start" date entered by user as parameter for start_date decorator 
def start_date(start):
    session = Session(engine) 

    """Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start date."""

    # Create query for minimum, average, and max tobs where query date is greater than or equal to the date the user submits in URL
    start_date_tobs_results = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    session.close() 

    # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_date_tobs_values =[]
    for min, avg, max in start_date_tobs_results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min"] = min
        start_date_tobs_dict["average"] = avg
        start_date_tobs_dict["max"] = max
        start_date_tobs_values.append(start_date_tobs_dict)
    
    return jsonify(start_date_tobs_values)

# Create a route that when given the start date only, returns the minimum, average, and maximum temperature observed for all dates greater than or equal to the start date entered by a user

@app.route("/api/v1.0/<start>/<end>")

# Define function, set start and end dates entered by user as parameters for start_end_date decorator
def Start_end_date(start, end):
    session = Session(engine)

    """Return a list of min, avg and max tobs between start and end dates entered"""
    
    # Create query for minimum, average, and max tobs where query date is greater than or equal to the start date and less than or equal to end date user submits in URL

    start_end_date_tobs_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    session.close()
  
    # Create a list of min,max,and average temps that will be appended with dictionary values for min, max, and avg tobs queried above
    start_end_tobs_date_values = []
    for min, avg, max in start_end_date_tobs_results:
        start_end_tobs_date_dict = {}
        start_end_tobs_date_dict["min_temp"] = min
        start_end_tobs_date_dict["avg_temp"] = avg
        start_end_tobs_date_dict["max_temp"] = max
        start_end_tobs_date_values.append(start_end_tobs_date_dict) 
    

    return jsonify(start_end_tobs_date_values)
   
if __name__ == '__main__':
    app.run(debug=True) 