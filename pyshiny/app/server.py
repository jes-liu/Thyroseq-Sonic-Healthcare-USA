"""
The server of the app where inputs, outputs, and session information are handled

Author: Jesse Liu
"""

import os
from shiny import render, ui, reactive
from shiny.types import ImgData
from shinywidgets import render_widget
from contents.features.plots import Plots
from contents.features.query import Query
from contents.features.reports import Report
from contents.connections.connect_db import Connect
from contents.utils.utils import choices, create_mgp_table, convert_mgp_to_wf


# The server that houses the inputs from the user, spits out the outputs, and stores session information for downloads
def server(input, output, session):

    # region ----------------------------------- QUERY -----------------------------------
    # Grab the query based on inputs that are used as filters for SQLite
    def get_query(limit, style):
        db = Query().get_thyroseq_db(columns=input.columns(),
                                     limit=[limit, input.limit()],
                                     style=style
                                     )
        return db

    # Renders the queried table into an output
    @output
    @render.table
    def thyroseq_db():
        return get_query(limit=True, style=True)

    # Creates a path to a temp csv file when the download button is clicked to be outputted as the download
    @session.download(filename='name.csv')
    def download_db_csv():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Downloading Table", detail="pulling query")
            df = get_query(limit=False, style=False)
            progress.inc(2, detail="saving to csv")
            df.to_csv('contents/utils/tmp/temp_data.csv', index=False)
            progress.inc(2, detail="fetching file")
            path = os.path.join(os.path.dirname(__file__), 'contents/utils/tmp/temp_data.csv')
            progress.inc(2, detail="downloaded")
        return path
    # endregion

    # region ----------------------------------- PLOTS -----------------------------------
    # Creates a bar plot from the queried table
    @output
    @render_widget()
    def bar_plot():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Drawing Bar Plot", detail='pulling query')
            db = get_query(limit=False, style=False)
            progress.inc(3, detail='plotting')
            plot = Plots(db).bar_plot(bar_choice_range=input.bar_choice_range(),
                                      bar_choice_category=input.bar_choice_category()
                                      )
            progress.inc(3, detail='finished')
        return plot

    # Creates a pie chart from the queried table
    @output
    @render_widget()
    def pie_chart():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Drawing Pie Chart", detail='pulling query')
            db = get_query(limit=False, style=False)
            progress.inc(3, detail='plotting')
            plot = Plots(db).pie_chart(pie_choice=input.pie_choice(),
                                       date=input.date()
                                       )
            progress.inc(3, detail='finished')
        return plot

    # Creates a turn around time graph
    @output
    @render_widget()
    def turn_around_time():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Drawing Turn Around Time", detail='pulling query')
            db = get_query(limit=False, style=False)
            progress.inc(3, detail='plotting')
            plot = Plots(db).turn_around_time(date=input.date(),
                                              from_=input.turn_around_time_from(),
                                              to_=input.turn_around_time_to()
                                              )
            progress.inc(3, detail='finished')
        return plot

    # Creates a time graph with categorical choices
    @output
    @render_widget()
    def time_graph():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Drawing Reports Over Time", detail='pulling query')
            db = get_query(limit=False, style=False)
            progress.inc(3, detail='plotting')
            plot = Plots(db).time_graph(date_type=input.date_type(),
                                        time_choice=input.time_choice())
            progress.inc(3, detail='finished')
        return plot

    # Creates a bar plot
    @output
    @render_widget()
    def physician_plot():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Drawing Physician Plot", detail='pulling query')
            db = get_query(limit=False, style=False)
            progress.inc(3, detail='plotting')
            plot = Plots(db).physician_plot(columns=input.columns(),
                                            )
            progress.inc(3, detail='finished')
        return plot

    # Creates a path to a temp distribution png when the download button is clicked to be outputted as the download
    @session.download(filename='Bar_plot.png')
    def download_bar_png():
        with ui.Progress(min=0, max=3) as progress:
            progress.set(0, message="Downloading Table", detail="pulling query")
            db = get_query(limit=False, style=False)
            progress.inc(1, detail="generating table")
            _ = Plots(db).bar_plot_db(bar_choice_range=input.bar_choice_range(),
                                      bar_choice_category=input.bar_choice_category())
            progress.inc(1, detail="saving to png")
            path = os.path.join(os.path.dirname(__file__), 'contents/utils/tmp/temp_png.png')
            progress.inc(1, detail="downloaded")
        return path

    # Creates a path to a temp distribution csv file when the download button is clicked to be outputted as the download
    @session.download(filename='Bar_plot.csv')
    def download_bar_csv():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Downloading Table", detail="pulling query")
            db = get_query(limit=False, style=False)
            progress.inc(1.5, detail="generating table")
            df = Plots(db).bar_plot_db(bar_choice_range=input.bar_choice_range(),
                                       bar_choice_category=input.bar_choice_category())
            progress.inc(1.5, detail="saving to csv")
            df.to_csv('contents/utils/tmp/temp_data.csv', index=False)
            progress.inc(1.5, detail="fetching file")
            path = os.path.join(os.path.dirname(__file__), 'contents/utils/tmp/temp_data.csv')
            progress.inc(1.5, detail="downloaded")
        return path

    # Creates a path to a temp tat csv file when the download button is clicked to be outputted as the download
    @session.download(filename='name.csv')
    def download_tat_csv():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Downloading Table", detail="pulling query")
            db = get_query(limit=False, style=False)
            progress.inc(1.5, detail="generating table")
            df = Plots(db).turn_around_time_db(from_=input.turn_around_time_from(), to_=input.turn_around_time_to())
            progress.inc(1.5, detail="saving to csv")
            df.to_csv('contents/utils/tmp/temp_data.csv', index=False)
            progress.inc(1.5, detail="fetching file")
            path = os.path.join(os.path.dirname(__file__), 'contents/utils/tmp/temp_data.csv')
            progress.inc(1.5, detail="downloaded")
        return path

    # Creates a path to a temp phy csv file when the download button is clicked to be outputted as the download
    @session.download(filename='name.csv')
    def download_phy_csv():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Downloading Table", detail="pulling query")
            db = get_query(limit=False, style=False)
            progress.inc(1.5, detail="generating table")
            df = Plots(db).physician_plot_db(columns=input.columns(),)
            progress.inc(1.5, detail="saving to csv")
            df.to_csv('contents/utils/tmp/temp_data.csv', index=False)
            progress.inc(1.5, detail="fetching file")
            path = os.path.join(os.path.dirname(__file__), 'contents/utils/tmp/temp_data.csv')
            progress.inc(1.5, detail="downloaded")
        return path
    # endregion

    # region ----------------------------------- UTILS -----------------------------------
    @reactive.event(input.password_go)
    def password_check():
        password = False
        if input.password() == "SHINY":
            password = True
        return password

    @output
    @render.text()
    def password_correct():
        if password_check():
            ui.remove_ui(selector="div:has(> #password)")
            ui.remove_ui(selector="div:has(> #password_go)")
            ui.remove_ui(selector="div:has(> #password_correct)")
            return 'Password Correct'
        else:
            return 'Password Incorrect'

    @reactive.Effect
    @reactive.event(input.turn_around_time_from)
    def _():
        to_choices = ['date']
        choice_index = to_choices.index(input.turn_around_time_from()) + 1
        ui.update_select(
            id='turn_around_time_to',
            choices=to_choices[choice_index:]
        )

    @reactive.Effect
    @reactive.event(input.column_not_all)
    def unselect_all():
        ui.update_checkbox_group(
            id='columns',
            label=None,
            selected='id'
        )

    @reactive.Effect
    @reactive.event(input.column_all)
    def select_all():
        ui.update_checkbox_group(
            id='columns',
            label=None,
            selected=choices()['Columns']
        )

    @reactive.Effect
    @reactive.event(input.column_default)
    def select_default():
        ui.update_checkbox_group(
            id='columns',
            label=None,
            selected=['col_1', 'col _2', 'col_3']
        )

    session.on_ended(Connect().close_connection)
    @reactive.Effect
    @reactive.event(input.close)
    async def __():
        await session.close()
    # endregion

    # region ----------------------------------- REPORTS ---------------------------------
    # Creates a path to a temp png file to be outputted as a report image
    @output
    @render.image
    @reactive.event(input.report_go, input.report_go_success, input.report_go_failed)
    def generate_report():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Generating Report")
            progress.inc(3, detail='adding information')
            png_file = Report(columns=input.columns()).generate_temp_report()
            path = os.path.join(os.path.dirname(__file__), 'contents/utils/tmp', png_file)
            # noinspection PyTypeChecker
            img: ImgData = {'src': str(path), 'width': '300%', 'height': '450%', 'alt': '', 'style': ''}
            progress.inc(3, detail="finished")
        return img

    # Creates a path to a temp pdf file when the download button is clicked to be outputted as the download
    @session.download(filename='name.pdf')
    def download_report():
        with ui.Progress(min=0, max=6) as progress:
            progress.set(0, message="Downloading Table", detail="generating full report")
            pdf_file = Report(columns=input.columns()).generate_full_report()
            progress.inc(3, detail="fetching file")
            path = os.path.join(os.path.dirname(__file__), 'contents/utils/tmp', pdf_file)
            progress.inc(3, detail="downloaded")
        return path
    # endregion

    # region ---------------------------------- MGP-to-WF --------------------------------
    # Convert
    @output
    @render.text()
    @reactive.event(input.mgp_go, input.mgp_go_failed, input.mgp_go_success)
    def mgp_out():
        with ui.Progress(min=0, max=1) as progress:
            progress.set(0, message="Converting to", detail="finding number")
            wf_number = Query().query_by_mgp(mgp_in=input.mgp_in(), type='single')
            progress.inc(1, detail="number found")
        return wf_number

    # Function to check file upload success or fail
    def upload_success_fail():
        if input.mgp_in_file is not None:
            return 'File Uploaded!'
        else:
            return 'Failed Upload!'

    # Checks if a file has been uploaded
    @output
    @render.text()
    @reactive.event(input.mgp_go_file, input.mgp_go_file_success, input.mgp_go_file_failed)
    def mgp_file_check():
        return upload_success_fail()

    # Shows the input file in HTML format
    @output
    @render.ui()
    @reactive.event(input.mgp_in_file)
    def mgp_table():
        file = input.mgp_in_file()
        table = create_mgp_table(file)
        return ui.HTML(table)

    # Converts
    @output
    @render.ui()
    @reactive.event(input.mgp_go_file, input.mgp_go_file_success, input.mgp_go_file_failed)
    def mgp_to_wf():
        file = input.mgp_in_file()
        mgp_df = convert_mgp_to_wf(file)
        mgp_df.to_csv(os.path.join(os.path.dirname(__file__), 'contents/utils/tmp/temp_data.csv'), index=False)
        mgp_df = mgp_df.style.format(). \
            set_table_attributes('class="table-striped table"'). \
            set_table_styles([dict(selector="th", props='text-align:center; border:1px solid'),
                              dict(selector="td", props='text-align:center; border:1px solid'), ]). \
            to_html()
        return ui.HTML(mgp_df)

    # Creates a path to a temp mgp csv file when the download button is clicked to be outputted as the download
    @session.download(filename='name.csv')
    def download_mgp_csv():
        with ui.Progress(min=0, max=1) as progress:
            progress.set(0, message="Downloading Table", detail="fetching file")
            path = os.path.join(os.path.dirname(__file__), 'contents/utils/tmp/temp_data.csv')
            progress.inc(1, detail="downloaded")
        return path
    # endregion
