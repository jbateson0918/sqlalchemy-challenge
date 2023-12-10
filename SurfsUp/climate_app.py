# Import the dependencies.
import datetime as dt
import os
from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


#################################################
# Database Setup
#################################################
os.chdir(os.path.dirname(os.path.realpath(__file__)))
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
# reflect the tables
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station



#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# HTML Routes
#################################################
@app.route("/")
def home():
    return ("Home Page<br/>"
            f"/api/v1.0/precipitation<br/>"
            f"/api/v1.0/stations<br/>"
            f"/api/v1.0/tobs<br/>"
            f"/api/v1.0/<start><br/>"
            f"/api/v1.0/<start>/<end><br/>")


#################################################
# API Routes
#################################################
@app.route("/api/v1.0/precipitation")
def percipiatation(): 
    # Create our session (link) from Python to the DB
    session = Session(engine)
    recent_date_str = session.query(Measurement.date)\
        .order_by(Measurement.date.desc())\
        .first()[0]
    recent_date = dt.date.fromisoformat(recent_date_str)
    year_ago = recent_date - dt.timedelta(days=365)
    year_data = session.query(Measurement.date, func.avg(Measurement.prcp))\
        .filter(Measurement.date >= year_ago)\
        .group_by(Measurement.date)\
        .order_by(Measurement.date)\
        .all()
    
    precipitation = {}
    for row in year_data:
        date = row[0]
        prcp = row[1]
        precipitation[date] = prcp
    
    session.close()
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = session.query(Station.name)\
        .group_by(Station.name)\
        .order_by(Station.name)\
        .all()
    
    station_lists = []
    for row in stations:
        station_lists = row[0]

    session.close()
    return jsonify(station_lists)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    year_temp_data = session.query(Measurement.date, Measurement.station, Measurement.tobs)\
        .filter(Measurement.date >= year_ago)\
        .filter(Measurement.station == "USC00519281")\
        .all()
    recent_date_str = session.query(Measurement.date)\
        .order_by(Measurement.date.desc())\
        .first()[0]
    recent_date = dt.date.fromisoformat(recent_date_str)
    year_ago = recent_date - dt.timedelta(days=365)


    observation = []
    for row in year_temp_data:
            date = row[0]
            station = row[1]
            tops = row[2]
            precipitation[date] = tops

    session.close()
    return jsonify(observation)

@app.route("/api/v1.0/<start>")
def tstats(start):
    session = Session(engine)
    year_temp_stats = session.query(min(Measurement.tobs), max(Measurement.tobs), avg(Measurement.tobs))\
        .filter(Measurement.date >= year_ago)\
        .filter(Measurement.station == "USC00519281")\
        .all()
    data_sum = {"Maximum": f"{year_temp_stats[0][1]} F", "Minimum": f"{year_temp_stats[0][0]} F", "Average": f"{year_temp_stats[0][2]} F"}

    session.close()
    return jsonify(data_sum)

@app.route("/api/v1.0/<start>/<end>")
def tstats_st_end(start,end):
    st_end_stats = session.query(Measurement.date, Measurement.station, Measurement.tobs)\
        .filter(Measurement.date >= year_ago)\
        .filter(Measurement.station == "USC00519281")\
        .all()
    st_end_sum = {"Maximum": f"{st_end_stats[0][1]} F", "Minimum": f"{st_end_stats[0][0]} F", "Average": f"{st_end_stats[0][2]} F"}

    session.close()
    return jsonify(st_end_stats)
if __name__ == '__main__':
    app.run(debug=True)