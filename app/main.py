import multiprocessing
import subprocess

def run_fetch_data():
    subprocess.run(["python3", "fetch_data.py"])

def run_fetch_corefpr_data():
    subprocess.run(["python3", "fetch_corefpr_data.py"])

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=run_fetch_data)
    p2 = multiprocessing.Process(target=run_fetch_corefpr_data)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
