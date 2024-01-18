# Use this script inside docker to run sequentially:
# - process data
# - train
# - visualize

from data.make_dataset import main as make_dataset
from models.train_model import main as train_model
from visualizations.visualize import main as visualize

if __name__ == "__main__":
    make_dataset()
    train_model()
    visualize()