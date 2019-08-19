from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, FormField, FieldList, HiddenField,DecimalField, IntegerField,SubmitField


app = Flask(__name__)
app.secret_key = 'SCRATCH'

class TimeInputForm(FlaskForm):
    time=IntegerField('Time (min)')
    input1 = StringField('AO1')
    input2 = StringField('AO2')
    input3 = StringField('AO2')
    input4 = StringField('AO2')
    input5 = StringField('AO2')
    submit=SubmitField('Submit')

@app.route('/', methods=['post','get'])
@app.route('/home', methods=['post','get'])
def home():
    form = TimeInputForm()      
    if form.validate_on_submit():
        pass
    return render_template('home2.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)