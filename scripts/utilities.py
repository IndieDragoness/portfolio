def count_string_in_dictionary_keys(str_value, dict_value):
    "Iterates through the keys of dict_value, counts the number of keys containing str_value."
    string_count = 0
    for s in dict_value.keys():
        if str_value in s:
            string_count += 1
    return string_count

if __name__ == "__main__":
    pass # Remove 'pass' when actual tests are inserted
    # Will be invoked if this module is being run directly, but not via import!
    # Use this area for testing this module directly.
