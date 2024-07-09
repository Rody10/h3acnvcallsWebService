# h3acnvcallsWebService

The h3acnvcallsWebService queries a database that stores structural variants in human genomes. The database has data about the variant's location (chromosome number, start and end), type of variant and number of times the variant was found in the data set.

This web service was created to allow for simple querying of the results obtained from the structural variant analyses.

The application uses Flask, sqlite3 and Jinja2.

## Installation

### Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- `pip` (Python package installer)
- `virtualenv` (optional, but recommended for creating a virtual environment)

### Step-by-Step Installation

1. **Clone the Repository**

2. **Create a Virtual Environment**

    python3 -m venv venv

3. **Activate the Virtual Environment**

    For macOS and Linux:
        source venv/bin/activate

    For Windows:
        venv\Scripts\activate

4. **Install Dependencies**

    ip install -r requirements.txt

5. **Set Environment Variables**

    For macOS and Linux:
        export FLASK_APP=app.py
        export FLASK_ENV=development

    For Windows:
        set FLASK_APP=app.py
        set FLASK_ENV=development

6. **Run the application**

    flask run



# Usage




