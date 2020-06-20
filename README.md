## pandas-integration
This is a small exercise where I show you how to clean and join 2 dataframes and integrate with SQLite trough SQLAlchemy

One you downloaded and activated your virtual env.

Install the dependencies with the following command 
 `pip install -r requirements.txt`

Run the application with this command
`python ingestion.py`

Sometimes the data comes from different sources, in this case we have two different data frames that need to be filtered, 
cleaned and then integrated into a database

- #### PRODUCTS.csv: Contains the product's basic information.
- #### PRICES-STOCK.csv: Contains information about the prices and stock

From PRODUCTS.csv the only branches we are interested in are RHSM and MM without duplicates

| PRODUCT_ID| BRANCH | STOCK | PRICE |
| --- | --- | --- | --- |

From PRICES-STOCK.csv the only branches we are interested in are RHSM and MM without duplicates
| STORE| SKU | BARCODES | BRAND | NAME | DESCRIPTION | PACKAGE | IMAGE_URL | CATEGORY | URL |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
