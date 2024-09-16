DROP TABLE IF EXISTS prediction;

CREATE TABLE prediction (
  ts TIMESTAMP PRIMARY KEY DEFAULT CURRENT_TIMESTAMP,
  latitude REAL NOT NULL,
  longitude REAL NOT NULL,
  housing_median_age REAL NOT NULL,
  total_rooms INTEGER NOT NULL,
  total_bedrooms INTEGER NOT NULL,
  population INTEGER NOT NULL,
  households INTEGER NOT NULL,
  median_income INTEGER NOT NULL,
  ocean_proximity TEXT NOT NULL,
  y REAL NOT NULL
);
