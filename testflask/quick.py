from flask import Flask, render_template
from flask_wtf import Form
from wtforms import StringField, FormField, FieldList, HiddenField
import calendar

app = Flask(__name__)
app.secret_key = 'SCRATCH'

def dow_name(dow):
    return calendar.day_name[dow]

app.jinja_env.filters['dow'] = dow_name

class TimeForm(Form):
    opening = StringField('Opening Hour')
    closing = StringField('Closing Hour')
    day = HiddenField('Day')

class BusinessForm(Form):
    name = StringField('Business Name')
    hours = FieldList(FormField(TimeForm), min_entries=7, max_entries=7)


@app.route('/', methods=['post','get'])
def home():
    form = BusinessForm()
    if form.validate_on_submit():
        results = []
        for idx, data in enumerate(form.hours.data):
            results.append('{day}: [{open}]:[{close}]'.format(
                day=calendar.day_name[idx],
                open=data["opening"],
                close=data["closing"],
                )
            )
        return render_template('results.html', results=results)
    print(form.errors)
    return render_template('home.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)