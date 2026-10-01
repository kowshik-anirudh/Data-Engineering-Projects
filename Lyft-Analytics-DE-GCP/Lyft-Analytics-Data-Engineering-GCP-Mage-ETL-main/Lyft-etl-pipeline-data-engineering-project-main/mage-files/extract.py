import io
import os
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

# Trip data is stored in this repo (data/lyft_data.csv); set LYFT_DATA_URL to load from your own GCS bucket instead
DEFAULT_DATA_URL = 'https://raw.githubusercontent.com/kowshik-anirudh/Data-Engineering-Projects/main/Lyft-Analytics-DE-GCP/Lyft-Analytics-Data-Engineering-GCP-Mage-ETL-main/Lyft-etl-pipeline-data-engineering-project-main/data/lyft_data.csv'


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Load the raw trip records CSV into a DataFrame.
    """
    url = os.getenv('LYFT_DATA_URL', DEFAULT_DATA_URL)
    response = requests.get(url)
    response.raise_for_status()

    return pd.read_csv(io.StringIO(response.text), sep=',')


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
