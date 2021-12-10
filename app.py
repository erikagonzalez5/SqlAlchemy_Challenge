import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


# Database setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflecting an existing database into a new model
Base = automap_base()

# Reflecting the tables
Base.prepare(engine, reflect=True)

# Save references to the table
Measurement = Base.classes.measurement
Station = Base.classes.station


# Flask setup
app = Flask(__name__)

# Flask routes#

# Creating index
@app.route("/")
def welcome():
    return(
        f"All Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

# Creating precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
# Create our session (link) from Python to the DB
    session = Session(engine)
# Query results    
    one_year = dt.date(2017, 8, 23) -dt.timedelta(days=365)
    data_precipitation = session.query(Measurement.date, func.max(Measurement.prcp)).\
    filter(Measurement.date >= one_year).\
    group_by(Measurement.date).\
    order_by(Measurement.date).all()


# Create a dictionary from the row data and append to a list of prcp_totals and return JSON
    prcp_totals = []
    for data in data_precipitation:
        prcp_dict = {}
        prcp_dict["date"] = data[0]
        prcp_dict["prcp"] = data[1]
        prcp_totals.append(prcp_dict)

    return jsonify(list(prcp_totals))

# Creating stations route
@app.route("/api/v1.0/stations")
def stations():
# Create our session (link) from Python to the DB
    session = Session(engine)
# Query results    
    stations = session.query(Station.name, Station.station).all()
# Convert list of tuples into normal list
    all_names = list(np.ravel(stations))

    return jsonify(all_names)

# Creating tobs route
@app.route("/api/v1.0/tobs")
def tobs():
# Create our session (link) from Python to the DB
    session = Session(engine)
# Query results
    temp_obs = session.query(Measurement.station, Measurement.date, Measurement.tobs).\
    filter(Measurement.station == "USC00519281").\
    filter(Measurement.date > "2016-08-23").\
    order_by(Measurement.date).all()

# Create a dictionary from the row data and append to a list of 
    date_temp_obs = []
    for results in temp_obs:
        date_temp_dict = {}
        date_temp_dict["date"] = results[1]
        date_temp_dict["tobs"] = results[2]
        date_temp_obs.append(date_temp_dict)

    return jsonify(date_temp_obs)

# Creating <start> route
@app.route("/api/v1.0/<start>")
def start_date(start):
# Create our session (link) from Python to the DB
    session = Session(engine)
# Query results
    start_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= "2010-01-01").\
    group_by(Measurement.date).all()
# Convert list of tuples into normal list
    start_temps_list = list(np.ravel(start_temps))

    return jsonify(start_temps_list)

# Creating <start>/<end> route
@app.route("/api/v1.0/<start>/<end>")
def start_end(start,end):
# Create our session (link) from Python to the DB
    session = Session(engine)
# Query results
    start_end_temps = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= "2010-01-01").\
    filter(Measurement.date <= "2017-08-03").all()
# Convert list of tuples into normal list
    start_end_list = list(np.ravel(start_end_temps))

    return jsonify(start_end_list)

    

# Defining main behavior
if __name__ == "__main__":
    app.run(debug=True)
