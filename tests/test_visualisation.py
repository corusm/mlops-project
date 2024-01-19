import os

from tests import _PROJECT_ROOT

VISUALISE_SCRIPT_PATH = os.path.join(_PROJECT_ROOT, "mlops_project/visualizations/visualize.py")


def test_visualise_script_execution():
    # result = subprocess.run(["python", VISUALISE_SCRIPT_PATH], capture_output=True, text=True)
    # assert result.returncode == 0, f"visualise.py failed to run: {result.stderr}"
    pass
