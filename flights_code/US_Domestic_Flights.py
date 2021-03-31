from __future__ import print_function

import sys
from pyspark.sql import SparkSession
from pyspark.sql.functions import format_string, date_format
from csv import reader

if __name__ == "__main__":
    spark = SparkSession \
        .builder \
        .appName("Python Spark SQL - Flights Analysis") \
        .config("spark.some.config.option", "some-value") \
        .getOrCreate()

    out_path = "us_flights"

    # data can be found at the projects github repo; however, the flights data is very large
    flight_data_path = "/user/cad605/data/combined_flights.csv"
    airport_data_path = "/user/cad605/data/airports.csv"

    # sys.argv[1]
    airports = spark.read.format('csv').options(header='true', inferschema='true').load(
        sys.argv[1])
    flights = spark.read.format('csv').options(header='true', inferschema='true').load(
        sys.argv[2])

    airports.createOrReplaceTempView("airports")
    flights.createOrReplaceTempView("flights")

    # filter our airports to only those within the United States, and that are large, commmercial airports (ex. no
    # Air Force bases)
    filtered_airports = spark.sql(
        "SELECT ident, type, name, latitude_deg, longitude_deg, iso_country, iso_region, municipality FROM airports "
        "WHERE (iso_country='US' AND type='large_airport' AND (name NOT LIKE '%Air Force%'))")
    filtered_airports.show()
    filtered_airports.createOrReplaceTempView("filtered_airports")

    # filter flights to only domestic flights, where the origin and destination match an airport within our
    # filtered_airport table
    filtered_flights = spark.sql(
        "SELECT f.callsign, f.origin, f.destination, f.day, a1.name as origin_name, a1.latitude_deg as origin_lat, "
        "a1.longitude_deg as origin_long, a1.iso_region as origin_region, a1.municipality as origin_municipality, "
        "a2.name as dest_name, a2.latitude_deg as dest_lat, a2.longitude_deg as dest_long, a2.iso_region as "
        "dest_region, a2.municipality as dest_municipality FROM flights as f INNER JOIN filtered_airports AS a1 ON "
        "f.origin = a1.ident INNER JOIN filtered_airports as a2 ON f.destination = a2.ident")
    filtered_flights.show()

    # write combined dataset, US Domestic Flights, to output file: us_flights
    filtered_flights.select(
        format_string('%s, %s, %s, %s, %s, %f, %f, %s, %s, %s, %f, %f, %s, %s', filtered_flights.callsign,
                      filtered_flights.origin, filtered_flights.destination,
                      date_format(filtered_flights.day, 'yyyy-MM-dd'), filtered_flights.origin_name,
                      filtered_flights.origin_lat, filtered_flights.origin_long, filtered_flights.origin_region,
                      filtered_flights.origin_municipality, filtered_flights.dest_name, filtered_flights.dest_lat,
                      filtered_flights.dest_long, filtered_flights.dest_region,
                      filtered_flights.dest_municipality)).write.save(out_path, format="text")
