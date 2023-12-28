import yfinance as yf
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.impute import SimpleImputer
import pandas as pd
import numpy as np
from ta import add_all_ta_features
from joblib import dump

# Step 1: Get Historical Stock Data
sp500 = yf.Ticker("^GSPC")
historical_data = sp500.history(period="5y")

# Preprocess Data
historical_data["Target"] = np.where(historical_data["Close"].shift(-1) > historical_data["Close"], 1, 0)
historical_data = historical_data.dropna()

# Feature Engineering
historical_data = add_all_ta_features(historical_data, open="Open", high="High", low="Low", close="Close", volume="Volume")
historical_data["SMA_50"] = historical_data["Close"].rolling(window=50).mean()
historical_data["SMA_200"] = historical_data["Close"].rolling(window=200).mean()

# Select features and target
predictors = [
    "Close",
    "Volume",
    "momentum_rsi",
    "trend_macd_signal",
    "trend_sma_fast",
    "trend_sma_slow",
    "SMA_50",
    "SMA_200"
]
target = "Target"



# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    historical_data[predictors], historical_data[target], test_size=0.2, random_state=42
)

X_train = X_train.dropna()
y_train = y_train[X_train.index]  # Update y_train accordingly

X_test = X_test.dropna()
y_test = y_test[X_test.index]  # Update y_test accordingly

# Train a RandomForestClassifier
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

model = RandomForestClassifier(random_state=1)
grid_search = GridSearchCV(model, param_grid, scoring='precision', cv=3)
grid_search.fit(X_train, y_train)

# Get the best parameters
best_params = grid_search.best_params_

# Train the model with the best parameters
best_model = RandomForestClassifier(random_state=1, **best_params)
best_model.fit(X_train, y_train)

# Save the trained model
dump(best_model, 'random_forest_model.joblib')