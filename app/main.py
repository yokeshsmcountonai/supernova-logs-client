import os
import time
import sys
import db  # Assuming db.fetch_details() and db.fetch_details_core_fpr() exist
from datetime import datetime

PROM_SYSTEM_FILE = "output/system_metrics.prom"
PROM_COREFPR_FILE = "output/corefpr_details.prom"

def write_to_prometheus_file(data, file_path, metrics_names, is_corefpr=False):
    """Writes fetched device metrics to a .prom file for Prometheus."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            for device, values in data.items():
                if not values:
                    continue  # Skip if there's no data
                
                if is_corefpr:  # Handling CoreFPR data
                    for idx, row in enumerate(values):
                        for metric_name, value in zip(metrics_names, row):
                            f.write(f"{metric_name}{{device=\"{device}\", id=\"{idx}\"}} {value}\n")
                else:  # Handling System Metrics
                    cpu_usage, ram_usage, voltage, temperature, gpu_temperature, timestamp, unix_timestamp = values
                    f.write(f'cpu_usage{{device="{device}"}} {cpu_usage}\n')
                    f.write(f'ram_usage{{device="{device}"}} {ram_usage}\n')
                    f.write(f'voltage{{device="{device}"}} {voltage}\n')
                    f.write(f'temperature{{device="{device}"}} {temperature}\n')
                    f.write(f'gpu_temperature{{device="{device}"}} {gpu_temperature}\n')
                    f.write(f'm_timestamp{{device="{device}"}} {unix_timestamp}\n')

        print(f"Successfully wrote to {file_path}")

    except Exception as e:
        print(f"Error writing to {file_path}: {e}", file=sys.stderr)


def fetch_data():
    """Fetch and write system and corefpr metrics every 10 seconds."""
    try:
        device_list = ["cam1_logs", "cam2_logs", "cm5_logs"]
        corefpr_metrics = [
            "revolution_id","core_to_camera", "camera_to_core", "core_to_infer",
            "infer_to_ml", "ml_to_core", "core_to_alarm", "alarm_to_core", "cf_timestamp"
        ]

        while True:
            try:
                # Fetch system metrics
                system_result = db.fetch_details(device_list)
                if system_result:
                    write_to_prometheus_file(system_result, PROM_SYSTEM_FILE, [], is_corefpr=False)

                # Fetch CoreFPR details
                corefpr_result = db.fetch_details_core_fpr()
                if corefpr_result:
                    write_to_prometheus_file(corefpr_result, PROM_COREFPR_FILE, corefpr_metrics, is_corefpr=True)

                time.sleep(10)  # Wait 10 seconds before next fetch

            except Exception as e:
                print(f"Error fetching or processing data: {e}", file=sys.stderr)
                time.sleep(5)  # Wait before retrying to prevent immediate crash loops

    except Exception as e:
        print(f"Critical error in fetch_data: {e}", file=sys.stderr)
        time.sleep(5)
        restart_script()


def restart_script():
    """Restart the script in case of a critical error."""
    print("Restarting script...", file=sys.stderr)
    time.sleep(5)
    os.execv(sys.executable, ['python3'] + sys.argv)  # Restart script


if __name__ == "__main__":
    try:
        fetch_data()
    except Exception as e:
        print(f"Unhandled error in main: {e}", file=sys.stderr)
        restart_script()
