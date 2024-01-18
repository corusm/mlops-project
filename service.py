from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
import pandas as pd
import matplotlib.pyplot as plt
import os
from tsai.basics import *


app = FastAPI()

@app.post("/predict")
async def load_model(data: UploadFile = File(...)):
    # Read the uploaded CSV file
    new_df = pd.read_csv(data.file)
    new_df['t'] = pd.to_datetime(new_df['t'])
    fcst_date = "2003-01-01"
    fcst_history = 104
    freq = '24H'
    datetime_col = "t"

    dates = pd.date_range(start=None, end=fcst_date, periods=fcst_history, freq=freq)
    new_df = new_df[new_df[datetime_col].isin(dates)].reset_index(drop=True)

    learn = load_learner("models/patchTST.pt")
    filtered_df = learn.transform(new_df)
    
    x_vars = new_df.columns[1:]
    y_vars = new_df.columns[1:]
    new_X, _ = prepare_forecasting_data(filtered_df, fcst_history=104, fcst_horizon=0, x_vars=x_vars, y_vars=None)
    new_X.shape
    
    new_scaled_preds, *_ = learn.get_X_preds(new_X)
    
    fcst_horizon = 60

    new_scaled_preds = to_np(new_scaled_preds).swapaxes(1,2).reshape(-1, len(y_vars))
    dates = pd.date_range(start=fcst_date, periods=fcst_horizon + 1, freq='7D')[1:]
    preds_df = pd.DataFrame(dates, columns=[datetime_col])
    preds_df.loc[:, y_vars] = new_scaled_preds
    preds_df = learn.inverse_transform(preds_df)

    # Directory where plots will be saved
    plots_directory = 'saved_plots'
    os.makedirs(plots_directory, exist_ok=True)

    # Number of columns (excluding 't') and determine layout
    num_plots = len(preds_df.columns) - 1
    num_columns = 2  # You can adjust this as needed
    num_rows = (num_plots + 1) // num_columns

    # Create a figure with subplots
    fig, axs = plt.subplots(num_rows, num_columns, figsize=(15, 5 * num_rows))
    axs = axs.flatten()  # Flatten in case we have a grid

    # Loop through each column (except 't') and create a subplot
    for idx, column in enumerate(preds_df.columns):
        if column != 't':  # Skip the 't' column
            ax = axs[idx - 1]  # Adjust index for subplot
            preds_df.plot(x='t', y=column, kind='line', ax=ax, title=f'{column} over Time')

    # Adjust layout
    plt.tight_layout()

    # Save the entire figure to a BytesIO buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Return the plot as a direct image response from memory
    return StreamingResponse(buf, media_type="image/png")
