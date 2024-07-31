import copy
import globus_sdk
import pandas as pd
from urllib.parse import unquote
from globus_portal_framework.gclients import load_search_client
import globus_portal_framework.gsearch as gsearch


from globus_portal_framework.constants import (VALID_SEARCH_KEYS
)



def html_title(title):
    if title:
        title = f'<b>{title}</b>'
        return title
    return ''

def html_authors(authors):
    if authors is None:
        return ''
    if isinstance(authors, list):
        return ', '.join(authors).replace('\\"', '"')
    else:
        return authors

def html_url(url):
    if url:
        url = f'<a href="{url}" target="_blank" rel="noopener noreferrer">{url}</a>'
        return url
    return ''

def html_keywords(keywords):
    if keywords is None:
        return ''
    if isinstance(keywords, list):
        return ', '.join(keywords)
    else:
        return keywords

def html_abstract(abstract):
    if abstract:
        return abstract.replace('\\"', '"')
    return ''

def html_duration(duration):
    if duration:
        try:
            return str(int(duration))
        except:
            return ''
    return ''

def html_rating(rating):
    if rating:
        try:
            return format(float(rating), ".1f")
        except:
            return ''
    return ''



def to_html(entries, limit: bool):

    columns = ['Title', 'Authors', 'URL', 'Keywords', 'Abstract', 'Duration', 'Rating']

    try:
        metadata = []
        for entry in entries:
            res = {}
            for col in columns:
                if col in entry['entries'][0]['content'].keys():
                    res[col] = entry['entries'][0]['content'][col]
                else: 
                    res[col] = None
            metadata.append(res)
    except:
        return ""

    df = pd.DataFrame(metadata, columns=columns)

    content = df.to_html(escape=False, formatters=[
                html_title, html_authors, html_url, html_keywords, html_abstract, html_duration, html_rating
            ])

    if limit:
        return "You have reached the output limit. 1000 entries downloaded." + content
    else:
        return content


def parse(q):

    query_components = q.split("&")

    filters = []
    query = "*"
    for c in query_components:
        if '?q=' in c:
            query = unquote(c[len('?q='):]).replace('+', " ")
            
        elif 'filter-match-all.' in c:
            field, value = c[len('filter-match-all.'):].split('=')
            value = unquote(value).replace('+', " ")

            for filter in filters:
                if filter.get('field_name') == field:
                    filter['values'].append(value)
                    break
            else:
                filter = {}
                filter['field_name'] = field
                filter['type'] = 'match_all'
                filter['values'] = [value]
                filters.append(filter)


        elif 'filter-match-any.' in c:
            field, value = c[len('filter-match-any.'):].split('=')
            value = unquote(value).replace('+', " ")

            for filter in filters:
                if filter.get('field_name') == field:
                    filter['values'].append(value)
                    break
            else:
                filter = {}
                filter['field_name'] = field
                filter['type'] = 'match_any'
                filter['values'] = [value]
                filters.append(filter)


        elif 'filter-range.' in c:
            field, value = c[len('filter-range.'):].split('=')
            value_from = unquote(value.split('--')[0]).replace('+', " ")
            value_to = unquote(value.split('--')[1]).replace('+', " ")
            value = {'from': value_from, 'to': value_to}

            for filter in filters:
                if filter.get('field_name') == field:
                    filter['values'].append(value)
                    break
            else:
                filter = {}
                filter['field_name'] = field
                filter['type'] = 'range'
                filter['values'] = [value]
                filters.append(filter)

    # import sys
    # print(query, file=sys.stderr)
    # print(filters, file=sys.stderr)

    return query, filters


def html_search(index, query, filters, user):

    client = load_search_client(user)

    index_data = gsearch.get_index(index)

    search_data = {k: index_data[k] for k in VALID_SEARCH_KEYS
                   if k in index_data}

    search_data.update({
        'q': query,
        'facets': gsearch.prepare_search_facets(index_data.get('facets', [])),
        'filters': filters,
        'offset': 0,
        'limit': 50
    })

    import sys
    print(filters, file=sys.stderr)

    try:
        result = client.post_search(index_data['uuid'], search_data)
        
        if len(result.data['gmeta']) == 0:
            return None

        entries = copy.deepcopy(result.data['gmeta'])

        while result.data['has_next_page'] and len(entries) < 1000:
            search_data['offset'] = search_data['offset'] + 50
            result = client.post_search(index_data['uuid'], search_data)
            entries = entries + copy.deepcopy(result.data['gmeta'])

        reach_limit = result.data['has_next_page'] and len(entries) >= 1000

        return to_html(entries, reach_limit)

    except globus_sdk.SearchAPIError:
        return 'error: There was an error in your search, please try a different query or contact your HPC-ED.'
