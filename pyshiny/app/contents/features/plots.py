"""
Takes in the queried database based on user inputted filters and plots that table in multiple graphs

Author: Jesse Liu
"""

import plotly.express as px
import plotly.graph_objects as go
from contents.utils.utils import choices
from datetime import datetime
import pandas as pd
import os


class Plots:

    def __init__(self, db):
        self.id = 'id'
        self.db = db

    # This function structures the db with the categorical choice
    @staticmethod
    def prep_choices(db, choice):
        category = choices()[choice]
        if not category:
            return db
        else:
            try:
                category.remove('')
            except ValueError:
                pass
            category = reversed(category)
            pattern = '|'.join(category)
            db[choice] = db[choice].str.extract('({})'.format(pattern))
        return db

    # Create a bar plot for numeric and/or categorical distribution
    def bar_plot_db(self, bar_choice_range, bar_choice_category):
        cols = list({self.id, bar_choice_range, bar_choice_category} and set(self.db.columns))
        bar_db = self.db[cols]
        bar_db[bar_choice_range] = round(bar_db[bar_choice_range], 1)
        bar_db = self.prep_choices(bar_db, bar_choice_category)
        if bar_choice_category == '':
            bar_db = bar_db.groupby([bar_choice_range]).count().reset_index()[[bar_choice_range, self.id]]
        else:
            bar_db = bar_db.dropna(subset=[bar_choice_category])
            bar_db = bar_db.groupby([bar_choice_range, bar_choice_category])
            bar_db = bar_db.count().reset_index()[[bar_choice_range, bar_choice_category, self.id]]
        bar_db = bar_db.rename(columns={self.id: 'Volume'})
        return bar_db

    def bar_plot(self, bar_choice_range, bar_choice_category):
        bar_db = self.bar_plot_db(bar_choice_range, bar_choice_category)
        if bar_choice_category == '':
            fig = px.bar(bar_db, x=bar_choice_range, y='Volume',
                         title='Distribution Plot for {}'.format(bar_choice_range),
                         text_auto=True
                         )
        else:
            fig = px.bar(bar_db, x=bar_choice_range, y='Volume',
                         color=bar_choice_category,
                         title='Distribution Plot for {} by {}'.format(bar_choice_range, bar_choice_category),
                         text_auto=True
                         )
        fig.write_image(os.path.join(os.path.dirname(__file__), '../utils/tmp/temp_png.png'),
                        width=1220*1.5,
                        height=450*1.5)
        return go.FigureWidget(fig)

    # Create a pie chart for categorical distribution
    def pie_chart(self, pie_choice, date):
        pie_db = self.db[[self.id, pie_choice]]
        pie_db = self.prep_choices(pie_db, pie_choice)
        pie_db = pie_db.groupby([pie_choice]).count().reset_index()[[pie_choice, 'id']]
        pie_db[pie_choice] = [i + ' ({})'.format(str(j)) for i, j in zip(pie_db[pie_choice], pie_db['id'])]
        date_0 = datetime.strptime(str(date[0]), "%Y-%m-%d").strftime("%b-%Y").strip()
        date_1 = datetime.strptime(str(date[1]), "%Y-%m-%d").strftime("%b-%Y").strip()
        if date_0 != date_1:
            dates = '{} to {}'.format(date_0, date_1)
        else:
            dates = date_0
        fig = px.pie(pie_db, values=self.id, names=pie_choice,
                     labels={
                         self.id: 'Volume',
                     },
                     title='{}{} from {}'.format(pie_choice, dates)
                     )
        return go.FigureWidget(fig)

    # Shows the time taken for the reports to be generated since accessioning
    def turn_around_time_db(self, from_, to_):
        time_db = self.db[[self.id, to_, from_]]
        time_db[[to_, from_]] = time_db[[to_, from_]].apply(
            pd.to_datetime, errors='coerce', infer_datetime_format=True)
        time_db = time_db.dropna(subset=[to_, from_])
        time_db['Days'] = (time_db[to_] - time_db[from_]).dt.days
        # return time_db
        over_30_days = time_db[time_db['Days'] >= 30].count()['Days']
        time_db = time_db[time_db['Days'] < 30].sort_values(self.id)
        time_db = time_db.groupby(['Days']).count().reset_index()[['Days', self.id]]
        time_db.loc[len(time_db.index)] = [30, over_30_days]
        time_db = time_db.rename(columns={self.id: 'Volume'})
        return time_db


    # Create a time graph for the categorical distribution in percentages
    def time_graph(self, date_type, time_choice):
        date_type = date_type.replace(' ', '_')
        time_db = self.db[[date_type, time_choice]]
        time_db = self.prep_choices(time_db, time_choice)
        time_db[date_type] = pd.to_datetime(time_db[date_type],
                                                     errors='coerce', infer_datetime_format=True)
        time_db[date_type] = time_db[date_type].dt.strftime('%Y-%m')
        fig = px.histogram(time_db, x=date_type, color=time_choice, barnorm="percent",
                           labels={
                               "count (normalized as percent)": 'Percent',
                           },
                           title='Time Graph for {}'.format(time_choice),
                           text_auto=True
                           )
        return go.FigureWidget(fig)




    # other plot functions here