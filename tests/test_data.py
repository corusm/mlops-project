import os

import pytest
import numpy as np
import subprocess

from tests import _PATH_DATA, _PROJECT_ROOT


@pytest.fixture(scope="session", autouse=True)
def prepare_data():
    """
    This fixture runs the make_dataset.py script before any tests are executed.
    It ensures that the raw data is processed and the results are stored in the expected directory.
    """
    if not os.path.exists(_PATH_DATA):
        os.makedirs(_PATH_DATA, exist_ok=True)

    # Assuming 'make_dataset.py' is in the current directory
    make_dataset_script = os.path.join(_PROJECT_ROOT, "mlops_project/data/make_dataset.py")
    assert os.path.isfile(make_dataset_script), f"{make_dataset_script} does not exist."

    # Run the make_dataset.py script
    subprocess.run(["python", make_dataset_script], check=True)

    # Ensure that the processed data file is created
    processed_file = os.path.join(_PATH_DATA, "processed/processed.npz")
    assert os.path.isfile(processed_file), f"Processed data file {processed_file} was not created."


@pytest.mark.skipif(not os.path.exists(_PATH_DATA), reason="Data files not found")
def test_data_size():
    feature_target_data = np.load(os.path.join(_PATH_DATA, "processed/processed.npz"))
    X = feature_target_data["array1"]
    y = feature_target_data["array2"]

    # Check if X and y are not empty
    assert X.size > 0, "X array is empty"
    assert y.size > 0, "y array is empty"

    # Check the shape of X and y
    assert len(X.shape) == 3, "X array should be 3D"
    assert len(y.shape) == 3, "y array should be 3D"

    # Check the first dimension is the same for X and y
    assert X.shape[0] == y.shape[0], "Mismatch in the number of samples between X and y"
    assert X.shape[1] == y.shape[1], "Mismatch in the number of features between X and y"


@pytest.mark.skipif(not os.path.exists(_PATH_DATA), reason="Data files not found")
def test_data_types():
    feature_target_data = np.load(os.path.join(_PATH_DATA, "processed/processed.npz"))
    X = feature_target_data["array1"]
    y = feature_target_data["array2"]

    # Check data types
    assert X.dtype == np.float64 or X.dtype == np.float32, "X array should have floating point type"
    assert y.dtype == np.float64 or y.dtype == np.float32, "y array should have floating point type"


@pytest.mark.skipif(not os.path.exists(_PATH_DATA), reason="Data files not found")
def test_statistical_properties():
    feature_target_data = np.load(os.path.join(_PATH_DATA, "processed/processed.npz"))
    X = feature_target_data["array1"]
    y = feature_target_data["array2"]

    # Basic statistical tests
    assert np.all(np.isfinite(X)), "X contains infinite or NaN values"
    assert np.all(np.isfinite(y)), "y contains infinite or NaN values"
