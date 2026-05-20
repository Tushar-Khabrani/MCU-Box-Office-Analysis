import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine, text
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
log = logging.getLogger("mcu_pipeline")

CONFIG = {
    "raw_csv"     : r"C:\Users\Tushar\OneDrive\Desktop\Marvel\mcu_py\data\mcu.csv",
    "clean_csv"   : r"C:\Users\Tushar\OneDrive\Desktop\Marvel\mcu_py\data\mcu_clean.csv",
    "powerbi_csv" : r"C:\Users\Tushar\OneDrive\Desktop\Marvel\dashboard\mcu_powerbi.csv",
    "db_host"     : "localhost",
    "db_user"     : "root",
    "db_password" : "Root@123",
    "db_name"     : "marvel",
    "db_port"     : 3306,
}

def extract(path):
    log.info("STEP 1 - Extracting raw data...")
    df = pd.read_csv(path)
    log.info(f"  Loaded {len(df)} rows, {len(df.columns)} columns")
    return df

def transform(df):
    log.info("STEP 2 - Cleaning data...")
    df = df.copy()
    if "Ref" in df.columns:
        df.drop(columns=["Ref"], inplace=True)
    df = df[df["Film"].str.strip() != "Total"].reset_index(drop=True)
    log.info(f"  {len(df)} films after removing Total row")
    bo_cols = ["US_Canada_BO", "Other_Territories_BO", "Worldwide_BO"]
    for col in bo_cols:
        df[col] = df[col].astype(str).str.replace(r"[\$,\[e\]]", "", regex=True).str.strip()
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Budget"] = (df["Budget"].astype(str)
                    .str.replace(r"\$|\xa0", "", regex=True)
                    .str.replace("million", "", regex=False)
                    .str.replace("\u2013", "-", regex=False)
                    .str.replace("\u2014", "-", regex=False)
                    .str.strip())
    df["Budget_min"] = pd.to_numeric(df["Budget"].str.split("-").str[0].str.strip(), errors="coerce") * 1_000_000
    df["Budget_max"] = pd.to_numeric(df["Budget"].str.split("-").str[-1].str.strip(), errors="coerce") * 1_000_000
    df["Budget_avg"] = (df["Budget_min"] + df["Budget_max"]) / 2
    df["Release_Date"]  = pd.to_datetime(df["Release_Date"], errors="coerce")
    df["Release_Year"]  = df["Release_Date"].dt.year.astype("Int64")
    df["Release_Month"] = df["Release_Date"].dt.month.astype("Int64")
    df["ROI"]    = ((df["Worldwide_BO"] - df["Budget_avg"]) / df["Budget_avg"]).round(2)
    df["Profit"] = df["Worldwide_BO"] - df["Budget_avg"]
    df["US_Percent"]   = (df["US_Canada_BO"]        / df["Worldwide_BO"] * 100).round(2)
    df["Intl_Percent"] = (df["Other_Territories_BO"] / df["Worldwide_BO"] * 100).round(2)
    log.info("  Cleaning complete!")
    return df

def load_mysql(df, cfg):
    log.info("STEP 3 - Loading into MySQL...")
    try:
        engine = create_engine(
            f"mysql+pymysql://{cfg['db_user']}:{cfg['db_password']}@{cfg['db_host']}:{cfg['db_port']}/{cfg['db_name']}"
        )
        df_db = df.copy()
        df_db["Release_Date"] = df_db["Release_Date"].dt.strftime("%Y-%m-%d")
        df_db.to_sql("mcu_pipeline_clean", con=engine, if_exists="replace", index=False)
        log.info(f"  Inserted {len(df_db)} rows into MySQL!")
    except Exception as e:
        log.warning(f"  MySQL skip: {e}")

def export_powerbi(df, path):
    log.info("STEP 4 - Exporting Power BI CSV...")
    cols = ["Index","Film","Phase","Release_Date","Release_Year","Release_Month",
        "US_Canada_BO","Other_Territories_BO","Worldwide_BO","Budget",
        "Budget_min","Budget_max","Budget_avg","ROI","Profit",
        "US_Percent","Intl_Percent","US_Rank","WW_Rank"]
    df[[c for c in cols if c in df.columns]].to_csv(path, index=False)
    log.info(f"  Saved: {path}")

def save_clean_csv(df, path):
    log.info("STEP 5 - Saving clean CSV...")
    df.to_csv(path, index=False) 
    log.info(f"  Saved: {path}")

def print_summary(df):
    print("\n" + "="*50)
    print("  MCU PIPELINE - SUMMARY")
    print("="*50)
    print(f"  Total films       : {len(df)}")
    print(f"  Total WW Earnings : ${df['Worldwide_BO'].sum():,.0f}")
    print(f"  Highest grossing  : {df.loc[df['Worldwide_BO'].idxmax(), 'Film']}")
    print(f"  Best ROI film     : {df.loc[df['ROI'].idxmax(), 'Film']}")
    print(f"  Films at loss     : {(df['Profit'] < 0).sum()}")
    print("="*50 + "\n")

def run_pipeline():
    log.info("PIPELINE STARTED")
    df_raw   = extract(CONFIG["raw_csv"])
    df_clean = transform(df_raw)
    load_mysql(df_clean, CONFIG)
    export_powerbi(df_clean, CONFIG["powerbi_csv"])
    save_clean_csv(df_clean, CONFIG["clean_csv"])
    print_summary(df_clean)
    log.info("PIPELINE FINISHED!")

if __name__ == "__main__":
    run_pipeline()
