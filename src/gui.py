import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from win32api import GetSystemMetrics
from functions import get_stock_data, predict_stock_prices, get_stock_data_with_selenium, display_predictions, create_chart
import pandas as pd

# Define the MainWindow class
class MainWindow:
    def __init__(self, window):
        self.window = window
        self.window.title("Stock Market Analysis")

        # Set the window size to the screen size
        screen_width = GetSystemMetrics(0)
        screen_height = GetSystemMetrics(1)
        self.window.geometry(f"{screen_width}x{screen_height}")

        # Create a notebook (tabs container)
        self.notebook = ttk.Notebook(self.window)

        # Home Page
        self.home_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.home_tab, text="Home")

        # Create a container frame for graphs
        self.container_frame = ttk.Frame(self.home_tab)
        self.container_frame.pack(expand=True, fill='both')

        # Label for error messages
        self.error_label = ttk.Label(self.home_tab, text="", foreground="red")
        self.error_label.pack(pady=10)

        # Button for most popular stocks
        self.popular_stocks_frame = ttk.Frame(self.home_tab)
        self.popular_stocks_frame.pack(pady=10)

        popular_stocks_label = ttk.Label(self.popular_stocks_frame, text="Most Popular Stocks:")
        popular_stocks_label.pack(side="left", padx=10)

        # Example popular stocks (replace with actual popular stocks)
        popular_stocks = ["AAPL", "GOOGL", "AMZN", "MSFT"]
        for stock in popular_stocks:
            button = ttk.Button(self.popular_stocks_frame, text=stock,
                                command=lambda s=stock: self.button_click(s, '2020-01-01', '2023-12-31'))
            button.pack(side="left", padx=5)

        # Section for pinged stocks (replace with actual functionality)
        self.pinged_stocks_frame = ttk.Frame(self.home_tab)
        self.pinged_stocks_frame.pack(pady=10)

        pinged_stocks_label = ttk.Label(self.pinged_stocks_frame, text="Pinged Stocks:")
        pinged_stocks_label.pack(side="left", padx=10)

        # Example pinged stocks (replace with actual pinged stocks)
        pinged_stocks = ["GOOGL", "MSFT", "AAPL"]
        for stock in pinged_stocks:
            button = ttk.Button(self.pinged_stocks_frame, text=stock,
                                command=lambda s=stock: self.button_click(s, '2020-01-01', '2023-12-31'))
            button.pack(side="left", padx=5)

        # Button to switch to the predictions page
        predictions_button_home = ttk.Button(self.home_tab, text="Go to Predictions", command=self.show_predictions_page)
        predictions_button_home.pack(pady=10)

        # Predictions Page
        self.predictions_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.predictions_tab, text="Predictions")

        # Placeholder content for the predictions page
        predictions_label = ttk.Label(self.predictions_tab, text="This is the predictions page.")
        predictions_label.pack(pady=10)

        # Button for scraping data
        scrape_data_button = ttk.Button(self.home_tab, text="Scrape Data",
                                        command=lambda: self.scrape_data_button_click("AAPL", '2020-01-01', '2023-12-31'))
        scrape_data_button.pack(pady=10)

        scrape_data_button_selenium = ttk.Button(self.home_tab, text="Scrape Data with Selenium",
                                                 command=lambda: self.scrape_data_button_click_with_selenium("AAPL", '2020-01-01', '2023-12-31'))
        scrape_data_button_selenium.pack(pady=10)

        # Start the application
        self.notebook.pack(expand=True, fill="both")
        self.window.mainloop()

    def show_predictions_page(self):
        self.notebook.select(self.predictions_tab)

    def button_click(self, stock_symbol, start_date, end_date):
        # Destroy the existing chart widgets if they exist
        for widget in self.container_frame.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.destroy()
    
        stock_data = get_stock_data(stock_symbol, start_date, end_date)
        current_price = stock_data['Close'][-1]
    
        # Create and display the chart in the container frame
        chart = create_chart(stock_data, stock_symbol, current_price)
        canvas = FigureCanvasTkAgg(chart, master=self.container_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(expand=True, fill='both')
    
        # Update the container frame
        self.container_frame.update_idletasks()
    
        # Predict stock prices for the next 30 days
        last_date = stock_data.index[-1]
        future_dates = pd.date_range(start=last_date, periods=30, freq='B')
        predicted_prices = predict_stock_prices(stock_data, num_days=30)
    
        # Display predictions
        display_predictions(self.predictions_tab, stock_symbol, future_dates, predicted_prices)

    def scrape_data_button_click(self, stock_symbol, start_date, end_date):
        try:
            # Fetch stock data
            stock_data = get_stock_data(stock_symbol, start_date, end_date)
    
            # Predict stock prices for the next 30 days
            last_date = stock_data.index[-1]
            future_dates = pd.date_range(start=last_date, periods=30, freq='B')[1:]
            predicted_prices = predict_stock_prices(stock_data, num_days=30)
    
            # Display predictions
            display_predictions(self.predictions_tab, stock_symbol, future_dates, predicted_prices)
    
            # Save data to a CSV file (you can customize the filename)
            csv_filename = f"{stock_symbol}_data.csv"
            stock_data.to_csv(csv_filename, index=False)
    
            # Show success message
            self.error_label.config(text=f"Data scraped successfully and saved to {csv_filename}", foreground="green")
    
        except Exception as e:
        # Show error message
            self.error_label.config(text=f"Error: {str(e)}", foreground="red")

    def scrape_data_button_click_with_selenium(self, stock_symbol, start_date, end_date):
        try:
            # Fetch stock data using Selenium
            stock_data = get_stock_data_with_selenium(stock_symbol, start_date, end_date)
    
            # Predict stock prices for the next 30 days
            last_date = stock_data.index[-1]
            future_dates = pd.date_range(start=last_date, periods=30, freq='B')[1:]
            predicted_prices = predict_stock_prices(stock_data, num_days=30)
    
            # Display predictions
            display_predictions(self.predictions_tab, stock_symbol, future_dates, predicted_prices)
    
            # Save data to a CSV file (you can customize the filename)
            csv_filename = f"{stock_symbol}_data_with_selenium.csv"
            stock_data.to_csv(csv_filename, index=False)
    
            # Show success message
            self.error_label.config(text=f"Data scraped successfully and saved to {csv_filename}", foreground="green")
    
        except Exception as e:
            # Show error message
            self.error_label.config(text=f"Error: {str(e)}", foreground="red")

    def show_predictions_page(self):
        self.notebook.select(self.predictions_tab)

# Create the main window
if __name__ == "__main__":
    window = tk.Tk()
    app = MainWindow(window)
    window.mainloop()