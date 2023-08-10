"""
Defines the UI of the web app

Author: Jesse Liu
"""

import shinyswatch
from shiny import ui
from shinywidgets import output_widget
from contents.utils.utils import choices


def app_ui():
    page = ui.page_fluid(
        ui.tags.div(
            ui.row(
                ui.column(3, ui.input_password(id='password', label='', placeholder='Enter Password', width='100%')),
                ui.column(1, ui.input_action_button(id='password_go', label='Enter', width='100%')),
            ),
            ui.column(2, ui.output_text(id='password_correct')),
            style='text-align: center; margin-left: 650px'
        ),
        ui.panel_conditional("output.password_correct == 'Password Correct'",
        shinyswatch.theme.yeti(),

        # The main structuring of the app. Create a layout with a panel_sidebar() and panel_main()
        ui.page_navbar( # should change to nav_menu for scalability
            ui.nav_spacer(),
            ui.nav('DB'),
            ui.nav('EMPTY'),
            title=ui.tags.div(ui.img(src='TSQ_Logo.png',
                                     height='50px',
                                     style='margin:5px'),
                              ui.h4('COMPANY NAME', style='display:flex; margin-top:17px'),
                              style='display:flex; -webkit-filter:drop-shadow(1px 1px 5px); color:#FBFCFC'),
            bg='#288CBC',  # #003366 dark blue color code
            id='navbar_id'),
        # region ---------------------------------- TSQ DB ---------------------------------
        ui.panel_conditional("input.navbar_id == 'DB'",
            ui.layout_sidebar(
                # region ---------------------------------- FILTERS ----------------------------------
                ui.panel_sidebar(
                    # The inputs of the app. This will go in the panel_sidebar() area

                    # Sidebar Title
                    ui.tags.div(ui.h5('FILTER CONDITIONS', style='display:flex; margin-top:15px'),
                                ui.img(src='filter-icon.png',
                                       height='25px',
                                       style='margin-top:15px; margin-left:9px'),
                                style='display:flex'
                                ),

                    # Columns: Select columns to be included in the table
                    ui.input_checkbox('show_columns', 'Select Columns', False),
                    ui.panel_conditional("input.show_columns",
                                         ui.tags.div(
                                             ui.input_action_button(
                                                 id='column_not_all',
                                                 label='Unselect all',
                                                 class_='btn btn-danger btn-sm'),
                                             style='margin-left:20px; margin-top:-10px',
                                         ),
                                         ui.tags.div(
                                             ui.input_action_button(
                                                 id='column_default',
                                                 label='Select default',
                                                 class_='btn btn-secondary btn-sm'),
                                             style='margin-left:120px; margin-top:-31px',
                                         ),
                                         ui.tags.div(
                                             ui.input_action_button(
                                                 id='column_all',
                                                 label='Select all',
                                                 class_='btn btn-success btn-sm'),
                                             style='margin-left:233px; margin-top:-31px',
                                         ),
                                         ui.tags.div(
                                             ui.input_checkbox_group(
                                                 id='columns',
                                                 label=None,
                                                 choices=choices()['Columns'],
                                                 selected=['col_1', 'col_2', 'col_3']),
                                             style='margin-left:20px; margin-top:20px'
                                         )
                    ),

                    # : Create a slider for numeric input range
                    ui.input_checkbox('show_', 'Label', False),
                    ui.panel_conditional("input.show_",
                                         ui.input_slider(
                                             id='id',
                                             label=None,
                                             min=0,
                                             max=100,
                                             value=[0, 100]
                                         )
                    ),
		    
		    # additional UI functions go here

                    # Sort By: Create a selection for which columns to sort by
                    ui.input_checkbox('show_sort', 'Sort', False),
                    ui.panel_conditional("input.show_sort",
                                         ui.input_select(
                                             id='sort',
                                             label=None,
                                             choices=choices()['Sort By']
                                         ),
                                         # True or False: True is ascending, False is descending
                                         ui.input_switch(
                                             id='descending',
                                             label='Descending',
                                             value=False
                                         )
                    ),

                    # Limit: Create a numeric input for num of rows to show
                    ui.input_checkbox('show_limit', 'Number of rows to display (max 20 rows):', False),
                    ui.panel_conditional("input.show_limit",
                                         ui.input_numeric(
                                             id='limit',
                                             label=None,
                                             value=12,
                                             min=1,
                                             max=20,
                                             step=1
                                         )
                    ),

                    # Download the current list in csv
                    ui.row(
                        ui.download_button(
                            id='download_db_csv',
                            label='Download Database CSV',
                            icon=ui.img(src='download-icon.png',
                                        height='18px',
                                        style='margin-bottom:2px'),
                            class_='btn btn-primary'
                        )
                    )
                ),
                # endregion
                ui.panel_main(
                    ui.navset_pill(
                        # region ------------------------------------ DB -----------------------------------
                        # This is the first pill card that shows the database in the output table ui
                        ui.nav(
                            'Database',
                            ui.tags.div(
                                ui.output_table(id='db')
                                        ),
                            icon=ui.img(src='database-icon.png',
                                        height='18px',
                                        style='margin-bottom:2px; margin-right:3px')
                        ),
                        # endregion

                        # region ----------------------------------- PLOTS ---------------------------------
                        # This is the second pill card that shows plots based on the database filters and can be downloaded
                        ui.nav(
                            'Plots',
                            # First row of plots
                            ui.row(
                                ui.column(3,
                                          ui.input_select(
                                              id='bar_choice_range',
                                              label='',
                                              width='100%',
                                              choices=[]
                                          )
                                ),
                                ui.column(3,
                                          ui.input_select(
                                              id='bar_choice_category',
                                              label='',
                                              width='100%',
                                              choices=[]
                                          )
                                ),
                                ui.column(3,
                                          ui.panel_conditional('output.bar_plot == null',
                                                               ui.tags.div(ui.h6(' ')),
                                                               ui.row(
                                                                   ui.download_button(
                                                                       id='download_bar_png_disabled',
                                                                       label='Download PNG',
                                                                       width='96%',
                                                                       icon=ui.img(src='download-icon.png',
                                                                                   height='18px',
                                                                                   style='margin-bottom:2px'),
                                                                       style='margin-top:-8px',
                                                                       class_='btn btn-outline-primary disabled'
                                                                   )
                                                               )
                                          ),
                                          ui.panel_conditional('output.bar_plot != null',
                                                               ui.tags.div(ui.h6(' ')),
                                                               ui.row(
                                                                   ui.download_button(
                                                                       id='download_bar_png',
                                                                       label='Download PNG',
                                                                       width='96%',
                                                                       icon=ui.img(src='download-icon.png',
                                                                                   height='18px',
                                                                                   style='margin-bottom:2px'),
                                                                       style='margin-top:-8px',
                                                                       class_='btn btn-primary'
                                                                   )
                                                               )
                                          )
                                ),
                                ui.column(3,
                                          ui.panel_conditional('output.bar_plot == null',
                                                               ui.tags.div(ui.h6(' ')),
                                                               ui.row(
                                                                   ui.download_button(
                                                                       id='download_bar_csv_disabled',
                                                                       label='Download CSV',
                                                                       width='96%',
                                                                       icon=ui.img(src='download-icon.png',
                                                                                   height='18px',
                                                                                   style='margin-bottom:2px'),
                                                                       style='margin-top:-8px',
                                                                       class_='btn btn-outline-primary disabled'
                                                                   )
                                                               )
                                          ),
                                          ui.panel_conditional('output.bar_plot != null',
                                                               ui.tags.div(ui.h6(' ')),
                                                               ui.row(
                                                                   ui.download_button(
                                                                       id='download_bar_csv',
                                                                       label='Download CSV',
                                                                       width='96%',
                                                                       icon=ui.img(src='download-icon.png',
                                                                                   height='18px',
                                                                                   style='margin-bottom:2px'),
                                                                       style='margin-top:-8px',
                                                                       class_='btn btn-primary'
                                                                   )
                                                               )
                                          )
                                )
                            ),
                            ui.tags.div(
                                output_widget(id='bar_plot'),
                                class_='card'
                            ),
                            # Second row of plots
                            ui.row(
                                ui.column(6,
                                          ui.input_select(
                                              id='pie_choice',
                                              label=' ',
                                              width='100%',
                                              choices=[]
                                          )
                                ),
                            ),
                            ui.tags.div(
                                output_widget(id='pie_chart'),
                                class_='card'
                            ),
                            # Third row of plots
                            ui.row(
                                ui.column(3,
                                          ui.input_select(
                                              id='turn_around_time_from',
                                              label=' ',
                                              width='100%',
                                              selected='',
                                              choices=[]
                                          )
                                ),
                                ui.column(3,
                                          ui.input_select(
                                              id='turn_around_time_to',
                                              label=' ',
                                              width='100%',
                                              choices=[]
                                          )
                                ),
                                ui.column(6,
                                          ui.panel_conditional('output.turn_around_time == null',
                                                               ui.tags.div(ui.h6(' ')),
                                                               ui.row(
                                                                   ui.download_button(
                                                                       id='download_tat_csv_disabled',
                                                                       label='Download CSV',
                                                                       width='98%',
                                                                       icon=ui.img(src='download-icon.png',
                                                                                   height='18px',
                                                                                   style='margin-bottom:2px'),
                                                                       style='margin-top:17px',
                                                                       class_='btn btn-outline-primary disabled'
                                                                   )
                                                               )
                                          ),
                                          ui.panel_conditional('output.turn_around_time != null',
                                                               ui.tags.div(ui.h6(' ')),
                                                               ui.row(
                                                                   ui.download_button(
                                                                       id='download_tat_csv',
                                                                       label='Download CSV',
                                                                       width='98%',
                                                                       icon=ui.img(src='download-icon.png',
                                                                                   height='18px',
                                                                                   style='margin-bottom:2px'),
                                                                       style='margin-top:17px',
                                                                       class_='btn btn-primary'
                                                                   )
                                                               )
                                          )
                                )
                            ),
                            ui.tags.div(
                                output_widget(id='turn_around_time'),
                                class_='card'
                            ),
                            # Fourth row of plots
                            ui.row(
                                ui.column(6,
                                          ui.input_select(
                                              id='time_choice',
                                              label=' ',
                                              width='100%',
                                              choices=[]
                                          )
                                )
                            ),
                            ui.tags.div(
                                output_widget(id='time_graph'),
                                class_='card'
                            ),
                            # Fifth row of plots
                            ui.row(
                                ui.column(6,
                                          ui.input_select(
                                              id='_choice',
                                              label=' ',
                                              width='100%',
                                              choices=[]
                                          )
                                ),
                                ui.column(6,
                                          ui.panel_conditional('output._plot == null',
                                                               ui.tags.div(ui.h6(' ')),
                                                               ui.row(
                                                                   ui.download_button(
                                                                       id='download_phy_csv_disabled',
                                                                       label='Download CSV',
                                                                       width='98%',
                                                                       icon=ui.img(src='download-icon.png',
                                                                                   height='18px',
                                                                                   style='margin-bottom:2px'),
                                                                       style='margin-top:17px',
                                                                       class_='btn btn-outline-primary disabled'
                                                                   )
                                                               )
                                          ),
                                          ui.panel_conditional('output._plot != null',
                                                               ui.tags.div(ui.h6(' ')),
                                                               ui.row(
                                                                   ui.download_button(
                                                                       id='download_phy_csv',
                                                                       label='Download CSV',
                                                                       width='98%',
                                                                       icon=ui.img(src='download-icon.png',
                                                                                   height='18px',
                                                                                   style='margin-bottom:2px'),
                                                                       style='margin-top:17px',
                                                                       class_='btn btn-primary'
                                                                   )
                                                               )
                                          )
                                )
                            ),
                            ui.tags.div(
                                output_widget(id='_plot'),
                                class_='card'
                            ),
                            icon=ui.img(src='plot-icon.png',
                                        height='18px',
                                        style='margin-bottom:2px; margin-right:3px'
                                        )
                        ),
                        # endregion

                        # region ---------------------------------- S --------------------------------
                        # This is the third pill card that generates a png image of the 
                        ui.nav(
                            's',
                            ui.row(
                                ui.tags.div(ui.h6('Enter ID')),
                                ui.column(3,
                                          ui.input_text(
                                              id='db_id',
                                              label='',
                                              width='100%',
                                              value=''
                                          )
                                ),
                                ui.column(2,
                                          ui.panel_conditional('Number(input.db_id) % 1 != 0 || input.db_id == ""',
                                                               ui.input_action_button(
                                                                   id='_go_disabled',
                                                                   label='Generate',
                                                                   width='100%',
                                                                   class_='btn btn-outline-warning disabled'
                                                               )
                                          ),
                                          ui.panel_conditional('Number(input.db_id) % 1 == 0 && input.db_id != "" &&'
                                                               'output.generate_ == null && !input._go',
                                                               ui.input_action_button(
                                                                   id='_go',
                                                                   label='Generate',
                                                                   width='100%',
                                                                   class_='btn btn-warning'
                                                               )
                                          ),
                                          ui.panel_conditional('Number(input.db_id) % 1 == 0 && input.db_id != "" &&'
                                                               'output.generate_ != null',
                                                               ui.input_action_button(
                                                                   id='_go_success',
                                                                   label='Generate Again',
                                                                   width='100%',
                                                                   class_='btn btn-success'
                                                               )
                                          ),
                                          ui.panel_conditional('Number(input.db_id) % 1 == 0 && input.db_id != "" &&'
                                                               'output.generate_ == null && input._go',
                                                               ui.input_action_button(
                                                                   id='_go_failed',
                                                                   label='Generate Again',
                                                                   width='100%',
                                                                   class_='btn btn-danger'
                                                               )
                                          ),
                                ),
                                ui.column(1),
                                ui.column(5,
                                          ui.panel_conditional('output.generate_ == null',
                                                               ui.row(
                                                                   ui.download_button(id='download__disabled',
                                                                                      label='Download PDF',
                                                                                      icon=ui.img(src='download-icon.png',
                                                                                                  height='18px',
                                                                                                  style='margin-bottom:2px'),
                                                                                      class_='btn btn-outline-primary disabled'
                                                                                      )
                                                               )
                                          ),
                                          ui.panel_conditional('output.generate_ != null',
                                                               ui.row(
                                                                   ui.download_button(id='download_',
                                                                                      label='Download PDF',
                                                                                      icon=ui.img(src='download-icon.png',
                                                                                                  height='18px',
                                                                                                  style='margin-bottom:2px'),
                                                                                      class_='btn btn-primary'
                                                                   )
                                                               )
                                          )
                                )
                            ),
                            ui.tags.div(
                                ui.output_image(id='generate_',
                                                width='auto',
                                                height='auto'),
                                class_='card'
                            ),
                            icon=ui.img(src='-icon.png',
                                        height='18px',
                                        style='margin-bottom:2px; margin-right:3px'
                                        ),
                        ),
                        # endregion

                        # region ------------------------------------ MGP ----------------------------------
                        # This is the fourth pill card that converts
                        ui.nav(
                            '',
                            ui.row(
                                ui.column(4,
                                          ui.tags.div(ui.h6('Input Number'), style='text-align: center'),
                                          ui.input_text(
                                              id='mgp_in',
                                              width='100%',
                                              label='',
                                          )
                                ),
                                ui.column(2,
                                          ui.row(ui.panel_conditional('input.mgp_in == "" && output.mgp_out == null',
                                                               ui.tags.div(ui.h6('→'), style='text-align: center'),
                                                               ui.input_action_button(
                                                                   id='mgp_go_disabled',
                                                                   label='Convert',
                                                                   width='100%',
                                                                   class_='btn btn-outline-warning disabled'
                                                               )
                                          )),
                                          ui.panel_conditional('input.mgp_in != "" && output.mgp_out == null',
                                                               ui.tags.div(ui.h6('→'), style='text-align: center'),
                                                               ui.input_action_button(
                                                                   id='mgp_go',
                                                                   label='Convert',
                                                                   width='100%',
                                                                   class_='btn btn-warning'
                                                               )
                                          ),
                                          ui.panel_conditional('input.mgp_in != "" &&'
                                                               'output.mgp_out != "Error: No WF Found" &&'
                                                               'output.mgp_out != null',
                                                               ui.tags.div(ui.h6('→'), style='text-align: center'),
                                                               ui.input_action_button(
                                                                   id='mgp_go_success',
                                                                   label='Convert Again',
                                                                   width='100%',
                                                                   class_='btn btn-success'
                                                               )
                                          ),
                                          ui.panel_conditional('output.mgp_out == "Error: No WF Found"',
                                                               ui.tags.div(ui.h6('→'), style='text-align: center'),
                                                               ui.input_action_button(
                                                                   id='mgp_go_failed',
                                                                   label='Convert Again',
                                                                   width='100%',
                                                                   class_='btn btn-danger'
                                                               )
                                          )
                                ),
                                ui.column(4,
                                          ui.tags.div(ui.h6('Output WF Number'), style='text-align: center'),
                                          ui.output_text_verbatim(
                                              id='mgp_out',
                                              placeholder=True
                                          )
                                )
                            ),
                            ui.row(
                                ui.column(4,
                                          ui.tags.div(ui.h6('Input File of MGP Numbers'), style='text-align: center'),
                                          ui.input_file(id='mgp_in_file',
                                                        label='',
                                                        width='100%',
                                                        accept=['.xlsx', '.xls', '.csv']
                                          )
                                ),
                                ui.column(2,
                                          ui.tags.div(ui.h6('→'), style='text-align: center'),
                                          ui.panel_conditional('output.mgp_to_wf == null && '
                                                               'output.mgp_file_check == null',
                                                               ui.input_action_button(
                                                                   id='mgp_go_file',
                                                                   label='Convert',
                                                                   width='100%',
                                                                   class_='btn btn-warning'
                                                               )
                                          ),
                                          ui.panel_conditional('output.mgp_to_wf != null && '
                                                               'output.mgp_file_check == "File Uploaded!"',
                                                               ui.input_action_button(
                                                                   id='mgp_go_file_success',
                                                                   label='Convert Again',
                                                                   width='100%',
                                                                   class_='btn btn-success'
                                                               )
                                          ),
                                          ui.panel_conditional('output.mgp_to_wf == null && '
                                                               'output.mgp_file_check == "File Uploaded!"',
                                                               ui.input_action_button(
                                                                   id='mgp_go_file_failed',
                                                                   label='Convert Again',
                                                                   width='100%',
                                                                   class_='btn btn-danger'
                                                               )
                                          ),
                                          ui.tags.div(ui.output_text(id='mgp_file_check'), style='text-align: center')
                                ),
                                ui.column(4,
                                          ui.tags.div(ui.h6('Output File of WF Numbers'), style='text-align: center'),
                                          ui.panel_conditional('output.mgp_file_check != "File Uploaded!"',
                                                               ui.download_button(id='download_mgp_csv_disabled',
                                                                                  label='Download CSV',
                                                                                  width='100%',
                                                                                  icon=ui.img(src='download-icon.png',
                                                                                              height='18px',
                                                                                              style='margin-bottom:2px'),
                                                                                  class_='btn btn-outline-primary disabled'
                                                               )
                                          ),
                                          ui.panel_conditional('output.mgp_file_check == "File Uploaded!"',
                                                               ui.download_button(id='download_mgp_csv',
                                                                                  label='Download CSV',
                                                                                  width='100%',
                                                                                  icon=ui.img(src='download-icon.png',
                                                                                              height='18px',
                                                                                              style='margin-bottom:2px'),
                                                                                  class_='btn btn-primary'
                                                               )
                                          )
                                )
                            ),
                            ui.row(
                                ui.column(4, ui.tags.div(ui.output_ui(id='mgp_table'), class_='card')),
                                ui.column(8, ui.tags.div(ui.output_ui(id='mgp_to_'), class_='card'))
                            )
                        ),
                        # endregion

                        # region ------------------------------------ WIP ----------------------------------
                        # This is the fifth pill card
                        ui.nav(
                            'Empty',
                            'Empty Space For Future Development'
                        ),
                        # endregion

                        header=ui.tags.div(class_='card')
                    )
                )
            ),
        ),
        # endregion

        # region ---------------------------------- NO DB ----------------------------------
        ui.panel_conditional("input.navbar_id == 'EMPTY'",
            ui.layout_sidebar(ui.panel_sidebar('Sidebar'), ui.panel_main('Main'))
        ),
        # endregion

        title='Shiny Web-App'
    )  # password
    )  # page fluid
    return page
