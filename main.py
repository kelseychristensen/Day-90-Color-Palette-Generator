from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
import colorgram
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename

class Form(FlaskForm):
    file = FileField(validators=[DataRequired()])
    num_colors = IntegerField(label="Number of Colors", validators=[DataRequired(), NumberRange(max=34)])
    submit = SubmitField()

def rgb2hex(r,g,b):
    return "#{:02x}{:02x}{:02x}".format(r,g,b)

def colors(photo, num_colors):
    colors = colorgram.extract(photo, num_colors)
    color_list = []
    for index in range(num_colors):
        color = colors[index]
        rgb = color.rgb
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        color_list.append(rgb2hex(red, green, blue))
    return color_list

app = Flask(__name__)
app.config['SECRET_KEY'] = "goi4924rvfadjfo94hbiodaajfda39u"
Bootstrap(app)

@app.route('/', methods=['GET', 'POST'])
def home():
    form = Form()
    if request.method == "POST":
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('static/uploads/' + filename)
        color_list = colors(f'static/uploads/{filename}', form.num_colors.data)
        return render_template('palette.html', list=color_list, number_colors=form.num_colors.data)
    return render_template("index.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
