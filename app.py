# Import the dependencies
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

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
''' Keeping the "Base" variable upper-lower case because this is what the automap function expects '''
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to the measurement and station tables in the database
''' Keeping the Station variable upper-lower case to prevent confusion with the function "station" and the attribute "Station.station" below '''
''' Keeping the Measurement variable upper-lower to maintain consistency with the concurrent Station variable '''

Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

# Create Flask application object
app = Flask(__name__)

#################################################
# Flask Routes
#################################################


#################################################
''' TASK /: Create welcome route, then list all available api routes '''
# Create a welcome route
@app.route("/")
def welcome():

    # List all available api routes as hyperlinks, annotated and with instructions for clarity
    return (
        "<h2>Available Hawaii Weather API Routes for JSON Data:</h2>"
        "<ul>"
        "<li>Last 12 months of precipitation data -- <a href=\"/api/v1.0/precipitation\">/api/v1.0/precipitation</a></li>"
        "<li>Details of temperature observation stations -- <a href=\"/api/v1.0/stations\">/api/v1.0/stations</a></li>"
        "<li>Last 12 months of temperature data from the most active temperature observation station -- <a href=\"/api/v1.0/tobs\">/api/v1.0/tobs</a></li>"
        "</ul>"
        "<ul>"
        "<li>Temperature benchmark data from variable date ranges -- /api/v1.0/<strong>[start]</strong>/<strong>[end]</strong></li>"
        "</ul>"
        "<p><small><strong>Note:</strong> for the last route, replace <strong>[start]</strong> and <strong>[end]</strong> with start and end dates using the format: <strong>YYYY-mm-dd/YYYY-mm-dd</strong>.<br/>Copy and paste the result into your browser, preceded by '<strong>http://localhost:5000/</strong>'.<br/><em>Example:</em> <a href=\"/api/v1.0/2016-08-23/2017-08-23\">http://localhost:5000/api/v1.0/2016-08-23/2017-08-23</a>.<br>Date ranges outside the scope of actual dates occurring in the dataset will default to the earliest and latest dates in the data.<br>If only one date is provided, the output will calculate from that date through the latest record in the dataset.</small></p>"

        "<p><small><strong>Note:</strong> All the links assume the user employs <strong>port 5000</strong> for Flask output.<br/>If not, the links won't work, and you'll have to paste each route into your browser preceded by '<strong>http://localhost:XXXX/</strong>', where '<strong>XXXX</strong>' is your port of choice.<br/><em>Example:</em> <a href=\"/api/v1.0/precipitation\">http://localhost:XXXX/api/v1.0/precipitation</a>.</small></p>"
    )


#################################################
''' TASK PRECIPITATION: Convert the query results from the precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using [date] as the key and [prcp] as the value. Return the JSON representation of the dictionary. '''
# Create a precipitation route using the app Flask object
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

    # Return a JSON list of precipitation query values
    return jsonify(precipitaton_query_values)


#################################################
''' TASK STATIONS: Return a JSON list of stations from the dataset '''
# Create a station route using the app Flask object
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

    # Return a JSON list of stations values
    return jsonify (stations_values) # quantity of stations: 9


#################################################
''' TASK TOBS: Query the dates and temperature observations of the most-active station for the previous year of data. Return a JSON list of temperature observations for the previous year. '''
# Create a tobs route using the app Flask object
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

    # Close session
    session.close()

    # Create a list of dictionaries to store the date and temperature observations
    tobs_list = []
    for date, tobs in tobs_results:
        tobs_dict = {"date": date, "tobs": tobs}
        tobs_list.append(tobs_dict)

    # Return the JSON representation of the temperature observations
    return jsonify(tobs_list)


#################################################
''' TASK START-END: Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range: '''
''' For a specified start, calculate the min, avg, and max for all the dates greater than or equal to the start date. '''
''' For a specified start date and end date, calculate the min, avg, and max for the dates from the start date to the end date, inclusive. '''
# Create a start-end route using the app Flask object
@app.route("/api/v1.0/<start>/<end>") # Decorator for when user provides both start and end dates
@app.route("/api/v1.0/<start>") # Decorator for when user provides only start date
def Start_end_date(start, end=None):

    # Establish session
    session = Session(engine)

    """ Return a list of min, avg, and max tobs between start and end dates entered """

    # Get the earliest and latest dates in the dataset
    earliest_date = session.query(func.min(Measurement.date)).scalar()
    latest_date = session.query(func.max(Measurement.date)).scalar()

    # Set default values for start and end dates if they are outside the dataset date range
    if start < earliest_date:
        start = earliest_date

    if end is None or end > latest_date:
        end = latest_date

    # Query for minimum, average, and maximum tobs within the specified date range
    start_end_date_tobs_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()

    # Close session
    session.close()

    # Create a list of dictionaries to store the temperature data
    start_end_tobs_date_values = []
    for min_temp, avg_temp, max_temp in start_end_date_tobs_results:
        tobs_dict = {
            "min_temp": min_temp,
            "avg_temp": avg_temp,
            "max_temp": max_temp
        }
        start_end_tobs_date_values.append(tobs_dict)

    # Return the JSON representation of the temperature observation data
    return jsonify(start_end_tobs_date_values)


#################################################
''' Make sure the Flask application is only run if the script is being executed directly, to prevent contaminating other Flask apps running simultaneously and to facilitate reusability '''
if __name__ == '__main__':
    app.run(debug=True) 