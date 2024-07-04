from wtforms import Form, StringField, IntegerField, SelectField, validators

class QueryDellyCNVTableForm(Form):
    chromosome = SelectField(
        label="Chromosome",
        choices=["any","chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX"],                    
        default="any",
        validators=[validators.Optional()]
        )
    start_position = IntegerField(
        label="Start position",
        default=11626, # lowest value for the column
        validators=[validators.Optional()]
        ) 
    end_position = IntegerField(
        label="End position",
        default=248945995, # highest value for the column
        validators=[validators.Optional()]
        )

class QueryVariantsTableForm(Form):
    chromosome = SelectField(
        label="Chromosome",
        choices=["any","chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX"],                    
        default="any",
        validators=[validators.Optional()]
        )
    start_position = IntegerField(
        label="Start position",
        default=1, # lowest value for the column
        validators=[validators.Optional()]
        ) 
    end_position = IntegerField(
        label="End position",
        default=248946070, # highest value for the column -> SELECT MAX(end) FROM variants WHERE typeof(end) = 'integer' - issue with end column
        validators=[validators.Optional()]
        )
    type = SelectField(
        label="Type",
        choices=["any","BND","INS","DEL","DUP","INV","CTX"],                    
        default="any",
        validators=[validators.Optional()]
        )
    classifier = SelectField(
        label="Classifier",
        choices=["any","delly","gridss","manta", "smoove"],                    
        default="any",
        validators=[validators.Optional()]
        )
    
class QueryBothTablesForm(Form):
    query_both_tables_chromosome = SelectField(
        label="Chromosome",
        choices=["any","chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX"],                    
        default="any",
        validators=[validators.Optional()]
        )
    delly_cnv_start_position = IntegerField(
        label="Start position",
        default=11626, # lowest value for the column
        validators=[validators.Optional()]
        ) 
    delly_cnv_end_position = IntegerField(
        label="End position",
        default=248945995, # highest value for the column
        validators=[validators.Optional()]
        )
    variants_start_position = IntegerField(
        label="Start position",
        default=1, # lowest value for the column
        validators=[validators.Optional()]
        ) 
    variants_end_position = IntegerField(
        label="End position",
        default=248946070, # highest value for the column -> SELECT MAX(end) FROM variants WHERE typeof(end) = 'integer' - issue with end column
        validators=[validators.Optional()]
        )
    variants_type = SelectField(
        label="Type",
        choices=["any","BND","INS","DEL","DUP","INV","CTX"],                    
        default="any",
        validators=[validators.Optional()]
        )
    variants_classifier = SelectField(
        label="Classifier",
        choices=["any","delly","gridss","manta", "smoove"],                    
        default="any",
        validators=[validators.Optional()]
        )



