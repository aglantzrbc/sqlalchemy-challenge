# Import the dependencies.
import sqlalchemy

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify 

import numpy as np
import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

# Print the address and IP when the application starts
@app.before_first_request
def print_server_info():
    server_address = app.config.get('SERVER_NAME')
    server_ip = app.config.get('SERVER_HOST')
    print(f"Flask application is running on {server_address} ({server_ip})")


#################################################
# Flask Routes
#################################################

# Create root ("/") route
@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes for Hawaii Weather Data:<br/>"
        f"-- Daily Precipitation Totals for Last Year: <a href=\"/api/v1.0/precipitation\" target=\"_blank\">/api/v1.0/precipitation</a><br/>"
        f"-- Active Weather Stations: <a href=\"/api/v1.0/stations\" target=\"_blank\">/api/v1.0/stations</a><br/>"
        f"-- Daily Temperature Observations for Station USC00519281 for Last Year: <a href=\"/api/v1.0/tobs\" target=\"_blank\">/api/v1.0/tobs</a><br/>"
        f"-- Min, Average & Max Temperatures for Date Range: /api/v1.0/trip/yyyy-mm-dd/yyyy-mm-dd<br>"
        f"(Note: to access values between a start and end data range, enter both dates using format: YYYY-mm-dd/YYYY-mm-dd)"
    )
