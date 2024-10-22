import pytest
import pandas as pd
import os
import sys
import numpy as np

# Ajouter le répertoire racine du projet au chemin Python
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.models.predict_model import make_predictions

def test_make_predictions_with_missing_data():
    # Create a copy of the user matrix with missing values
    user_matrix = pd.read_csv("data/processed/user_matrix.csv")
    user_matrix_with_nan = user_matrix.copy()
    user_matrix_with_nan.iloc[0, 1] = np.nan  # Introduce a NaN value
    temp_user_matrix_filename = "data/processed/temp_user_matrix_with_nan.csv"
    user_matrix_with_nan.to_csv(temp_user_matrix_filename, index=False)

    try:
        predictions_df = make_predictions(
            user_ids=[1],
            model_name="KNN_Recommendation_Model",
            user_matrix_filename=temp_user_matrix_filename,
            movie_matrix_filename="data/processed/movie_matrix.csv",
            n_recommendations=3,
            log_file="test_predictions_log.csv"
        )

        # The function should handle missing data appropriately, either by imputing or raising an error
        # For this test, we can check if an error is raised
        assert False, "Une exception était attendue à cause des données manquantes."

    except ValueError as e:
        # Expected exception
        assert "Input X contains NaN" in str(e), "Message d'erreur inattendu."

    finally:
        # Clean up test artifacts
        os.remove(temp_user_matrix_filename)
        predictions_dir = 'predictions'
        test_log_path = os.path.join(predictions_dir, "test_predictions_log.csv")
        if os.path.exists(test_log_path):
            os.remove(test_log_path)
            if not os.listdir(predictions_dir):
                os.rmdir(predictions_dir)