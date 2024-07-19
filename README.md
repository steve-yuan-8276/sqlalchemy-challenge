# SQLAlchemy Challenge

## Introduction

In this project, we perform climate analysis and data exploration for a vacation planning application. 

The dataset contains climate data for Honolulu, Hawaii from `20100101` to `20170823`.

We'll analyze this data using SQLAlchemy, Pandas, and Matplotlib. Finally, we'll create a Flask API to serve the data.

## Repository Structure

The repository structure is as follows:
```
sqlalchemy-challenge/
├── Resources/
│ ├── hawaii.sqlite
│ ├── hawaii_stations.csv
│ └── hawaii_measurements.csv
├── SurfsUP/
│ ├── app.py
│ └── climate_starter.ipynb
└── README.md
```

### Files

- `hawaii.sqlite`: The SQLite database containing climate data.
- `app.py`: The Flask application that serves the climate data via API endpoints.
- `climate_starter.ipynb`: The Jupyter notebook for performing climate data analysis and exploration.
- `README.md`: This file, providing an overview of the project and instructions for usage.

### How To Run

To run this project locally, follow these steps:

1. **Clone the repository**:
    ```sh
    git clone git@github.com:steve-yuan-8276/sqlalchemy-challenge.git
    cd sqlalchemy-challenge/SurfsUP
    ```

2. **Run the Jupyter Notebook**:
    Open `climate_starter.ipynb` in Jupyter Notebook and run the cells to perform the climate data analysis.

3. **Run the Flask app**:
    ```sh
    python app.py
    ```

## Solution

### Part 1: Analyze and Explore the Climate Data

Open `climate_solution.ipynb` in Jupyter Notebook to perform the following analyses:

1. **Precipitation Analysis**:
    - Retrieve and plot the last 12 months of precipitation data.
    - Print summary statistics.

2. **Station Analysis**:
    - Calculate the total number of stations.
    - Find the most-active stations and their observation counts.
    - Calculate the lowest, highest, and average temperatures for the most-active station.
    - Retrieve and plot the last 12 months of temperature observation data for the most-active station.

### Flask API

Run the Flask app `app.py`：

```sh
    python app.py
```

After running `app.py`, you can access the following API endpoints:

1. **Home**: `/`
    - Lists all available routes and their descriptions.

2. **Precipitation Data**: `/api/v1.0/precipitation`
    - Returns JSON representation of the precipitation data for the last 12 months.
    - Date as the key and precipitation as the value.

3. **Stations**: `/api/v1.0/stations`
    - Returns JSON list of all stations from the dataset,which includes station, name, longitude, latitude,  elevation, Average precipitation,  Average Temperature.

4. **Temperature Observations**: `/api/v1.0/tobs`
    - Returns JSON list of temperature observations of the most-active station for the previous year.

5. **Temperature Statistics**:
    - `/api/v1.0/<start>`: Returns JSON list of TMIN, TAVG, and TMAX for all dates greater than or equal to the start date.
    - `/api/v1.0/<start>/<end>`: Returns JSON list of TMIN, TAVG, and TMAX for dates between the start and end date inclusive.

### Example Requests

```sh
http://127.0.0.1:5000/api/v1.0/precipitation

http://127.0.0.1:5000/api/v1.0/stations

http://127.0.0.1:5000/api/v1.0/tobs

http://127.0.0.1:5000/api/v1.0/20160101

http://127.0.0.1:5000/api/v1.0/20160101/20170601
```


Thanks for your time.