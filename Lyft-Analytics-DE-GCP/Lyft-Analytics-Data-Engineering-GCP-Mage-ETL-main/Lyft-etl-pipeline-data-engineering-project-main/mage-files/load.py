from mage_ai.data_preparation.repo_manager import get_repo_path
from mage_ai.io.bigquery import BigQuery
from mage_ai.io.config import ConfigFileLoader
from pandas import DataFrame
from os import path, getenv

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


@data_exporter
def export_data_to_big_query(data, **kwargs) -> None:
    """
    Export each fact/dimension table to BigQuery.
    Credentials come from 'io_config.yaml'; the target project and dataset
    come from the GCP_PROJECT_ID and BQ_DATASET environment variables.

    Docs: https://docs.mage.ai/design/data-loading#bigquery
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'
    project = getenv('GCP_PROJECT_ID', 'your-gcp-project')
    dataset = getenv('BQ_DATASET', 'lyft_data_engineering')

    for key, value in data.items():
        table_id = f'{project}.{dataset}.{key}'
        BigQuery.with_config(ConfigFileLoader(config_path, config_profile)).export(
            DataFrame(value),
            table_id,
            if_exists='replace',  # Specify resolution policy if table name already exists
        )
