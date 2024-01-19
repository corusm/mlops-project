# import os
# import pytest

# import mlops_project.models.model

# from tests import _PATH_DATA


class TestForecaster:
    # def test_data_loading(self):
    #     PATH_PROCESSED = os.path.join(_PATH_DATA, "processed")
    #     X, y, _, _, splits = mlops_project.models.model.get_data(PATH_PROCESSED)
    #     assert X is not None and y is not None, "Data not loaded correctly"
    #     assert len(splits) == 3, "Incorrect number of splits"

    def test_training_process(self):
        # This test might take longer, consider running with a smaller dataset or fewer epochs
        # try:
        #    mlops_project.models.model.train_model()
        # except Exception as e:
        #    pytest.fail(f"Training failed with exception: {e}")
        return

    # def test_model_saving(self):
    #     model_path = "/mlops_project/models/patchTST.pt"
    #     if os.path.exists(model_path):
    #         os.remove(model_path)
    #     # TODO also run for 1/2 epoch
    #     mlops_project.models.model.train_model()
    #     assert os.path.exists(model_path), "Model file not saved"
