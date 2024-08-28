"""
Entrypoint

Example:
    python main.py
"""

from src.utilities import gen_k_random_trades, parse_price, STOCKS, TRADES


if __name__ == "__main__":
    print('\n\nStarting state...')

    print(STOCKS)

    print('\n\nCalculate formulas for a given stock and price...')

    while True:
        try:
            print('\nNote: Hit CTRL-c or CTRL-d to exit this mode')
            symbol = input('\nType any of the symbol abbreviations from the StockDB > ')
            price = input('Type a price in $ > ')

            price = parse_price(price)

            print(f'Dividend yield is: {STOCKS[symbol].dividend_yield(price)}')  # pylint: disable=E1136
            print(f'P/E ratio is: {STOCKS[symbol].pe_ratio(price)}')  # pylint: disable=E1136
        except (KeyboardInterrupt, EOFError):
            break
        except (ValueError, KeyError) as exc:
            print('\n!!! Wrong input:')
            print(f'\tException occured: {exc}')

    print('\n\nRegistering transactions...')
    print(TRADES)

    for trade_with_ts in gen_k_random_trades(150):
        TRADES.add(trade_with_ts)

    print(TRADES)

    print('\n\nCalculate Volume Weighted Stock Price for a given stock symbol')
    print(STOCKS)
    while True:
        try:
            print('\nNote: Hit CTRL-c or CTRL-d to exit this mode')
            symbol = input('\nType any of the symbol abbreviations from the StockDB > ')

            print(
                f'\nVolume weighted stock price in past 15 minutes for'
                f' stock {symbol} is {TRADES.volume_weighted_stock_price(symbol):.4f}'
            )
        except (KeyboardInterrupt, EOFError):
            break
        except (ValueError, KeyError) as exc:
            print('\n!!! Wrong input:')
            print(f'\tException occured: {exc}')
            continue

    print(f'\nGBCE all share index for all shares {TRADES.gbce_all_share_index():.4f}')
