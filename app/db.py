import psycopg2
from psycopg2 import sql

# PostgreSQL database credentials
DB_HOST = "100.65.137.88" #http://100.65.137.88/
DB_PORT = "5432"
DB_NAME = "knitting"
DB_USER = "postgres"
DB_PASSWORD = "55555"

def get_db_connection():
    """Establish and return a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None

def insert_stats_to_db(stats):
    """Insert the system stats into the PostgreSQL database."""

    conn = get_db_connection()
  
    if conn is None:
        return
    
    try:
        cursor = conn.cursor()
        # Define your insert query
        query = f"""
            INSERT INTO cpu_logs (
                timestamp, 
                cpu_usage, 
                ram_usage, 
                swap_usage, 
                tasks, 
                arm_clock, 
                temperature, 
                voltage,
                upload_speed, 
                downloadspeed, 
                gpu_memory, 
                gpu_temperature, 
                root_usage,
                wifi_status, 
                kniti_usage, 
                database_usage
            ) VALUES (
                '{stats["timestamp"]}', 
                {stats["cpu_usage"]}, 
                {stats["ram_usage"]}, 
                {stats["swap_usage"]}, 
                {stats["tasks"]}, 
                {stats["arm_clock"]}, 
                {stats["temperature"]}, 
                {stats["voltage"]}, 
                {stats["upload_speed"]}, 
                {stats["download_speed"]}, 
                '{stats["gpu_memory"]}', 
                {stats["gpu_temperature"]}, 
                {stats["root_usage"]}, 
                '{stats["wifi_status"]}', 
                {stats["kniti_usage"]}, 
                {stats["database_usage"]}
            );
            """

        cursor.execute(query)

        conn.commit()
        cursor.close()
    except Exception as e:
        print(f"Error inserting data into database: {e}")
    finally:
        conn.close()


def fetch_details(device_list):
    conn = get_db_connection()

    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()

        # Queries for cam1, cam2, and cm5
        cam1_query = """
            SELECT cpu_usage, ram_usage, voltage, temperature, gpu_temperature,timestamp,  
            EXTRACT(EPOCH FROM timestamp::TIMESTAMP) AS unix_timestamp 
            FROM cam1_log ORDER BY timestamp DESC 
            LIMIT 1;
        """
        cam2_query = """
            SELECT cpu_usage, ram_usage, voltage, temperature, gpu_temperature,timestamp,  
            EXTRACT(EPOCH FROM timestamp::TIMESTAMP) AS unix_timestamp 
            FROM cam2_log ORDER BY timestamp DESC 
            LIMIT 1;
        """
        cm5_query = """
            SELECT cpu_usage, ram_usage, voltage, temperature, gpu_temperature,timestamp,  
            EXTRACT(EPOCH FROM timestamp::TIMESTAMP) AS unix_timestamp 
            FROM cm5_log ORDER BY timestamp DESC 
            LIMIT 1;
        """

        # Execute each query separately
        cursor.execute(cam1_query)
        cam1_result = cursor.fetchone()

        cursor.execute(cam2_query)
        cam2_result = cursor.fetchone()

        cursor.execute(cm5_query)
        cm5_result = cursor.fetchone()

        cursor.close()

        # Return results as a dictionary
        return {
            "cam1": cam1_result,
            "cam2": cam2_result,
            "cm5": cm5_result
        }

    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return None
    finally:
        conn.close()



def fetch_details_core_fpr():
    conn = get_db_connection()

    if conn is None:
        return None
    
    try:
        cursor = conn.cursor()

        # Queries for cam1, cam2, and cm5
        cam1_query = """
            SELECT core_to_camera,camera_to_core,core_to_infer,infer_to_ml,ml_to_core, core_to_alarm, alarm_to_core,EXTRACT(EPOCH FROM rotation_details.timestamp) AS c_timestamp
            FROM public.corefpr_log_cam1 
            JOIN public.rotation_details 
            ON corefpr_log_cam1.revolution_id = rotation_details.rotation_id
            ORDER BY rotation_details.timestamp DESC
            OFFSET 3
            LIMIT 20
            
        """
        cam2_query = """
            SELECT core_to_camera,camera_to_core,core_to_infer,infer_to_ml,ml_to_core, core_to_alarm, alarm_to_core,EXTRACT(EPOCH FROM rotation_details.timestamp) AS c_timestamp
            FROM public.corefpr_log_cam2
            JOIN public.rotation_details 
            ON corefpr_log_cam2.revolution_id = rotation_details.rotation_id
            ORDER BY rotation_details.timestamp DESC
            OFFSET 3
            LIMIT 20
        """
        
        # Execute each query separately
        cursor.execute(cam1_query)
        cam1_result = cursor.fetchall()

        cursor.execute(cam2_query)
        cam2_result = cursor.fetchall()

    

        cursor.close()
        print(cam1_result,'**************************************')
        print(cam2_result,'######################################')
        # Return results as a dictionary
        return {
            "cam1": cam1_result,
            "cam2": cam2_result
        }

    except Exception as e:
        print(f"Error fetching data from database: {e}")
        return None
    finally:
        conn.close()
