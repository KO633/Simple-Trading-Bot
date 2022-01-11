from alpaca_trade_api.rest import REST, TimeFrame, TimeFrameUnit
import numpy as np
import time
import os

# insert personal id and secret key registered on alpaca trades on paper by default
# for real trading remove base url line
os.environ['APCA_API_SECRET_KEY'] = ''
os.environ['APCA_API_KEY_ID'] = ''
os.environ['APCA_API_BASE_URL'] = 'https://paper-api.alpaca.markets'
api = REST()

symb = "EMTL"
pos_held = False

while True:
    print("")
    print("Checking Price")

    market_data = api.get_bars(symb, TimeFrame(5, TimeFrameUnit.Minute))

    close_list = []
    for bar in market_data:
        close_list.append(bar.c)

    close_list = np.array(close_list, dtype=np.float64)
    ma = np.mean(close_list)
    last_price = close_list[4]

    print("Moving Average: " + str(ma))
    print("Last Price: " + str(last_price))

    if ma + 0.1 < last_price and not pos_held:
        print("Buy")
        api.submit_order(
            symbol=symb,
            qty=1,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        pos_held = True

    elif ma - 0.1 > last_price and pos_held:
        print("Sell")
        api.submit_order(
            symbol=symb,
            qty=1,
            side='sell',
            type='market',
            time_in_force='gtc'
        )

        pos_held = False

    time.sleep(60)
