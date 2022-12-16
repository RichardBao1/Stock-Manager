from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length

class Stock_Form(FlaskForm):
    Stock = StringField("Stock", validators=[InputRequired(),Length(min=1)], id="autocomplete")
    submit = SubmitField("OK")

class Buy_Sell_Stock(FlaskForm):
    number_of_stocks = IntegerField('No. of Stocks', validators=[])
    buy_sell_choices = ['Buy', 'Sell']
    buy_sell = SelectField('Buy or Sell', choices=buy_sell_choices, default = buy_sell_choices[0])
    stock = StringField("Stock", validators=[InputRequired(),Length(min=1)], id="autocomplete")
    submit = SubmitField("OK")


