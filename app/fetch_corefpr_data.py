import db
from datetime import datetime
import time
import os


import os
from datetime import datetime

def write_to_prometheus_file(data):
    PROM_FILE_PATH = 'output/corefpr_details.prom'
    print(f"Writing to: {PROM_FILE_PATH}")

    os.makedirs(os.path.dirname(PROM_FILE_PATH), exist_ok=True)
    with open(PROM_FILE_PATH, "w") as f:
        for cam, values in data.items():
            if values:
                metrics_names = [
                    "core_to_camera", "camera_to_core", "core_to_infer",
                    "infer_to_ml", "ml_to_core", "core_to_alarm", "alarm_to_core", "timestamp"
                ]
                data=zip(metrics_names,values)
                print(data)
                for metric_name, value in zip(metrics_names, values): 
                    print(metric_name,'=',value) 
                    f.write(f"{metric_name}{{device=\"{cam}\"}} {value}\n")


def fetch_data_from_cameras():
    """Fetch latest data from multiple devices and write to Prometheus .prom file."""
    while True:
        result = db.fetch_details_core_fpr()
        print(f"Raw Result: {result}")  # Debugging line

        if result:
            converted_result = {cam: values for cam, values in result.items() if values}  
            print(result,"$$$$$$$$$$$$$$$$")
            write_to_prometheus_file(converted_result)  

        time.sleep(10)  # Adjust the sleep time as needed

# Run the function
fetch_data_from_cameras()
