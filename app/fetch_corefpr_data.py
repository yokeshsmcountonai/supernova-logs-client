import os
import time
import db  # Assuming db.fetch_details_core_fpr() is correctly imported

def write_to_prometheus_file(data):
    PROM_FILE_PATH = "output/corefpr_details.prom"
    print(f"Writing to: {PROM_FILE_PATH}")

    os.makedirs(os.path.dirname(PROM_FILE_PATH), exist_ok=True)

    with open(PROM_FILE_PATH, "w") as f:
        for cam, rows in data.items():
            if rows:
                metrics_names = [
                    "core_to_camera", "camera_to_core", "core_to_infer",
                    "infer_to_ml", "ml_to_core", "core_to_alarm", "alarm_to_core", "cf_timestamp"
                ]

                for idx, row in enumerate(rows):  # Iterate over multiple rows
                    for metric_name, value in zip(metrics_names, row):
                            f.write(f"{metric_name}{{device=\"{cam}\", id=\"{idx}\"}} {value}\n")


    print(f"Successfully wrote to {PROM_FILE_PATH}")


def fetch_data_from_cameras():
    """Fetch latest data from multiple devices and write to Prometheus .prom file."""
    while True:
        result = db.fetch_details_core_fpr()
        # print(f"Raw Result: {result}")

        if result:
            converted_result = {cam: values for cam, values in result.items() if values}

            write_to_prometheus_file(converted_result)

        time.sleep(10)


fetch_data_from_cameras()
