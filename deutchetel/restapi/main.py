from flask import Blueprint, request, jsonify
import deutchetel.main as dt
import pandas as pd
import numpy as np
import deutchetel.utils as utils
import deutchetel.db as db

bp = Blueprint("rest_api", __name__)


@bp.route("/predict", methods=["POST"])
def predict():
    longitude = request.form["longitude"]
    latitude = request.form["latitude"]
    housing_median_age = request.form["housing_median_age"]
    total_rooms = request.form["total_rooms"]
    total_bedrooms = request.form["total_bedrooms"]
    population = request.form["population"]
    households = request.form["households"]
    median_income = request.form["median_income"]
    ocean_proximity = request.form["ocean_proximity"]

    model = dt.load_model(dt.MODEL_NAME)
    op_1h_to_ocean, op_inland, op_island, op_near_bay, op_near_ocean = utils.conv_ocean_proximity(ocean_proximity)
    X = pd.DataFrame(
        np.array([[longitude, latitude, housing_median_age,  total_rooms, total_bedrooms, population, households,
                   median_income, op_1h_to_ocean, op_inland, op_island, op_near_bay, op_near_ocean]]),
        columns=['longitude', 'latitude', 'housing_median_age', 'total_rooms', 'total_bedrooms', 'population',
                 'households', 'median_income', 'ocean_proximity_<1H OCEAN', 'ocean_proximity_INLAND',
                 'ocean_proximity_ISLAND', 'ocean_proximity_NEAR BAY', 'ocean_proximity_NEAR OCEAN']
    )
    y = dt.predict(X, model)
    db.log_prediction(longitude, latitude, housing_median_age,  total_rooms, total_bedrooms, population, households,
                      median_income, ocean_proximity, y[0])
    return jsonify({'median_house_value': y[0]})


@bp.route("/history", methods=["POST"])
def history():
    try:
        size = int(request.form.get("size", 10))
    except ValueError:
        size = 10

    history = db.get_history(size)
    return jsonify({'predictions': history})








