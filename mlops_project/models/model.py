import hydra
import omegaconf
from tsai.basics import TSForecaster, load_object, mse, mae, np, os

import wandb
from fastai.callback.wandb import *

import matplotlib.pyplot as plt

# By using tsai module the model can be reduced just to the architecture definition.

"""
A forecasting model class using the tsai library, focused on time series data.

Attributes:
arch_config (dict): Configuration parameters for the model architecture.

Methods:
_get_data(path): Loads preprocessed data, pipelines, and splits.
train_model(): Trains the forecasting model using the TSForecaster from tsai.
                The model is trained and saved to models directory.
"""

def get_data(path) -> Any:
    feature_target_data = np.load(os.path.join(path, "processed.npz"))
    X = feature_target_data["array1"]
    y = feature_target_data["array2"]

    preproc_pipe = load_object(os.path.join(path, "preproc_pipe.pkl"))
    exp_pipe = load_object(os.path.join(path, "exp_pipe.pkl"))
    splits = load_object(os.path.join(path, "splits.pkl"))

    return X, y, preproc_pipe, exp_pipe, splits


@hydra.main(config_path="configs", config_name="config")
def train_model(cfg) -> Any:
    PATH_PROCESSED = "/data/processed"

    X, y, preproc_pipe, exp_pipe, splits = get_data(PATH_PROCESSED)

    with wandb.init(project="dtu-mlops-model-reg-62") as run:

        wandb.config = omegaconf.OmegaConf.to_container(
            cfg, resolve=True, throw_on_missing=True
        )

        arch_config = dict(
            n_layers=wandb.config["n_layers"],  # number of encoder layers
            n_heads=4,  # number of heads
            d_model=wandb.config["d_model"],  # dimension of model
            d_ff=wandb.config["d_ff"],  # dimension of fully connected network
            attn_dropout=0.0,  # dropout applied to the attention weights
            dropout=wandb.config["dropout"],  # dropout applied to all linear layers in the encoder except q,k&v projections
            patch_len=24,  # length of the patch applied to the time series to create patches
            stride=2,  # stride used when creating patches
            padding_patch=True,  # padding_patch
        )

        learn = TSForecaster(
            X,
            y,
            splits=splits,
            batch_size=16,
            path="models",
            pipelines=[preproc_pipe, exp_pipe],
            arch="PatchTST",
            arch_config=arch_config,
            metrics=[mse, mae],
            cbs=WandbCallback()
        )

        n_epochs = 20
        lr_max = 0.0025

        learn.fit_one_cycle(n_epochs, lr_max=lr_max)
        
        # save model
        learn.export("patchTST.pt")

        model_artifact = wandb.Artifact(name="model_62", type="model")
        model_artifact.add_file("patchTST.pt")
        run.log_artifact(model_artifact)

        plot_splits(splits)
        plt.savefig("splits.png")
        plot_artifact = wandb.Artifact(name="plots_62", type="plot")
        plot_artifact.add_file("splits.pt")
        run.log_artifact(plot_artifact)


    # TODO make a plot
