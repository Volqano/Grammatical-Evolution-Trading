import yfinance as yf


def calculate_rsi(series, period):
    """RSI mowi nam o sile aktywow sugerujac czy sa overbought czy oversold"""
    delta = series.diff()

    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()

    rs = avg_gain / (avg_loss + 1e-10)
    rsi = 100 - (100 / (1 + rs))

    return rsi


def get_data(ticker, start="2020-01-01", end="2025-01-01"):
    data = yf.download(ticker, start=start, end=end)
    data.columns = data.columns.get_level_values(0)

    data["SMA10"] = data["Close"].rolling(10).mean()
    data["SMA50"] = data["Close"].rolling(50).mean()
    data["RSI"] = calculate_rsi(data["Close"], period=14)

    data = data.dropna()

    return data


def get_fast_data(ticker, start="2020-01-01", end="2025-01-01"):
    data = yf.download(ticker, start=start, end=end)
    data.columns = data.columns.get_level_values(0)

    data["SMA10"] = data["Close"].rolling(10).mean()
    data["SMA50"] = data["Close"].rolling(50).mean()
    data["RSI"] = calculate_rsi(data["Close"], period=14)

    data = data.dropna()

    return {col: data[col].values for col in data.columns}  # zamiana na slownik do szybszych operacji
