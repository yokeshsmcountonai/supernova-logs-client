import db
from datetime import datetime
import time
import os

def fetch_data_from_devices():
    """Fetch latest data from multiple devices and write to Prometheus .prom file."""
    device_list = ["cam1_logs", "cam2_logs", "cm5_logs"]

    while True:
        result = db.fetch_details(device_list)  
        converted_result = {}
        if result:
            # for cam, values in result.items():
            #     *metrics, timestamp_str = values  
            #     dt = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S") 
            #     unix_timestamp = int(dt.timestamp())  
            #     converted_result[cam] = (*metrics, unix_timestamp) 

            print(result)  

            write_to_prometheus_file(result)  

            time.sleep(10)

def write_to_prometheus_file(stats):
    """Writes the fetched device metrics to a .prom file for Prometheus."""
    prom_file = "output/system_metrics.prom"
    os.makedirs(os.path.dirname(prom_file), exist_ok=True)

    with open(prom_file, "w") as f:
        for device, values in stats.items():
            if not values:  
                continue  # Skip if there's no data
            
            cpu_usage, ram_usage, voltage, temperature, gpu_temperature, timestamp,unix_timestamp = values

            f.write(f'cpu_usage{{device="{device}"}} {cpu_usage}\n')
            f.write(f'ram_usage{{device="{device}"}} {ram_usage}\n')
            f.write(f'voltage{{device="{device}"}} {voltage}\n')
            f.write(f'temperature{{device="{device}"}} {temperature}\n')
            f.write(f'gpu_temperature{{device="{device}"}} {gpu_temperature}\n')
            # f.write(f'timestamp{{device="{device}"}} {timestamp}\n')
            f.write(f'm_timestamp{{device="{device}"}} {unix_timestamp}\n')

    print(f"Metrics written to {prom_file}")


if __name__ == "__main__":
    fetch_data_from_devices()
