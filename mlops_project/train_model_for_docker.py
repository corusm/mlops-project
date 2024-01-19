# Use this script inside docker to run sequentially:
# - process data
# - train
# - visualize

import subprocess

if __name__ == "__main__":
    subprocess.run(["python", "mlops_project/data/make_dataset.py"], check=True)
    subprocess.run(["python", "mlops_project/train_model.py"], check=True)
#    subprocess.run(["python", "mlops_project/visualizations/visualize.py"], check=True)