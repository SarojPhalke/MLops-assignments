import nest_asyncio
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import pandas as pd
import matplotlib.pyplot as plt

# Apply nest_asyncio to allow running the FastAPI app inside the Jupyter notebook
nest_asyncio.apply()

# Initialize the FastAPI app
app = FastAPI()

# Implement the WineDataFilter class
class WineDataFilter:
    def __init__(self, file_path: str):
        # Load the wine dataset
        self.df = pd.read_csv(file_path)

    def filter_by_quality(self, min_quality: int, max_quality: int) -> pd.DataFrame:
        # Filter the dataset based on the quality range
        return self.df[(self.df['quality'] >= min_quality) & (self.df['quality'] <= max_quality)]

# Instantiate the WineDataFilter
wine_filter = WineDataFilter(file_path="winequality-red.csv")

# Set up the FastAPI endpoint
@app.get("/filter_wines/")
def filter_wines(min_quality: int = Query(5), max_quality: int = Query(8), features: list[str] = Query(None)):
    # Filter the wine data based on quality
    filtered_df = wine_filter.filter_by_quality(min_quality, max_quality)

    # Generate and save visualizations
    if features:
        for feature in features:
            plt.figure(figsize=(8, 6))
            plt.hist(filtered_df[feature], bins=20, color='blue', edgecolor='black')
            plt.title(f'Distribution of {feature}')
            plt.xlabel(feature)
            plt.ylabel('Frequency')
            image_path = f'{feature}_distribution.png'
            plt.savefig(image_path)
            plt.close()

    # Return the filtered data and file paths of the saved visualizations
    response = {
        "filtered_data": filtered_df.to_dict(orient="records"),
        "visualizations": [f"{feature}_distribution.png" for feature in features] if features else []
    }

    return JSONResponse(content=response)

import uvicorn

# Run the FastAPI app
uvicorn.run(app, host="127.0.0.1", port=8001)
