from io import StringIO
import csv
from flask import make_response

def download(results, header_list):
    sio_instance = StringIO()
    csv_writer = csv.writer(sio_instance)
    csv_writer.writerow(header_list) # write column headings
    csv_writer.writerows(results)
    output = make_response(sio_instance.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=export.csv"
    output.headers["Content-type"] = "text/csv"
    return output
