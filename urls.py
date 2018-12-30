from flask import redirect, url_for, render_template, request
from rates_app import app
# from db_model import update_rates, XRate
import funcs


@app.route("/")
def home():
    return redirect(url_for("get_rates"))


@app.route("/rates/")
def get_rates():
    if request.args:  # Requested rate
        get_records = funcs.filter_r(request.args)  # Requested, barely readable records.
    else:
        get_records = funcs.get_r()  # All available, barely readable records.
    customize_it = funcs.create_tup(get_records)  # Readable and compact form to proceed for the next step.
    return render_template("template1.html", rates=customize_it)
