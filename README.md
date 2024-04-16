
Climate Analysis and Flask App README
Part 1: Analyze and Explore the Climate Data
Setup
Use the create_engine() function from SQLAlchemy to connect to the SQLite database.
Use automap_base() to reflect the tables into classes: Station and Measurement.
Create a session to link Python to the database.


Precipitation Analysis
Find the most recent date in the dataset.
Retrieve the previous 12 months of precipitation data.
Load the data into a Pandas DataFrame and set the column names.
Sort the DataFrame by date.
Plot the results using Matplotlib.
Print summary statistics for the precipitation data.


Station Analysis
Calculate the total number of stations in the dataset.
Find the most active stations:
List stations and observation counts in descending order.
Identify the station with the greatest number of observations.
Calculate the lowest, highest, and average temperatures for the most active station.
Query the previous 12 months of temperature observation (TOBS) data for the most active station.
Plot the TOBS data as a histogram.

Closing
Close the SQLAlchemy session.

Part 2: Design Your Climate App
Routes
/: Homepage listing available routes.
/api/v1.0/precipitation: JSON representation of the last 12 months of precipitation data.
/api/v1.0/stations: JSON list of stations from the dataset.
/api/v1.0/tobs: JSON list of temperature observations for the previous year from the most active station.
/api/v1.0/<start>: JSON list of TMIN, TAVG, and TMAX for dates greater than or equal to the specified start date.
/api/v1.0/<start>/<end>: JSON list of TMIN, TAVG, and TMAX for dates between the specified start and end dates.
