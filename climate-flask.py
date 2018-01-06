# design a flask api
from flask import Flask
from flask import jsonify

# Python SQL toolkit and Object Relational Mapper
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, date
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func, extract
import numpy as np

# Create Database Connection
engine = create_engine('sqlite:///hawaii-new.sqlite')

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(engine,reflect=True)

# create a reference of the classes
Station=Base.classes.stations
# create a reference of the classes
Measurement=Base.classes.measurements

# Using the references to classes, start querying the database
from sqlalchemy.orm import Session
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

#Session management with scoped session (Session that is universal across all threads in the code)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)
some_session = Session()


# Querying the database 
prcp_data = some_session.query(Measurement.date,Measurement.prcp).filter(Measurement.date >= '2016-08-01').filter(Measurement.date <='2017-08-01').all()
# Unpacking the tuple into separate lists
dates_p=[res[0] for res in prcp_data]
prcp_p = [res[1] for res in prcp_data]
# combining the above lists into dictionary
prcp_dict = dict(zip(dates_p,prcp_p))

# querying the db
stations = some_session.query(Station.station)
# unpacking the tuple into separate lists
station = [res[0] for res in stations]

temp_obs = some_session.query(Measurement.tobs).filter(Measurement.date >= '2016-08-01').filter(Measurement.date <='2017-08-01').all()
temp = [res[0] for res in temp_obs]


# Create an app, being sure to pass __name__
climate_flask = Flask(__name__)

# Define what to do when a user hits the index route
@climate_flask.route("/")
def home():
    print("Server received request for 'Home' page...")
    return "Hello - Welcome to my climate API"


@climate_flask.route("/api/v1.0/preciptation")
def preciptation():
    print("Server received request for 'Preciptation' data...")
    return jsonify(prcp_dict)

@climate_flask.route("/api/v1.0/stations")
def stations():
    print("Server received request for 'stations' data...")
    return jsonify(station)


@climate_flask.route("/api/v1.0/tobs")
def tobs():
    print("Server received request for 'Temperature Observations' data...")
    return jsonify(temp)


@climate_flask.route("/api/v1.0/<start_date>")
def temps(start_date):
    return jsonify(Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all())


@climate_flask.route("/api/v1.0/<start_date>/<end_date>")
def temp_end(start_date,end_date):
    return jsonify(Session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date<= end_date).all())

if __name__ == "__main__":
    climate_flask.run(debug=True)