# Import the dependencies.
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

# Homepage
# List all the available routes.
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Welcome to the Climate App!⛅🌦️<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

# precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    year_from_last_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= year_from_last_date).all()
    
    session.close()

    precipitation_list = []
    for date, prcp in precipitation:
        precipitation_list.append({"date": date, "precipitation": prcp})

    return jsonify(precipitation_list)

# stations route
@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    count_active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    session.close()

    # Return a JSON list of stations from the dataset
    station_list = []
    for station in count_active_stations:
        station_list.append({"station": station[0], "active count": station[1]})

    return jsonify(station_list)

# tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    most_active_station = session.query(Measurement.station, func.count(Measurement.station)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]
    
    year_from_last_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    temperature_query = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= year_from_last_date).all()
    
    session.close()
    
    temperature_list = []
    for date, tobs in temperature_query:
        temperature_list.append({"date": date, "tobs": tobs})

    return jsonify(temperature_list)

# start route
@app.route("/api/v1.0/<start>")
def temperature_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    
    
    session.close()
    
    temperature_start_list = []
    for min, max, avg in temperature_stats:
        temperature_start_list.append({"start date": start_date.strftime("%Y-%m-%d"), "end date": most_recent_date[0], 
                                       "minimum temperature": min, "maximum temperature": max, "average temperature": avg})
        

    return jsonify(temperature_start_list)

# start/end route
@app.route("/api/v1.0/<start>/<end>")
def temperature_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    start_date = dt.datetime.strptime(start, "%Y-%m-%d")
    end_date = dt.datetime.strptime(end, "%Y-%m-%d")
    temperature_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date, Measurement.date <= end_date).all()
    
    session.close()

    temperature_start_end_list = []
    for min_temp, max_temp, avg_temp in temperature_stats:
        temperature_start_end_list.append({
            "start_date": start_date,
            "end_date": end_date,
            "min_temperature": min_temp,
            "max_temperature": max_temp,
            "avg_temperature": avg_temp
        })

    return jsonify(temperature_start_end_list)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)











