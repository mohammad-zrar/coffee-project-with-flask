from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label="Cafe Location on Google Maps (URL)", validators=[DataRequired(), URL()])
    open = StringField(label="Opening Time e.g. 8AM", validators=[DataRequired()])
    close = StringField(label="Closing Time e.g. 5:30PM")
    coffee = SelectField(label="Coffee Rating", choices=["☕️" * 1, "☕️" * 2, "☕️" * 3, "☕️" * 4, "☕️" * 5],
                         validators=[DataRequired()])
    wifi = SelectField(label="WiFi Strength Rating", choices=["✘", "💪" * 1, "💪" * 2, "💪" * 3, "💪" * 4, "💪" * 5],
                       validators=[DataRequired()] )
    power = SelectField(label="Power Socket Availability", choices=["✘", "🔌" * 1, "🔌" * 2, "🔌" * 3, "🔌" * 4, "🔌" * 5],
                        validators=[DataRequired()])
    submit = SubmitField('Submit')


# Exercise:
# add: Location URL, open time, closing time, coffee rating, Wi-Fi rating, power outlet rating fields
# make coffee/Wi-Fi/power a select element with choice of 0 to 5.
# e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        form_data = [form.cafe.data, form.location.data, form.open.data, form.close.data,
                     form.coffee.data, form.wifi.data, form.power.data]
        form_data = ",".join(form_data)  # Converting list to string
        with open("cafe-data.csv", "a", newline='', encoding="utf8") as f:
            f.write("\n"+form_data)
        return redirect(url_for('add_cafe'))
    return render_template("add.html", form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding="utf8") as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)

    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
