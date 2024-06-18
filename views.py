from flask import render_template, request, redirect, url_for, jsonify
import forms, db
from forms import QueryDellyCNVTableForm

def setup_routes(app):

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/query-delly-cnv-table", methods=["GET"])
    def query_delly_cnv_table():
        form = forms.QueryDellyCNVTableForm()
        return render_template("query-delly-cnv-table.html", form=form)
        
    @app.route("/query-delly-cnv-table-form-submit", methods=["GET"])
    def query_delly_cnv_table_form_submit():
        
        form = QueryDellyCNVTableForm(request.args)
        print("in route handler method")
        print(form.validate())
        if form.validate():
            chromosome = request.args["chromosome"]
            print("chromosome: ", chromosome)
            start_position = request.args["start_position"]
            end_position = request.args["end_position"]
            number_of_calls_with_0_copies = request.args["number_of_calls_with_0_copies"]
            number_of_calls_with_1_copy = request.args["number_of_calls_with_1_copy"]
            number_of_calls_with_2_copies = request.args["number_of_calls_with_2_copies"]
            number_of_calls_with_3_copies = request.args["number_of_calls_with_3_copies"]
            number_of_calls_with_4_copies = request.args["number_of_calls_with_4_copies"]
            number_of_calls_with_5_copies = request.args["number_of_calls_with_5_copies"]
            number_of_calls_with_6_copies = request.args["number_of_calls_with_6_copies"]
            number_of_calls_with_7_or_more_copies = request.args["number_of_calls_with_7_or_more_copies"]

            results = db.query_delly_cnv_table(
                                            chromosome,
                                            start_position,
                                            end_position,
                                            number_of_calls_with_0_copies,
                                            number_of_calls_with_1_copy,
                                            number_of_calls_with_2_copies,
                                            number_of_calls_with_3_copies,
                                            number_of_calls_with_4_copies,
                                            number_of_calls_with_5_copies,
                                            number_of_calls_with_6_copies,
                                            number_of_calls_with_7_or_more_copies)
            
            return render_template("query-delly-cnv-table-form-submit.html", results=results)

        


