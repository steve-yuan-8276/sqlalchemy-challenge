# Import the dependencies.
import numpy as np
from flask import Flask, jsonify
import sqlalchemy as sa
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, and_, or_
from datetime import datetime as dt, timedelta

#################################################
# Database Setup
#################################################
engine = create_engine('sqlite:///../Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurements = Base.classes.measurement

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
def home():
    "List all available api routes."
    return (
        f"<b>Available Routes:</b><br/><br/>"
        f"<b>/api/v1.0/precipitation</b><br/>"
        f"- Returns JSON representation of the precipitation data for the last 12 months.<br/>"
        f"- Date as the key and precipitation as the value.<br/><br/>"
        f"<b>/api/v1.0/stations</b><br/>"
        f"- Returns JSON list of all stations from the dataset.<br/><br/>"
        f"<b>/api/v1.0/tobs</b><br/>"
        f"- Returns JSON list of temperature observations of the most-active station for the previous year.<br/><br/>"
        f"<b>/api/v1.0/&lt;start&gt;</b><br/>"
        f"- Returns JSON list of the minimum temperature, the average temperature, and the maximum temperature for all dates greater than or equal to the start date.<br/>"
        f"- Date format: YYYYMMDD<br/>"
        f"- Date Range:20100101-20170823<br/><br/>"
        f"<b>/api/v1.0/&lt;start&gt;/&lt;end&gt;</b><br/>"
        f"- Returns JSON list of the minimum temperature, the average temperature, and the maximum temperature for dates between the start and end date inclusive.<br/>"
        f"- Date format: YYYYMMDD<br/>"
        f"- Date Range:20100101-20170823<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create session from python to the DB
    session = Session(engine)

    #Find the most recent date in the data set.
    most_recent_date = (
        session.query(Measurements.date)
        .order_by(Measurements.date.desc())
        .limit(1)
        # Use the `.scalar()` method to execute the query and get a single result. This will return a single value from the first column of the query.
        .scalar()
    )

    # Convert the string date to a datetime object
    most_recent_date = dt.strptime(most_recent_date, '%Y-%m-%d')

    # Calculate the date one year from the last date in data set.
    previous_date = (
        (most_recent_date - timedelta(days=365))   # Calculate the date
        .strftime('%Y-%m-%d')  # Format
    )

    # Query the results
    results = (
        session.query(Measurements.date, Measurements.prcp)
        .filter(Measurements.date.between(previous_date, most_recent_date))
        .order_by(Measurements.date)
        .all()
    )

    # Covert a dictionary from DB and append to a list of measurements
    all_precipitations = []
    for date, prcp in results:
        precipitation_dic = {}
        precipitation_dic['date'] = date
        precipitation_dic['prcp'] = prcp
        all_precipitations.append(precipitation_dic)

    # Close the session
    session.close()

    #display
    return jsonify(all_precipitations)


@app.route("/api/v1.0/stations")
def stations():
    # Create session from python to the DB
    session = Session(engine)

    # join stations and measurements table, then query all stations
    join_results =(
        session.query(
            Station.station,
            Station.name,
            Station.latitude,
            Station.longitude,
            Station.elevation,
            func.avg(Measurements.prcp).label('avg_prcp'),
            func.avg(Measurements.tobs).label('avg_tobs')
        )
        .join(Measurements, Measurements.station == Station.station)
        .group_by(Station.station, Station.name)
        .all()
    )

    # Covert a dictionary from DB and append to a list of stations
    all_stations = []
    for station, name, lat, long, elev, avg_prcp, avg_tobs in join_results:
        station_dict = {}
        station_dict["station"] = station
        station_dict["name"] = name
        station_dict["latitude"] = lat
        station_dict["longitude"] = long
        station_dict["elevation"] = elev
        station_dict["Average Precipitation"] = round(avg_prcp, 2)
        station_dict["Average Temperature"] = round(avg_tobs, 2)
        all_stations.append(station_dict)

    # Close the session
    session.close()

    #display
    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create session from python to the DB
    session = Session(engine)

    # List the stations and their counts in descending order.
    cnt_active_station = (
        session.query(Measurements.station, func.count(Measurements.station))
        .group_by(Measurements.station)
        .order_by(func.count(Measurements.station).desc())
        .all()
    )
    most_active_station = cnt_active_station[0][0]

    #Find the most recent date in the data set.
    most_recent_date = (
        session.query(Measurements.date)
        .order_by(Measurements.date.desc())
        .limit(1)
        # Use the `.scalar()` method to execute the query and get a single result. This will return a single value from the first column of the query.
        .scalar()
    )

    # Convert the string date to a datetime object
    most_recent_date = dt.strptime(most_recent_date, '%Y-%m-%d')

    # Calculate the date one year from the last date in data set.
    previous_date = (
        (most_recent_date - timedelta(days=365))   # Calculate the date
        .strftime('%Y-%m-%d')  # Format
    )

    # Find the temperature data for the previous year
    results = (
        session.query(Measurements.date, Measurements.tobs)
        .filter(and_(
            Measurements.station == most_active_station,
            Measurements.date.between(previous_date, most_recent_date)))
    )

    # Covert a dictionary from DB and append to a list of tobs
    all_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        all_tobs.append(tobs_dict)

    # Close the session
    session.close()

    #display
    return jsonify(all_tobs)


@app.route("/api/v1.0/<start>", defaults={'end': None})
@app.route("/api/v1.0/<start>/<end>")
def selected_date_temp(start, end):
    # Create session from python to the DB
    session = Session(engine)

    # format the start_date
    start_date = dt.strptime(start, '%Y%m%d').strftime('%Y-%m-%d')

    # Find the end_date, if end_date is null, use most_recent_date date instead.
    if not end:
        most_recent_date_str = (
            session.query(Measurements.date)
            .order_by(Measurements.date.desc())
            .limit(1)
            .all()
        )
        end_date = dt.strptime(most_recent_date_str[0][0], '%Y-%m-%d')
    else:
        end_date = dt.strptime(end, '%Y%m%d').strftime('%Y-%m-%d')

    # Find the temperature data
    results = (
        session.query(
            func.min(Measurements.tobs).label('TMIN'),
            func.max(Measurements.tobs).label('TMAX'),
            func.avg(Measurements.tobs).label('TAVG')
        )
        .filter(Measurements.date.between(start_date, end_date))
        .all()
    )

    # Covert a temp data into a list
    temp_data = []
    for min, max, avg in results:
        temp_dict = {}
        temp_dict['TMIN'] = min
        temp_dict['TMAX'] = max
        temp_dict['TAVG'] = round(avg, 2)
        temp_data.append(temp_dict)

    # Close the session
    session.close()

    return jsonify(temp_data)


if __name__ == "__main__":
    app.run(debug=True)

#%%
