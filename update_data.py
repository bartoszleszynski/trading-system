import yfinance as yf
from config import URL_FNG, PATH_FNG, PATH_BTC, BTC_TICKER
from etl import get_json_from_api, fng_json_to_df, save_data


def main():
    try:
        df_btc = yf.download(BTC_TICKER)
        save_data(df_btc, PATH_BTC)        
        fng_json = get_json_from_api(URL_FNG)
        df_fng = fng_json_to_df(fng_json)
        save_data(df_fng, PATH_FNG)
    except Exception as Ex:
        print(f'Error: {Ex}')


if __name__ == "__main__":
    main()