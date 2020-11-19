"""
This file is meant to define functions that CDA needs to implement on top of those defined 
in previous files from the ISB-CGC ETL process located here: https://github.com/isb-cgc/NextGenETL
"""
"""
Functions needed to implement transformations upon the data
"""
import sys
import jsonlines
def transform_nested_fields(cases,trans_dict):
    """This function receives 1 case level dictionary directly from GDC API output, as well as
    a dictionary of dictionaries for the fields to be excluded from the data recieved from GDC.
    It recursively searches through the nesting layers to remove unwanted fields from the data. 
    This can be potentially modified to also transform data directly from the GDC API
    """
    if not isinstance(cases,dict):
        print('cases')
        print(type(cases))
        if isinstance(cases,list):
            print(cases[0])
        quit()
    if not isinstance(trans_dict,dict):
        print('exfields')
        print(type(trans_dict))
        quit()
    
    casecopy = cases.copy()
    for field_name, field_val in cases.items():
        for trans_name, trans_val in trans_dict.items():
            if field_name == trans_name:
                excluded_field =(trans_val=='exclude')
                if excluded_field:
                    casecopy.pop(field_name)
                elif isinstance(cases[field_name],list):
                    for i in range(len(cases[field_name])):
                        if isinstance(cases[field_name][i],list):
                            print('wtf is this a list?')
                            print(field_name)
                        casecopy[field_name][i] = transform_nested_fields(casecopy[field_name][i], trans_dict[trans_name])
                elif isinstance(cases[field_name],dict):
                    casecopy[field_name] = transform_nested_fields(casecopy[field_name], trans_dict[trans_name])
                else:
                    temp = casecopy.pop(field_name)
                    tempdict = dict({field_name:temp})
                    if isinstance(trans_dict[trans_name],str):
                        print(trans_dict[trans_name])
                    if isinstance(trans_val,dict):
                        if 'transformations' in list(trans_val.keys()) :
                            tempdict = apply_all_transformations(tempdict, trans_val['transformations'])
                            casecopy.update(tempdict)
                        else: 
                            print('trans_val is dict and matches field name')
                            print(trans_val)
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

def apply_all_transformations(data,transforms):
    if 'simple' in transforms.keys():
        temp = apply_list_of_lists(data,transforms['simple'])
    return(temp)

def apply_list_of_lists(data,list_trans):
    temp = data.copy()
    for lists in list_trans:
        if lists[1] == '':
            temp = lists[0](data)
        else:
            temp = lists[0](data,lists[1])
    return(temp)

def functionalize_trans_dict(trans_dict):
    temp = trans_dict.copy()
    for trans_name, trans_val in trans_dict.items():
        if isinstance(trans_val,dict):
            if 'transformations' in list(trans_val.keys()):
                for key in trans_dict[trans_name]['transformations'].keys():
                    for i in range(len(trans_dict[trans_name]['transformations'][key])):
                        temp[trans_name]['transformations'][key][i][0] = globals()[trans_dict[trans_name]['transformations'][key][i][0]]
            else:
                temp[trans_name] = functionalize_trans_dict(trans_val)
    return(temp)

def main_of_transform_data_in_jsonl(API_PARAMS,scratchfp_in,scratchfp_out)
    """ This function will read from scratchfp_in, apply transformations to data as instructed from the YAML file,
    and write to another JSONL file scratchfp_out
    """
    with jsonlines.open(scratchfp_in) as reader:
        with jsonlines.open(scratchfp_out, mode = 'w') as writer:
            for case in reader: # for each entry in the jsonl file
                temp_entry = transform_nested_fields(case,API_PARAMS['TRANSFORM_FIELDS'])
                writer.write(temp_entry)
"""
Actual Transforms of the data
"""
def none_to_zero(dictr):
    field_name = list(dictr.keys())[0]
    if dictr[field_name] == 'None':
        dictr[field_name]=0
    return(dictr)
