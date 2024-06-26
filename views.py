from flask import render_template, request, redirect, url_for, jsonify
import forms, db, download
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
        if form.validate():
            chromosome = request.args["chromosome"]
            start_position = request.args["start_position"]
            end_position = request.args["end_position"]
            if (chromosome == "any"):
                chromosome = "%"
            if (start_position == ""):
               start_position = "11626" # lowest value for the column
            if (end_position == ""):
               end_position = "248945995" # highest value for the column
            
            page = int(request.args.get("page", 1))
            page_size = 10 # number of rows to display on each page

            total_records = db.get_total_records(
                chromosome,
                start_position,
                end_position    
            )

            results = db.query_delly_cnv_table_paginated(
                chromosome,
                start_position,
                end_position,
                page,
                page_size
            )

            total_pages = (total_records + page_size - 1) // page_size
            
            return render_template("query-delly-cnv-table-form-submit.html", form=form, results=results, page=page, total_pages=total_pages)
        else:
            return render_template("query-delly-cnv-table.html", form=form) # if validation fails return the page

    # TO be completed 
    @app.route("/download-delly-cnv-query-results", methods=["GET"])
    def download_delly_cnv_query_results():
        form = QueryDellyCNVTableForm(request.args)
        # i am not getting parameters here, fix it
        print("in route handler method")
        print("checking form", form.validate())
        print(request)
        if form.validate():
            chromosome = request.args["chromosome"]
            print("Start of validation", chromosome)
            start_position = request.args["start_position"]
            end_position = request.args["end_position"]
            if (chromosome == "any"):
                chromosome = "%"
            if (start_position == ""):
               start_position = "11626" # lowest value for the column
            if (end_position == ""):
               end_position = "248945995" # highest value for the column
                       
            print("finished validation")
            results = db.query_delly_cnv_table_not_paginated(
                chromosome,
                start_position,
                end_position,
            )
            

            return download.download(results, [
                            "Chromosome",
                            "Start Position",
                            "End Position",
                            "CN0",
                            "CN1",
                            "CN2",
                            "CN3",
                            "CN4",
                            "CN5",
                            "CN6",
                            "CN7plus"])
        else:
            return render_template("query-delly-cnv-table.html", form=form)


