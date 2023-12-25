import yfinance as yf
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mplfinance as mpf
import matplotlib.dates as mdates
from win32api import GetSystemMetrics
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential,load_model
from keras.layers import LSTM, Dense

# Function to fetch stock data using yfinance
def get_stock_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    return data

# Function to predict stock prices using LSTM
def predict_stock_prices(data):
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
    test_data = np.reshape(test_data, (1, test_data.shape[0], 1))

    # Making predictions
    predictions = model.predict(test_data)
    predictions = scaler.inverse_transform(predictions)

    return predictions

def display_predictions(stock_name, future_dates, predicted_prices):
    # Ensure future_dates and predicted_prices have the same dimension
    future_dates = future_dates[:len(predicted_prices)]

    # Print the data for debugging
    print("Future Dates:", future_dates)
    print("Predicted Prices:", predicted_prices)

    # Create a new frame for each stock prediction
    prediction_frame = ttk.Frame(predictions_tab)
    prediction_frame.pack(pady=10)

    title = f"{stock_name} Predictions"
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

# Function to handle button click event
def button_click(stock_symbol, start_date, end_date):
    # Destroy the existing chart widgets if they exist
    for widget in container_frame.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.destroy()

    stock_data = get_stock_data(stock_symbol, start_date, end_date)
    current_price = stock_data['Close'][-1]

    # Create and display the chart in the container frame
    chart = create_chart(stock_data, stock_symbol, current_price)
    canvas = FigureCanvasTkAgg(chart, master=container_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(expand=True, fill='both')

    # Update the container frame
    container_frame.update_idletasks()

    # Predict stock prices for the next 30 days
    last_date = stock_data.index[-1]
    future_dates = pd.date_range(start=last_date, periods=30, freq='B')[1:]
    predicted_prices = predict_stock_prices(stock_data)

    # Display predictions
    display_predictions(stock_symbol, future_dates, predicted_prices)


# Function to switch to the predictions page
def show_predictions_page():
    notebook.select(predictions_tab)

# Create the main window
window = tk.Tk()
window.title("Stock Market Analysis")

# Set the window size to the screen size
screen_width = GetSystemMetrics(0)
screen_height = GetSystemMetrics(1)
window.geometry(f"{screen_width}x{screen_height}")

# Create a notebook (tabs container)
notebook = ttk.Notebook(window)

# Home Page
home_tab = ttk.Frame(notebook)
notebook.add(home_tab, text="Home")

# Create a container frame for graphs
container_frame = ttk.Frame(home_tab)
container_frame.pack(expand=True, fill='both')

# Label for error messages
error_label = ttk.Label(home_tab, text="", foreground="red")
error_label.pack(pady=10)

# Button for most popular stocks
popular_stocks_frame = ttk.Frame(home_tab)
popular_stocks_frame.pack(pady=10)

popular_stocks_label = ttk.Label(popular_stocks_frame, text="Most Popular Stocks:")
popular_stocks_label.pack(side="left", padx=10)

# Example popular stocks (replace with actual popular stocks)
popular_stocks = ["AAPL", "GOOGL", "AMZN", "MSFT"]
for stock in popular_stocks:
    button = ttk.Button(popular_stocks_frame, text=stock, command=lambda s=stock: button_click(s, '2020-01-01', '2023-12-31'))
    button.pack(side="left", padx=5)

# Section for pinged stocks (replace with actual functionality)
pinged_stocks_frame = ttk.Frame(home_tab)
pinged_stocks_frame.pack(pady=10)

pinged_stocks_label = ttk.Label(pinged_stocks_frame, text="Pinged Stocks:")
pinged_stocks_label.pack(side="left", padx=10)

# Example pinged stocks (replace with actual pinged stocks)
pinged_stocks = ["GOOGL", "MSFT", "AAPL"]
for stock in pinged_stocks:
    button = ttk.Button(pinged_stocks_frame, text=stock, command=lambda s=stock: button_click(s, '2020-01-01', '2023-12-31'))
    button.pack(side="left", padx=5)

# Button to switch to the predictions page
predictions_button_home = ttk.Button(home_tab, text="Go to Predictions", command=show_predictions_page)
predictions_button_home.pack(pady=10)

# Predictions Page
predictions_tab = ttk.Frame(notebook)
notebook.add(predictions_tab, text="Predictions")

# Placeholder content for the predictions page
predictions_label = ttk.Label(predictions_tab, text="This is the predictions page.")
predictions_label.pack(pady=10)

# Start the application
notebook.pack(expand=True, fill="both")
window.mainloop()