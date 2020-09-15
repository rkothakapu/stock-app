from stock_info_helper.core import setup_sod_df_for_all
import os


if __name__ == "__main__":
    df_all = setup_sod_df_for_all('tickers_data')
    for key in df_all:
        file = os.path.join(os.getcwd(), 'data', key)
        df_all[key].to_csv(file, index=True)