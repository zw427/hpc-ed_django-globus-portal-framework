import pandas as pd

class ValidationError(Exception):
    pass

def validate_url(value):
    if not isinstance(value, str):
        return False
    return True

def validate_resource_url_type(value):
    return True

def validate_language(value):
    valid_languages = ['en']
    if value not in valid_languages:
        return False
    return True

def validate_cost(value):
    return True

def validate_title(value):
    return True

def validate_provider_id(value):
    return True

def validate_subject(value):
    required_prefix = "urn:ogf.org:glue2:access-ci.org:resource:cider:infrastructure.organizations:"
    if not isinstance(value, str) or not value.startswith(required_prefix):
        return False
    return True

def validate_id(value):
    return True

def validate_visible_to(value):
    return True


def validate_excel_sheet(excel_file_path):
    df = pd.read_excel(excel_file_path)
    validation_functions = {
        'URL': validate_url,
        'Resource_URL_Type': validate_resource_url_type,
        'Language': validate_language,
        'Cost': validate_cost,
        'Title': validate_title,
        'Provider_ID': validate_provider_id,
        'subject': validate_subject,
        'id': validate_id,
        'visible_to': validate_visible_to,
    }

    errors = []

    for column, validate_func in validation_functions.items():
        if column in df.columns:
            for index, value in df[column].items():
                if not validate_func(value):
                    errors.append(f"Invalid value in cell ({index + 2}, '{column}')")

    if errors:
        raise ValidationError(f"Validation errors found:\n" + "\n".join(errors))

    print("All columns validated successfully.")
    return df
