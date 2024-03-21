

def title(result):
    """Return the title for this result, overriding the base template default of 'Result'"""
    return result[0]['Title']


def general_info(result):
    """Return all basic information in the first gmeta entry"""
    return result[0]
