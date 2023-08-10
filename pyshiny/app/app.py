"""
Calls the ui and server modules and connect it to the App

Author: Jesse Liu
"""

from pathlib import Path
from shiny import App
from ui import app_ui
from server import server

www_dir = Path(__file__).parent / "contents/utils/www"
app = App(app_ui(), server, debug=True, static_assets=www_dir)
