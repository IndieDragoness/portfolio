
def count_string_in_dictionary_keys(str_value, dict_value):
    "Iterates through the keys of dict_value, counts the number of keys containing str_value."
    string_count = 0
    for s in dict_value.keys():
        if str_value in s:
            string_count += 1
    return string_count
