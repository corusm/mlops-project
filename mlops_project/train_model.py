from tsai.basics import *
from models.model import Forecaster
import hydra
from omegaconf import DictConfig

@hydra.main(config_path="config", config_name="config")
def train(cfg: DictConfig):
    # TODO add arguments to allow parameter tuning
    model = Forecaster()
    model.train_model()


if __name__ == "__main__":
    train()
