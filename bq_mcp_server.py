from mcp.server.fastmcp import FastMCP
from google.cloud import bigquery
import pandas as pd

# Initialize FastMCP
mcp = FastMCP("BigQuery-Product-Service")

# Initialize BigQuery Client
# GCP will automatically pick up credentials if running on Vertex AI/Cloud Run
bq_client = bigquery.Client()

@mcp.tool()
def get_product_by_sku(sku: str) -> str:
    """
    Fetches comprehensive product details from BigQuery using a SKU reference.
    Use this when you need product names, dimensions, or technical specs.
    """
    query = """
        SELECT pd.product_dscr,pd.product_category_dscr,pd.product_subcategory_dscr,pd.product_type_nm,pd.product_type_group_nm, pd.sku_nbr, pd.department_dscr FROM `dataanalytics-013124-1d2.antonyp.product_dim` pd
        where sku = @sku
        and pd.product_dscr <> ''
        LIMIT 1
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("sku", "STRING", sku)
        ]
    )
    
    try:
        query_job = bq_client.query(query, job_config=job_config)
        results = query_job.to_dataframe()

        if results.empty:
            return f"No product found for SKU: {sku}"
        
        # Return as a stringified JSON for the LLM to parse easily
        return results.to_json(orient="records")
    except Exception as e:
        return f"Error querying BigQuery: {str(e)}"

if __name__ == "__main__":
    mcp.run()