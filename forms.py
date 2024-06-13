from wtforms import Form, StringField, IntegerField, SelectField, validators

class QueryDellyCNVTableForm(Form):
    chromosome = SelectField(
        label="Chromosome",
        choices=[None,"chr1","chr2","chr3","chr4","chr5","chr6","chr7","chr8","chr9","chr10","chr11","chr12","chr13","chr14","chr15","chr16","chr17","chr18","chr19","chr20","chr21","chr22","chrX"],                    
        default=None
        )
    start_position = IntegerField(
        label="Start position",
        default=None
        ) 
    end_position = IntegerField(
        label="End position",
        default=None
        )
    number_of_calls_with_0_copies = IntegerField(
        label="Number of calls with 0 copies",
        default=None
        ) # cn0
    number_of_calls_with_1_copy = IntegerField(
        label="Number of calls with 1 copy",
        default=None
        )
    number_of_calls_with_2_copies = IntegerField(
        label="Number of calls with 2 copies",
        default=None
        )
    number_of_calls_with_3_copies = IntegerField(
        label="Number of calls with 3 copies",
        default=None
        )
    number_of_calls_with_4_copies = IntegerField(
        label="Number of calls with 4 copies",
        default=None
        )
    number_of_calls_with_5_copies = IntegerField(
        label="Number of calls with 5 copies",
        default=None)
    number_of_calls_with_6_copies = IntegerField(
        label="Number of calls with 6 copies",
        default=None
        )
    number_of_calls_with_7_or_more_copies = IntegerField(
        label="Number of calls with 7 or more copies",
        default=None
        )

