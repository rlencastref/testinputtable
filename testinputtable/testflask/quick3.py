from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, FormField, FieldList, DecimalField, IntegerField,SubmitField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import datetime
#from testflask import db

app = Flask(__name__)
app.secret_key = 'SCRATCH'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db = SQLAlchemy(app)
db.app = app

## FORMS
class OneInputForm(FlaskForm):
    time = DecimalField('Time (min)',places=1,validators=[DataRequired()])
    input1 = DecimalField('AO1',places=1, validators=[DataRequired()])
    input2 = DecimalField('AO2',places=1, validators=[DataRequired()])
    input3 = DecimalField('AO3',places=1, validators=[DataRequired()])
    input4 = DecimalField('AO4',places=1, validators=[DataRequired()])
    input5 = DecimalField('AO5',places=1, validators=[DataRequired()])

class InputTableForm(FlaskForm):
    experimentname=StringField('Experiment Name',validators=[DataRequired(),Length(min=2,max=50)])
    inputs=FieldList(FormField(OneInputForm), min_entries=2,validators=[DataRequired()])
    load=SubmitField('Load Experiment')
    add=SubmitField('Add Row')
    submit=SubmitField('Save')
    
    def validate_experiment(self,experiment):
        exp=Input.query.filter_by(experiment=experiment.data).first()
        if exp:
            raise ValidationError('Experiment name already used. Please choose a different one.')
       
## MODELS
class Experiment(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50), unique=True, nullable=False)
    datecreated=db.Column(db.DateTime, nullable=False, default=datetime.utcnow)           
    status = db.Column(db.Boolean, nullable=False, default=False)
    # setup relationship to samples (one batch to many samples)
    inputs = db.relationship('Input',backref='inputexpname', lazy=True)
    
class Input(db.Model):
    time = db.Column(db.Numeric(3,2), primary_key=True, nullable=False)
    input1 = db.Column(db.Numeric(3,2), nullable=True)
    input2 = db.Column(db.Numeric(3,2), nullable=True)
    input3 = db.Column(db.Numeric(3,2), nullable=True)
    input4 = db.Column(db.Numeric(3,2), nullable=True)
    input5 = db.Column(db.Numeric(3,2), nullable=True)
    #setup relationship to Experiment table
    experiment = db.Column(db.String, db.ForeignKey('experiment.name'), nullable=False)
    
    def __repr__(self):
        return f"Input Table" 

## ROUTES
@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = InputTableForm()      
    if request.method == 'POST':
        if form.add.data:
            form.inputs.append_entry(FormField(OneInputForm()))  
            return render_template('home3.html', form=form)
        
        if form.submit.data:# and form.validate_on_submit():
            experiment = Experiment(name=form.experimentname.data)
            db.session.add(experiment)
            for entry in form.inputs:
                input = Input(time=entry.time.data, 
                              input1=entry.input1.data,
                              input2=entry.input2.data,
                              input3=entry.input3.data,
                              input4=entry.input4.data,
                              input5=entry.input5.data,
                              #relationships
                              inputexpname=Experiment.query.filter_by(name=form.experimentname.data).first())
                db.session.add(input)
            db.session.commit()
            flash('Input table has been saved', 'success')
            return render_template('home3.html', form=form)
    
    elif request.method == 'GET':
        return render_template('home3.html', form=form)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
