"""
Usage for MacOS (in terminal):
    cd to PyShiny/
    create a virtual environment from the requirements_no-deps.txt
    run the virtual environment using 'source venv/bin/activate'
    cd to app/
    run 'shiny run app.py'
    copy and paste the http local host to browser

Usage for Windows:
    create a virtual environment from the requirements_no-deps.txt
    run '.\env\Scripts\activate'
    run this script with the host ip if applicable

Author: Jesse Liu
"""

from shiny import run_app

if __name__ == '__main__':
    run_app(launch_browser=True, reload=False, app_dir='app/')  # add host
