from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, FormField, FieldList, DecimalField, IntegerField,SubmitField
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Length, ValidationError
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
    experiment=StringField('Experiment Name',validators=[DataRequired(),Length(min=2,max=50)])
    inputs=FieldList(FormField(OneInputForm), min_entries=2,validators=[DataRequired()])
    add=SubmitField('Add Row')
    submit=SubmitField('Submit')
    def validate_experiment(self,experiment):
        exp=InputTable.query.filter_by(experiment=experiment.data).first()
        if exp:
            raise ValidationError('Experiment name already used. Please choose a different one.')
    
    
## MODELS
class InputTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    experiment=db.Column(db.String(50),unique=True,nullable=False)
    time = db.Column(db.Numeric(3,2), nullable=False)
    input1 = db.Column(db.Numeric(3,2), nullable=True)
    input2 = db.Column(db.Numeric(3,2), nullable=True)
    input3 = db.Column(db.Numeric(3,2), nullable=True)
    input4 = db.Column(db.Numeric(3,2), nullable=True)
    input5 = db.Column(db.Numeric(3,2), nullable=True)
    
    def __repr__(self):
        return f"Input Table" 

## ROUTES
@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = InputTableForm()      
    if request.method == 'POST':
        print('post')
 
        if form.add.data:
            form.inputs.append_entry(FormField(OneInputForm()))  
            return render_template('home3.html', form=form)
        
        if form.submit.data:# and form.validate_on_submit():
            
            db.session.commit()
            return render_template('home3.html', form=form)
    
    elif request.method == 'GET':
        print('get')
        return render_template('home3.html', form=form)



if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
