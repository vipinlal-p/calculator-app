# Calculator App

A modern, feature-rich calculator application built with Python and Tkinter. This project demonstrates a clean, scalable, and professional-grade desktop application.

![Calculator Screenshot](https://via.placeholder.com/600x400.png?text=Calculator+Screenshot)

## Features

- **Standard and Scientific Modes**: Switch between a simple calculator for basic arithmetic and a scientific calculator for more advanced functions.
- **Modern UI/UX**: A clean and modern interface with dark and light themes.
- **History Panel**: View and manage your calculation history.
- **Memory Functions**: Store and recall numbers using memory functions (M+, M-, MR, MC).
- **Responsive and Resizable**: The calculator window can be resized to your liking.
- **Copy to Clipboard**: Easily copy the result to your clipboard.
- **Keyboard Support**: Use your keyboard to perform calculations.
- **Error Handling**: Proper error handling for invalid expressions and division by zero.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/calculator-app.git
    cd calculator-app
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application with the following command:

```bash
python main.py
```

## Project Structure

The project is structured with a clear separation of concerns, making it easy to maintain and extend.

```
/
├── src/
│   ├── calculator/
│   │   ├── __init__.py
│   │   ├── app.py          # Main application class
│   │   ├── logic.py        # Calculator logic
│   │   ├── ui.py           # UI components
│   │   ├── history.py      # History management
│   │   └── theme.py        # Theme management
│   └── __init__.py
├── main.py                 # Application entry point
├── requirements.txt        # Project dependencies
└── README.md
```

## Future Improvements

-   [ ] Add more scientific functions.
-   [ ] Add support for custom themes.
-   [ ] Add unit tests for the logic and UI.
-   [ ] Package the application for distribution (e.g., using PyInstaller).
-   [ ] Add more keyboard shortcuts.
