# ✨ AnsCom Terminal v2.0 ✨

### The Market, At Your Command.

![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![Libraries](https://img.shields.io/badge/libraries-matplotlib%2C%20selenium%2C%20pandas-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

**AnsCom Terminal** is a sophisticated, real-time stock and crypto analysis tool with a professional, Bloomberg-inspired interface. This major v2.0 update transforms the terminal from a single-asset viewer into a dynamic market analysis powerhouse.

The headline feature is **full market access**. We've replaced the static header with a powerful interactive **Command & Search Bar**, giving you direct access to the entire Nifty 500 Indian stock market, complete with intelligent, live search suggestions.

<br>

<!-- Replace with a real screenshot URL -->
 

<br>

---

## 🚀 WHAT'S NEW IN v2.0: FULL MARKET ACCESS

This update is all about speed, access, and intuitive control.

### #FullMarketAccess
The terminal now comes pre-loaded with data for the **Nifty 500**. Track any major Indian stock, not just the default.

### #InteractiveCommandBar
A new dynamic command bar is your gateway to the market. Type your command to instantly switch between different stocks and update your share quantity.

### #LiveSearch
No need to memorize every ticker. As you type a stock symbol, a list of matching companies appears instantly. Just click to select.

### #SeamlessSwitching
When you load a new stock, the entire terminal adapts. The chart, profit calculations, and all info panels reset automatically for a clean, fresh analysis of the new asset.

### #ZeroConfigSetup
The terminal now automatically generates the required `ind_nifty500list.csv` file if it's not found on first launch. It just works, right out of the box.

---

## 📊 CORE FEATURES

*   **Real-Time Data Feed**: Live price data scraped reliably from TradingView, updating every second.
*   **Professional Dark UI**: A custom, Bloomberg-inspired theme designed for focus and clarity.
*   **Live P/L Analysis**: See your profit & loss calculated and plotted in real-time based on your specified share count.
*   **Comprehensive Info Panel**: Instant view of:
    *   Live Profit/Loss (color-coded)
    *   Current Market Price (color-coded ticks)
    *   Total Holding Value
    *   Day's Price & Percentage Change
    *   5-Period Simple Moving Average (SMA)
*   **Advanced On-Chart Drawing Tools**:
    *   **Pencil & Line**: Draw trendlines and annotations directly on the chart.
    *   **Measure Tool**: Instantly calculate price change, percentage return, and time delta between any two points on the plot.

---

## 🛠️ INSTALLATION & USAGE

### #Setup

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/AnsCom-Terminal.git
    cd AnsCom-Terminal
    ```

2.  **Install Dependencies** (It's highly recommended to use a Python virtual environment):
    ```bash
    pip install matplotlib selenium pandas numpy webdriver-manager
    ```

3.  **Run the Terminal**:
    ```bash
    python your_script_name.py
    ```
    The script will handle the rest, including creating the `ind_nifty500list.csv` file and launching the necessary web driver.

### #HowToUse

1.  The terminal opens with the **Command Bar** at the top.
2.  To find a stock, start typing its ticker symbol after the `MARKET INDIA NSE` prefix (e.g., `RELIANCE`).
3.  An **auto-suggestion box** will appear. Simply **click** on your desired stock.
4.  Alternatively, type the full command and press **Enter**.

#### Command Syntax:
