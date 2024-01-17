import subprocess
import sys
import os

def run_script(script_path):
    try:
        # Print current working directory and PYTHONPATH
        print(f"Current working directory: {os.getcwd()}")
        python_path = os.environ.get('PYTHONPATH', '')
        print(f"PYTHONPATH: {python_path}")

        # Full path to script
        full_script_path = os.path.join(os.getcwd(), script_path)
        print(f"Full script path: {full_script_path}")

        # Check if the script file exists at the expected path
        if not os.path.isfile(full_script_path):
            raise FileNotFoundError(f"The script {full_script_path} does not exist.")

        # Run the script
        subprocess.run(["python3", full_script_path], check=True)
        print(f"Successfully executed {script_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while executing {script_path}: {e}")
        print(f"Return code: {e.returncode}")
        if e.output:
            print(f"Output: {e.output.decode('utf-8')}")
        if e.stderr:
            print(f"Error: {e.stderr.decode('utf-8')}")
    except FileNotFoundError as e:
        print(e)

if __name__ == "__main__":
    run_script("mlops_project/data/make_dataset.py")
    run_script("mlops_project/models/train_model.py")
    run_script("mlops_project/visualizations/visualize.py")
