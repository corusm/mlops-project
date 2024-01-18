# Use this script inside docker to run sequentially:
# - process data
# - train
# - visualize

import runpy

if __name__ == "__main__":
    runpy.run_path("mlops_project/data/make_dataset.py")
    runpy.run_path("mlops_project/train_model.py")
    runpy.run_path("mlops_project/visualizations/visualize.py")