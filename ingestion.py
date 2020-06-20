import os, re
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import Base, BranchProduct, Product

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
ASSETS_DIR = os.path.join(PROJECT_DIR, "assets")
PRODUCTS_PATH = os.path.join(ASSETS_DIR, "PRODUCTS.csv")
PRICES_STOCK_PATH = os.path.join(ASSETS_DIR, "PRICES-STOCK.csv")

engine = create_engine("sqlite:///db.sqlite")

def clean_final_products_df(prices_stock_df):
    prices_stock_df['BRAND'].fillna("MISS", inplace=True)
    prices_stock_df['NAME'].fillna("None", inplace=True)
    prices_stock_df['CATEGORY'].fillna("MISS", inplace=True)
    prices_stock_df['PACKAGE'].fillna("None", inplace=True)

    return prices_stock_df

def clean_prices_stock_df(prices_stock_df):
    #Filtramos cada Branch
    br_rhsm = prices_stock_df[(prices_stock_df['BRANCH'] == 'RHSM') & (prices_stock_df['STOCK'] > 0)]
    br_mm = prices_stock_df[(prices_stock_df['BRANCH'] == 'MM') & (prices_stock_df['STOCK'] > 0)]

    #Unimos los Dataframes
    frames = [br_rhsm, br_mm]
    prices_stock_df = pd.concat(frames)
    prices_stock_df.columns = ['PRODUCT_ID','BRANCH','PRICE','STOCK']

    #Quitamos dulpicados
    prices_stock_df.drop_duplicates(subset="PRODUCT_ID", keep = 'first', inplace = True) 
    prices_stock_df.to_csv('branches.csv')
    return prices_stock_df

def clean_products_df(products_df):
    # Para Full_category
    products_df['CATEGORY'] = products_df['CATEGORY'].str.cat(products_df['SUB_CATEGORY'], sep='|').str.lower()
    products_df['URL'] = products_df['IMAGE_URL'].copy()
    products_df['STORE'] = "Richart's"
    #Quitamos etiquetas HTML
    products_df['DESCRIPTION'] = products_df.DESCRIPTION.apply(lambda x: re.sub('<[^<]+?>', '', x))
    #Extraemos PACKAGE
    products_df['PACKAGE'] = products_df['DESCRIPTION'].str.extract(r'(\d{1,4} ?[a-zA-Z]{1,3}.?$)')
    #Extraemos los campos de interes
    products_df = products_df[['SKU', 'STORE', 'BARCODES', 'BRAND', 'NAME', 'DESCRIPTION', 'CATEGORY', 'PACKAGE', 'URL', 'IMAGE_URL']].copy()
    # Limpiamos sus campos vacios
    products_df = clean_final_products_df(products_df)

    return products_df

def injection(products_df, prices_stock_df):
    Session = sessionmaker(bind=engine)
    session  = Session()

    #Añadimos productos
    products_df.to_sql('products', con=engine, if_exists='append', index=False)
    #Añadimos prices
    prices_stock_df.to_sql('branchproducts', con=engine, if_exists='append', index=False)

    # Commit the changes
    session.commit()
    # Close the session
    session.close()

def process_csv_files():
    products = pd.read_csv(filepath_or_buffer=PRODUCTS_PATH, sep="|")
    prices = pd.read_csv(filepath_or_buffer=PRICES_STOCK_PATH, sep="|")

    return products, prices 

if __name__ == "__main__":
    Base.metadata.create_all(engine)

    #Dataframes
    products, prices = process_csv_files()
    
    # prices_stock_df
    prices_stock_df = clean_prices_stock_df(prices)
    # products_df
    products_df = clean_products_df(products)

    #Ingestion
    injection(products_df, prices_stock_df)

