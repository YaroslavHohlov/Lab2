from flask import Flask, render_template
from flask import request
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from io import BytesIO
import base64

app= Flask(__name__)

def get_data(region_index, row, week_interval=[1, 52]):

    files = os.listdir(os.path.join(os.getcwd(), "Datas"))

    region_path = str(region_index) + '.csv'

    dataframe = pd.read_csv(os.path.join(os.getcwd(), "Datas", region_path), names=['year', 'week', 'NDVI', 'BT', 'VCI', 'TCI', 'VHI'])

    df = dataframe.loc[:, ['year', 'week', row]]

    # TODO: create plot function
    file_path = create_plot(df, row, region_index)

    data = []

    for d in df.iterrows():
        # if d[1]['week'] >= week_interval[0] and d[1]['week'] <= week_interval[1]:
        #     data.append([d[1]['year'], d[1]['week'], d[1][row]])
        # else len(week_interval) == 2 :
        #     data.append([d[1]['year'], d[1]['week'], d[1][row]])
        if len(week_interval) == 2:
           if d[1]['week'] >= week_interval[0] and d[1]['week'] <= week_interval[1]:
               data.append([d[1]['year'], d[1]['week'], d[1][row]])
        elif len(week_interval) == 1:
            if d[1]['week'] >= week_interval[0]:
                data.append([d[1]['year'], d[1]['week'], d[1][row]])
    return data, file_path

@app.route('/', methods=['GET', 'POST'])
def web():
    # print(request.form['region'])
    if request.method == 'POST':

        week_interval = None if request.form['week_interval'] == '' else list(
            map(int, request.form['week_interval'].split('-')))
        print(week_interval)
        df, file_path = get_data(
                request.form['region'],
                request.form['time_row'],
                week_interval
            )

        return render_template('template.html',
            title=request.form['region'],
            row=request.form['time_row'],
            data=df,
            img=file_path
            )
    else:
        return render_template('template.html')

def create_plot(data, row, region):
    x_label = []
    for d in data.iterrows():
        x_label.append((d[1]['year'] - 1982) * 52 + d[1]['week'])
    plt.close()
    plt.plot(x_label, data[row], label=row)
    plt.xlabel('year')
    plt.ylabel(row)
    io_file = BytesIO()
    plt.savefig(io_file, format='png', dpi=100)
    base64_string = base64.b64encode(io_file.getvalue()).decode()
    return base64_string

if __name__ == '__main__':
    app.run(debug=True)
