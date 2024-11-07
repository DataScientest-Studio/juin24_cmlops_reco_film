import csv
import logging
import random
import time

from prometheus_client import Gauge, start_http_server

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_csv_data():
    """Load CSV data into a list of dictionaries."""
    data = []
    try:
        with open("/data/predictions_log.csv", mode="r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile, delimiter=",")
            for row in reader:
                data.append(row)
        logging.info(f"Loaded {len(data)} rows from CSV file.")
    except Exception as e:
        logging.error(f"Error reading CSV file: {e}")
    return data


def update_metrics(data):
    """Loop over the data and update metrics to mimic new data acquisition."""
    gauge = Gauge(
        "prediction_error_metric",
        "Error metric for predictions",
        ["userId", "model_name", "model_version", "model_run_id"],
    )

    index = 0
    total_rows = len(data)

    while True:
        if total_rows == 0:
            logging.error("No data available to process.")
            time.sleep(15)
            continue

        row = data[index]

        # Log the current row being processed
        logging.info(f"Processing row {index + 1}/{total_rows}: {row}")

        # Get the error_metric value and add random noise
        error_metric = float(row["error_metric"])
        random_noise = random.uniform(-0.05, 0.05)  # Adjust the range as needed
        error_metric_with_noise = error_metric + random_noise

        # Ensure the metric remains non-negative
        error_metric_with_noise = max(error_metric_with_noise, 0)

        # Update the metric with values from the row
        gauge.labels(
            userId=row["userId"],
            model_name=row["model_name"],
            model_version=row["model_version"],
            model_run_id=row["model_run_id"],
        ).set(error_metric_with_noise)

        logging.info(
            f"Metric updated for userId {row['userId']} with value {error_metric_with_noise:.4f}"
        )

        # Wait before processing the next row
        time.sleep(15)  # Adjust the interval as needed

        # Move to the next row
        index = (index + 1) % total_rows  # Loop back to start after the last row


if __name__ == "__main__":
    # Start the Prometheus HTTP server on port 8080
    start_http_server(8080)
    logging.info("Starting CSV exporter on port 8080...")

    # Load the CSV data once at startup
    csv_data = load_csv_data()

    # Start updating metrics
    update_metrics(csv_data)
