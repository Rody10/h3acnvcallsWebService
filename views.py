from flask import render_template, request, redirect, url_for, jsonify
import forms

def setup_routes(app):

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/query-delly-cnv-table", methods=["GET"])
    def query_delly_cnv_table():
        form = forms.QueryDellyCNVTableForm()
        return render_template("query-delly-cnv-table.html", form=form)    


