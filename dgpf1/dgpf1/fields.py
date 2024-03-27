import datetime

def title(result):
    """Return the title for this result, overriding the base template default of 'Result'"""
    return result[0]['Title']


def general_info(result):
    """Return all basic information in the first gmeta entry"""
    return result[0]


def detail_result_display_fields(result):
    """
    Return all fields in a consistent order, and attach any field specific info
    like if a field is a number or needs special rendering.
    """
    possible_date_fields = ["Version_Date", "Start_Datetime"]
    info = general_info(result)
    leading_fields = [
        {"field_name": "Title"},
        {"field_name": "Abstract"},
        {"field_name": "Authors"},
        {"field_name": "Expertise_Level"},
        {"field_name": "Learning_Outcome"},
        {"field_name": "Learning_Resource_Type"},
        {"field_name": "Target_Group"},
        {"field_name": "Keywords"},
    ]
    trailing_fields = [
        {"field_name": "Provider_ID", "display_name": "Provider ID"},
        {"field_name": "Rating"},
    ]
    known_field_names = [fl["field_name"] for fl in leading_fields + trailing_fields]
    other_fields = [{"field_name": f} for f in info
                    if f not in known_field_names]
    display_fields = leading_fields + other_fields + trailing_fields
    # Populate values from info
    for item in display_fields:
        item["display_name"] = item.get("display_name", item["field_name"].replace("_", " "))
        item["value"] = info.get(item["field_name"])
#        if isinstance(item["value"], list):
#            item["value"] = ", ".join(item["value"])
        if item["field_name"] in possible_date_fields:
            try:
                item["value"] = datetime.datetime.fromisoformat(item["value"].replace("Z", "+00:00")).strftime("%b %d  %Y %H:%M:%S %Z%z")
            except Exception:
                # If the date cannot be parsed, just leave it.
                pass
    return display_fields
