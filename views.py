from flask import render_template, request, redirect, url_for, jsonify
import forms, db, download
from forms import QueryDellyCNVTableForm, QueryVariantsTableForm, QueryBothTablesForm

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

            total_records = db.get_total_records_delly_cnv_query(
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

    @app.route("/download-delly-cnv-query-results", methods=["GET"])
    def download_delly_cnv_query_results():
        form = QueryDellyCNVTableForm(request.args)
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


    @app.route("/query-variants-table", methods=["GET"])
    def query_variants_table():
        form = forms.QueryVariantsTableForm()
        return render_template("query-variants-table.html", form=form)

    @app.route("/query-variants-table-form-submit", methods=["GET"])
    def query_variants_table_form_submit():
        
        form = QueryVariantsTableForm(request.args)
        if form.validate():
            chromosome = request.args["chromosome"]
            start_position = request.args["start_position"]
            end_position = request.args["end_position"]
            type = request.args["type"]
            classifier = request.args["classifier"]
            if (chromosome == "any"):
                chromosome = "%"
            if (start_position == ""):
                start_position = "1" # lowest value for the column
            if (end_position == ""):
                end_position = "248946070" # highest value for the column
            if (type == "any"):
                type = "%"
            if (classifier == "any"):
                classifier = "%"
            
            page = int(request.args.get("page", 1))
            page_size = 10 # number of rows to display on each page

            total_records = db.get_total_records_variants_query(
                chromosome,
                start_position,
                end_position,
                type,
                classifier    
            )

            results = db.query_variants_table_paginated(
                chromosome,
                start_position,
                end_position,
                type,
                classifier,
                page,
                page_size
            )

            total_pages = (total_records + page_size - 1) // page_size
            
            return render_template("query-variants-table-form-submit.html", form=form, results=results, page=page, total_pages=total_pages)
        else:
            return render_template("query-variants-table.html", form=form) # if validation fails return the page
        
        
    @app.route("/download-variants-query-results", methods=["GET"])
    def download_variants_query_results():
        form = QueryVariantsTableForm(request.args)
        if form.validate():
            chromosome = request.args["chromosome"]
            start_position = request.args["start_position"]
            end_position = request.args["end_position"]
            type = request.args["type"]
            classifier = request.args["classifier"]
            if (chromosome == "any"):
                chromosome = "%"
            if (start_position == ""):
               start_position = "1" # lowest value for the column
            if (end_position == ""):
               end_position = "248946070" # highest value for the column
            if (type == "any"):
                type = "%"
            if (classifier == "any"):
                classifier = "%"
            
            results = db.query_variants_table_not_paginated(
                chromosome,
                start_position,
                end_position,
                type,
                classifier
            )            
            return download.download(results, [
                            "Chromosome",
                            "Start Position",
                            "End Position",
                            "Type",
                            "AC",
                            "AH",
                            "Classifier"])
        else:
            return render_template("query-variants-table.html", form=form)

    @app.route("/query-both-tables", methods=["GET"])
    def query_both_tables():
        form = QueryBothTablesForm()
        return render_template("query-both-tables.html", form=form)
    
    @app.route("/query-both-tables-form-submit", methods=["GET"])
    def query_both_tables_form_submit():
        
        form = QueryBothTablesForm(request.args)
        if form.validate():
            query_both_tables_chromosome = request.args["query_both_tables_chromosome"]
            delly_cnv_start_position = request.args["delly_cnv_start_position"]
            delly_cnv_end_position = request.args["delly_cnv_end_position"]
            variants_start_position = request.args["variants_start_position"]
            variants_end_position = request.args["variants_end_position"]
            variants_type = request.args["variants_type"]
            variants_classifier = request.args["variants_classifier"]
            if (query_both_tables_chromosome == "any"):
                query_both_tables_chromosome = "%"
            if (delly_cnv_start_position == ""):
               delly_cnv_start_position = "11626" # lowest value for the column
            if (delly_cnv_end_position == ""):
               delly_cnv_end_position = "248945995" # highest value for the column
            if (variants_start_position == ""):
                variants_start_position = "1" # lowest value for the column
            if (variants_end_position == ""):
                variants_end_position = "248946070" # highest value for the column
            if (variants_type == "any"):
                variants_type = "%"
            if (variants_classifier == "any"):
                variants_classifier = "%"

            # temp for debugging
            #query_both_tables_chromosome = "chr1"
            #delly_cnv_start_position = "11626"
            #delly_cnv_end_position = "248945995"
            #variants_start_position = "11626"
            #variants_end_position = "248945995"
            #variants_type = "DEL"
            #
            
            
            page = int(request.args.get("page", 1))
            page_size = 10 # number of rows to display on each page - make this GLOBAL?
    
         

            total_records = db.get_total_records_both_tables_query(
                query_both_tables_chromosome,
                delly_cnv_start_position,
                delly_cnv_end_position,
                variants_start_position,
                variants_end_position,
                variants_type,
                variants_classifier  
            )

            results = db. query_both_tables_paginated(
                query_both_tables_chromosome,
                delly_cnv_start_position,
                delly_cnv_end_position,
                variants_start_position,
                variants_end_position,
                variants_type,
                variants_classifier,  
                page,
                page_size   
            )


            total_pages = (total_records + page_size - 1) // page_size
            
            return render_template("query-both-tables-form-submit.html", form=form, results=results, page=page, total_pages=total_pages)
        else:
            return render_template("query-both-tables.html", form=form) # if validation fails return the page
    
    @app.route("/download_both_tables_query_results", methods=["GET"])
    def download_both_tables_query_results():
        form = QueryBothTablesForm(request.args)
        if form.validate():
            query_both_tables_chromosome = request.args["query_both_tables_chromosome"]
            delly_cnv_start_position = request.args["delly_cnv_start_position"]
            delly_cnv_end_position = request.args["delly_cnv_end_position"]
            variants_start_position = request.args["variants_start_position"]
            variants_end_position = request.args["variants_end_position"]
            variants_type = request.args["variants_type"]
            variants_classifier = request.args["variants_classifier"]
            if (query_both_tables_chromosome == "any"):
                query_both_tables_chromosome = "%"
            if (delly_cnv_start_position == ""):
               delly_cnv_start_position = "11626" # lowest value for the column
            if (delly_cnv_end_position == ""):
               delly_cnv_end_position = "248945995" # highest value for the column
            if (variants_start_position == ""):
                variants_start_position = "1" # lowest value for the column
            if (variants_end_position == ""):
                variants_end_position = "248946070" # highest value for the column
            if (variants_type == "any"):
                variants_type = "%"
            if (variants_classifier == "any"):
                variants_classifier = "%"
            
            results = db. query_both_tables_not_paginated(
                query_both_tables_chromosome,
                delly_cnv_start_position,
                delly_cnv_end_position,
                variants_start_position,
                variants_end_position,
                variants_type,
                variants_classifier     
            )     
            return download.download(results, [
                            "Chromosome",
                            "Delly_CNV Start Position",
                            "Delly_CNV End Position",
                            "CN0",
                            "CN1",
                            "CN2",
                            "CN3",
                            "CN4",
                            "CN5",
                            "CN6",
                            "CN7PLUS",
                            "Variants Start Position",
                            "Variants End Position",
                            "Type",
                            "AC",
                            "AH",
                            "Classifier"])
        else:
            return render_template("query-variants-table.html", form=form)