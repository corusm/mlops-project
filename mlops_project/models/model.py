from tsai.basics import TSForecaster, load_object, mse, mae, np, os

import wandb
from fastai.callback.wandb import *

# By using tsai module the model can be reduced just to the architecture definition.


class Forecaster:
    """
    A forecasting model class using the tsai library, focused on time series data.

    Attributes:
    arch_config (dict): Configuration parameters for the model architecture.

    Methods:
    _get_data(path): Loads preprocessed data, pipelines, and splits.
    train_model(): Trains the forecasting model using the TSForecaster from tsai.
                   The model is trained and saved to models directory.
    """

    def __init__(self) -> None:
        # obsolete
        self.arch_config = dict(
            n_layers=3,  # number of encoder layers
            n_heads=4,  # number of heads
            d_model=16,  # dimension of model
            d_ff=128,  # dimension of fully connected network
            attn_dropout=0.0,  # dropout applied to the attention weights
            dropout=0.3,  # dropout applied to all linear layers in the encoder except q,k&v projections
            patch_len=24,  # length of the patch applied to the time series to create patches
            stride=2,  # stride used when creating patches
            padding_patch=True,  # padding_patch
        )

    def get_data(self, path):
        feature_target_data = np.load(os.path.join(path, "processed.npz"))
        X = feature_target_data["array1"]
        y = feature_target_data["array2"]

        preproc_pipe = load_object(os.path.join(path, "preproc_pipe.pkl"))
        exp_pipe = load_object(os.path.join(path, "exp_pipe.pkl"))
        splits = load_object(os.path.join(path, "splits.pkl"))

        return X, y, preproc_pipe, exp_pipe, splits

    def train_model(self):
        PATH_PROCESSED = "data/processed"

        X, y, preproc_pipe, exp_pipe, splits = self.get_data(PATH_PROCESSED)

        sweep_config = {
            'method':'bayes',
            'parameters': {
                'n_layers': {
                    'values':[1, 2, 3, 4, 5]
                    },
                'd_model': {
                    'values': [8, 16, 32, 48, 64]
                    },
                'd_ff':{
                    'values': [128, 192, 256, 320, 384]
                    },
                'dropout': { 
                    'values': [0, 0.3, 0.6]
                    }
            },
            'metric': {
                'name': 'valid_loss',
                'goal': 'minimize'
                }
        }
        sweep_id = wandb.sweep(sweep_config, project="62-train")

        def train_conf():
            with wandb.init():
                arch_config = dict(
                    n_layers=wandb.config.n_layers,  # number of encoder layers
                    n_heads=4,  # number of heads
                    d_model=wandb.config.d_model,  # dimension of model
                    d_ff=wandb.config.d_ff,  # dimension of fully connected network
                    attn_dropout=0.0,  # dropout applied to the attention weights
                    dropout=wandb.config.dropout,  # dropout applied to all linear layers in the encoder except q,k&v projections
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
        
        wandb.agent(sweep_id, train_conf, count=5)

        # TODO make a plot
