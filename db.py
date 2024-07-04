import sqlite3, os, csv

def import_tsv(file_path, table_name, cursor):
        with open(file_path, "r") as file:
                reader = csv.reader(file, delimiter="\t")
                columns = next(reader) # Skip the header row

                quoted_columns = [f'"{col}"' for col in columns]

                query = f"INSERT INTO {table_name} ({', '.join(quoted_columns)}) VALUES ({', '.join(['?'] * len(columns))})"
                for data in reader:
                    cursor.execute(query, data)

def create_database():
    database_exists = os.path.exists("database.db")
    # connect to the database. If the database does not exist the command then creates the database.
    conn = sqlite3.connect("database.db")
    # if the database did not exist, create the tables
    if not database_exists:
        cursor = conn.cursor()
        # delly_cnv table focuses specifically on CNVs detected by delly in CNV mode.
        cursor.execute('''CREATE TABLE delly_cnv (
                        chrom TEXT,
                        start INTEGER,
                        end INTEGER, 
                        cn0 INTEGER, 
                        cn1 INTEGER, 
                        cn2 INTEGER, 
                        cn3 INTEGER, 
                        cn4 INTEGER, 
                        cn5 INTEGER, 
                        cn6 INTEGER, 
                        cn7plus INTEGER
                        )''')
        # variants table combines data from multiple tools (manta, delly, smoove and gridss) to provide
        # a comprehensive list of various types of structural variants.
        cursor.execute('''CREATE TABLE variants (
                        chrom TEXT, 
                        start INTEGER, 
                        end INTEGER, 
                        type TEXT, 
                        ac INTEGER, 
                        ah TEXT, 
                        classifier TEXT
                        )''')

        # import data from TSV files
        import_tsv("tsv_files/manta.tsv","variants",cursor)
        import_tsv("tsv_files/delly.tsv","variants",cursor)
        import_tsv("tsv_files/smoove.tsv","variants",cursor)
        import_tsv("tsv_files/gridss.tsv","variants",cursor)
        import_tsv("tsv_files/delly_cnv.tsv","delly_cnv",cursor)

        # create indexes, helps speed up searches
        cursor.execute('CREATE INDEX dcnv_end ON delly_cnv(chrom, end)')
        cursor.execute('CREATE INDEX dcnv_start ON delly_cnv(chrom, start)')
        cursor.execute('CREATE INDEX classifier_ind ON variants(classifier)')
        cursor.execute('CREATE INDEX start_class_ind ON variants(chrom, start, classifier)')
        cursor.execute('CREATE INDEX end_class_ind ON variants(chrom, end, classifier)')
        cursor.execute('CREATE INDEX start_end_class_ind ON variants(chrom, start, end, classifier)')

        conn.commit()
        cursor.close()
        conn.close() 

def get_database():
      conn = sqlite3.connect("database.db")
      conn.row_factory = sqlite3.Row
      return conn

# delete?
def query_delly_cnv_table(           
            chromosome,
            start_position,
            end_position):
        
        conn = get_database()
        cursor = conn.cursor()

           
        query = '''
            SELECT * FROM delly_cnv 
            WHERE chrom LIKE ?
            AND (start > ?)
            AND (end < ?)
            LIMIT 5
            '''
        cursor.execute(query, (
                    chromosome,
                    start_position,
                    end_position,        
               ))

        results = cursor.fetchall()
        conn.close
        return results


def get_total_records_delly_cnv_query(chromosome, start_position, end_position):
    conn = get_database()
    cursor = conn.cursor()
    
    query = '''
        SELECT COUNT (*) FROM delly_cnv 
            WHERE chrom LIKE ?
            AND (start > ?)
            AND (end < ?)
        '''
    cursor.execute(query, (
        chromosome,
        start_position,
        end_position    
    ))
    total_records = cursor.fetchone()[0]
    conn.close()
    
    return total_records

def query_delly_cnv_table_paginated(chromosome, start_position, end_position, page, page_size):
    offset = (page - 1) * page_size
    
    query = '''
        SELECT * FROM delly_cnv 
            WHERE chrom LIKE ?
            AND (start > ?)
            AND (end < ?)
            LIMIT ?
            OFFSET ?
        '''
    conn = get_database()
    cursor = conn.cursor()
    cursor.execute(query, (
        chromosome,
        start_position,
        end_position,
        page_size,
        offset
    ))
    results = cursor.fetchall()
    conn.close()
    
    return results

def query_delly_cnv_table_not_paginated(chromosome, start_position, end_position):
    
    query = '''
        SELECT * FROM delly_cnv 
            WHERE chrom LIKE ?
            AND (start > ?)
            AND (end < ?)
        '''
    conn = get_database()
    cursor = conn.cursor()
    cursor.execute(query, (
        chromosome,
        start_position,
        end_position,
    ))
    results = cursor.fetchall()
    conn.close()
    
    return results

def get_total_records_variants_query(chromosome, start_position, end_position, type, classifier):
    conn = get_database()
    cursor = conn.cursor()
    
    query = '''
        SELECT COUNT (*) FROM variants 
            WHERE chrom LIKE ?
            AND (start > ?)
            AND (end < ?)
            AND type LIKE ?
            AND classifier LIKE ?
        '''
    cursor.execute(query, (
        chromosome,
        start_position,
        end_position,
        type,
        classifier  
    ))
    total_records = cursor.fetchone()[0]
    conn.close()
    
    return total_records

def query_variants_table_paginated(chromosome, start_position, end_position, type, classifier, page, page_size):
    print("in query_variants_table_paginated")
    offset = (page - 1) * page_size
    
    query = '''
        SELECT * FROM variants 
            WHERE chrom LIKE ?
            AND (start > ?)
            AND (end < ?)
            AND type LIKE ?
            AND classifier LIKE ?
            LIMIT ?
            OFFSET ?
        '''
    conn = get_database()
    cursor = conn.cursor()
    cursor.execute(query, (
        chromosome,
        start_position,
        end_position,
        type,
        classifier,
        page_size,
        offset
    ))
    results = cursor.fetchall()
    conn.close()
    
    return results

def query_variants_table_not_paginated(chromosome, start_position, end_position, type, classifier):
    
    query = '''
        SELECT * FROM variants
            WHERE chrom LIKE ?
            AND (start > ?)
            AND (end < ?)
            AND type LIKE ?
            AND classifier LIKE ?
        '''
    conn = get_database()
    cursor = conn.cursor()
    cursor.execute(query, (
        chromosome,
        start_position,
        end_position,
        type,
        classifier
    ))
    results = cursor.fetchall()
    conn.close()
    
    return results


def get_total_records_both_tables_query(chromosome, delly_cnv_start_position, delly_cnv_end_position, variants_start_position, variants_end_position, variants_type, variants_classifier):
    conn = get_database()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            COUNT(*) AS matching_rows
        FROM 
            variants v
        JOIN 
            delly_cnv d ON v.chrom = d.chrom
                        AND v.start < d.end
                        AND v.end > d.start
        WHERE
            v.type LIKE ?
            AND v.classifier LIKE ?
            AND v.chrom LIKE ?
            AND v.start > ?
            AND v.end < ?
            AND d.start > ?
            AND d.end < ?         
        '''
    cursor.execute(query, (
        variants_type,
        variants_classifier,
        chromosome,
        variants_start_position,
        variants_end_position,
        delly_cnv_start_position,
        delly_cnv_end_position
    ))
    total_records = cursor.fetchone()[0]
    conn.close()
    return total_records

def query_both_tables_paginated(chromosome, delly_cnv_start_position, delly_cnv_end_position, variants_start_position, variants_end_position, variants_type, variants_classifier,  page, page_size):
    offset = (page - 1) * page_size
    query = '''
        SELECT 
            v.chrom AS v_chrom, 
            v.start AS v_start, 
            v.end AS v_end, 
            v.type, 
            v.ac, 
            v.ah, 
            v.classifier,
            d.chrom AS d_chrom, 
            d.start AS d_start, 
            d.end AS d_end, 
            d.cn0, 
            d.cn1, 
            d.cn2, 
            d.cn3, 
            d.cn4, 
            d.cn5, 
            d.cn6, 
            d.cn7plus
        FROM 
            variants v
        JOIN 
            delly_cnv d ON v.chrom = d.chrom
                        AND v.start < d.end
                        AND v.end > d.start
        WHERE
            v.type LIKE ?
            AND v.classifier LIKE ?
            AND v.chrom LIKE ?
            AND v.start > ?
            AND v.end < ?
            AND d.start > ?
            AND d.end < ?
        LIMIT ?
        OFFSET ?          
        '''
    conn = get_database()
    cursor = conn.cursor()

    cursor.execute(query, (
        variants_type,
        variants_classifier,
        chromosome,
        variants_start_position,
        variants_end_position,
        delly_cnv_start_position,
        delly_cnv_end_position,
        page_size,
        offset
    ))

    results = cursor.fetchall()
    conn.close()
    print(results)
    return results

def query_both_tables_not_paginated(chromosome, delly_cnv_start_position, delly_cnv_end_position, variants_start_position, variants_end_position, variants_type, variants_classifier):
    query = '''
        SELECT 
            v.chrom AS v_chrom, 
            v.start AS v_start, 
            v.end AS v_end, 
            v.type, 
            v.ac, 
            v.ah, 
            v.classifier,
            d.chrom AS d_chrom, 
            d.start AS d_start, 
            d.end AS d_end, 
            d.cn0, 
            d.cn1, 
            d.cn2, 
            d.cn3, 
            d.cn4, 
            d.cn5, 
            d.cn6, 
            d.cn7plus
        FROM 
            variants v
        JOIN 
            delly_cnv d ON v.chrom = d.chrom
                        AND v.start < d.end
                        AND v.end > d.start
        WHERE
            v.type LIKE ?
            AND v.classifier LIKE ?
            AND v.chrom LIKE ?
            AND v.start > ?
            AND v.end < ?
            AND d.start > ?
            AND d.end < ?   
        LIMIT 10000     
        '''
    conn = get_database()
    cursor = conn.cursor()

    cursor.execute(query, (
        variants_type,
        variants_classifier,
        chromosome,
        variants_start_position,
        variants_end_position,
        delly_cnv_start_position,
        delly_cnv_end_position,
    ))
    results = cursor.fetchall()
    conn.close()
    return results