# Wikipedia Reflection Tool

This is a simple GUI application built with PyQt6 that allows users to fetch and view random Wikipedia articles in various languages and themes.

## Features

- Fetch random articles from Wikipedia.
- View article summary, sections, and categories.
- Supports multiple Wikipedia languages.
- Includes a light and dark theme toggle.
- GUI language can be changed between supported languages.

## Requirements

- Python 3.x
- PyQt6
- wikipedia-api
- requests

## Installation

1. Clone or download the repository.
2. Navigate to the project directory.
3. Install the required libraries using pip:

   ```bash
   pip install PyQt6 wikipedia-api requests
   ```

## Usage

1. Run the main script:

   ```bash
   python wiki_gui_tool.py
   ```

2. Use the language dropdowns to select the GUI and Wikipedia article languages.
3. Click "New Random Article" to fetch a new article.
4. Click on the article title to open the full article in your web browser.
5. Use the theme button to switch between light and dark themes. 