import yfinance as yf
import pandas as pd  # Add this line
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf
import matplotlib.dates as mdates
from win32api import GetSystemMetrics
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Function to fetch stock data using yfinance
def get_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Function to predict stock prices using LSTM
def predict_stock_prices(data, num_days=30):
    # Extracting the closing prices
    dataset = data['Close'].values.reshape(-1, 1)

    # Scaling the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    dataset_scaled = scaler.fit_transform(dataset)

    # Creating the input data for the LSTM model
    x_train, y_train = [], []
    for i in range(60, len(dataset_scaled)):
        x_train.append(dataset_scaled[i-60:i, 0])
        y_train.append(dataset_scaled[i, 0])
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshaping the data for LSTM
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # Building the LSTM model
    model = Sequential()
    model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(units=50, return_sequences=False))
    model.add(Dense(units=25))
    model.add(Dense(units=1))

    # Compiling the model
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Training the model
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    # Creating the test data
    test_data = dataset_scaled[len(dataset_scaled) - 60:, :]

    # Reshaping the data
    test_data = dataset_scaled[len(dataset_scaled) - 60:, :]

    # Reshaping the data
    test_data = np.reshape(test_data, (1, test_data.shape[0], 1))

    # Making predictions for multiple days into the future
    predictions = []
    for _ in range(num_days):
        prediction = model.predict(test_data)
        predictions.append(scaler.inverse_transform(prediction))

        # Update test_data for the next prediction
        test_data = np.append(test_data[:, 1:, :], prediction.reshape(1, 1, 1), axis=1)

    return predictions

# Function to fetch stock data using yfinance and Selenium
def get_stock_data_with_selenium(symbol, start_date, end_date):
    # Use Selenium to open a browser and navigate to a financial website
    driver = webdriver.Chrome()  # You may need to specify the path to your chromedriver executable
    driver.get(f'https://finance.yahoo.com/quote/{symbol}/history?p={symbol}')

    # Use Selenium to interact with the website and input date ranges
    start_date_input = driver.find_element(By.NAME, 'startDate')
    start_date_input.clear()
    start_date_input.send_keys(start_date)

    end_date_input = driver.find_element(By.NAME, 'endDate')
    end_date_input.clear()
    end_date_input.send_keys(end_date)
    end_date_input.send_keys(Keys.RETURN)

    # Wait for the data to load (you might need to adjust the waiting time based on the website)
    driver.implicitly_wait(10)

    # Extract data from the website
    # (You'll need to customize this part based on the structure of the website)
    # Example: extracting closing prices
    closing_prices = [float(price.text.replace(',', '')) for price in driver.find_elements(By.XPATH, "//td[@data-col='close']/span")]

    # Close the browser
    driver.quit()

    # Create a DataFrame using the extracted data
    data = pd.DataFrame({'Close': closing_prices})

    return data

# Function to display predictions in the GUI
def display_predictions(predictions_tab, stock_symbol, future_dates, predicted_prices):
    # Ensure future_dates and predicted_prices have the same dimension
    future_dates = future_dates[:len(predicted_prices)]

    # Flatten the predicted prices array
    predicted_prices = np.array([price[0][0] for price in predicted_prices])

    # Create a new frame for each stock prediction
    prediction_frame = ttk.Frame(predictions_tab)
    prediction_frame.pack(pady=10)

    title = f"{stock_symbol} Predictions"
    title_label = ttk.Label(prediction_frame, text=title)
    title_label.pack()

    # Create a new figure
    fig, ax = plt.subplots(figsize=(8, 4))

    # Plot predicted prices
    ax.plot(future_dates, predicted_prices, color='red', label='Predicted Prices')
    ax.set_xlabel('Date')
    ax.set_ylabel('Stock Price')
    ax.set_title(title)
    ax.legend()
    plt.tight_layout()

    # Display the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=prediction_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill='both')

# Function to create a financial chart
def create_chart(data, stock_name, current_price, predicted_prices=None):
    data.index = pd.to_datetime(data.index)

    # Create subplots with shared x-axis
    fig, (ax, ax_vol) = plt.subplots(2, 1, figsize=(8, 6), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    
    title = f"{stock_name} Stock Price\nCurrent Price: {current_price}"
    
    # Plot candlestick chart
    mpf.plot(data, type='candle', style='yahoo', mav=(10, 20), ax=ax, volume=ax_vol)

    if predicted_prices is not None:
      future_dates = pd.date_range(start=data.index[-1], periods=len(predicted_prices)+1, freq='B')[1:]
      ax.plot(future_dates, predicted_prices, color='red', label='Predicted Prices')
    
    # Set the title only if the figure is not None
    if fig is not None:
        fig.suptitle(title)

    ax.set_ylabel('Price')
    ax_vol.set_ylabel('Volume')
    
    # Customize axes and grid lines
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.grid(True)
    
    plt.tight_layout()
    
    # Return the figure without displaying it in the Tkinter window
    return fig