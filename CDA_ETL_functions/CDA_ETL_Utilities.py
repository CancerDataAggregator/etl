"""
This file is meant to define functions that CDA needs to implement on top of those defined 
in previous files from the ISB-CGC ETL process located here: https://github.com/isb-cgc/NextGenETL
"""
def exclude_nested_fields(cases,exfields):
    """This function receives 1 case level dictionary directly from GDC API output, as well as
    a dictionary of dictionaries for the fields to be excluded from the data recieved from GDC.
    It recursively searches through the nesting layers to remove unwanted fields from the data. 
    This can be potentially modified to also transform data directly from the GDC API
    """
    casecopy=cases.copy()
    for field in cases.keys():
        for exfield in exfields.keys():
            if exfield == field:
                #Check if end of excluded fields
                end_of_excluded_field =(exfields[exfield]=='')
                end_of_dat_field = end_of_data_field(cases[field])
                if end_of_excluded_field:
                    casecopy.pop(field)
                else:
                    if end_of_dat_field:
                        break
                    else:
                        if isinstance(casecopy[field],list):
                            for i in range(len(casecopy[field])):
                                casecopy[field][i] = exclude_nested_fields(casecopy[field][i],
                                                                    exfields[exfield])
                        if isinstance(casecopy[field],dict):
                            casecopy[field] =exclude_nested_fields(casecopy[field],exfields[exfield])
    return(casecopy)
def end_of_data_field(field):
    """ This function determines if the field being examined by exclude_nested_fields() is the end of
    the field path (final layer of nesting) or if there are more fields within that field (is it a 
    record?) Records from GDC are either one dictionary, or lists of dictionaries.
    """
    end_of_field = True
    if isinstance(field,dict):
        end_of_field = False
        return(end_of_field)
    if isinstance(field,list):
        for entries in field:
            if isinstance(entries,dict):
                end_of_field = False
                return(end_of_field)