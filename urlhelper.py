"""Get as much info as possible about a URL.

"""

import mimetypes

import requests
import bs4

MAXIMUM_REDIRECTS = 4
FIELDS = [
    {
        'name': 'title',
        'soup_find': ('title', {}),
    },
]


_session = requests.Session()


class MaxRedirectError(Exception):

    def __init__(self):
        self.message = (
            "Head request redirected %d times (max is %d)"
            % (MAXIMUM_REDIRECTS + 1, MAXIMUM_REDIRECTS)
        )


class HttpError(Exception):

    def __init__(self, status_code):
        self.status_code = status_code
        self.message = "Encountered HTTP error %d" % status_code


def head_until_no_redirect(url, maximum_redirects=MAXIMUM_REDIRECTS):
    """Keep fetching the redirect URL until 200 (not 301) or fail.

    Return:
        url, Response:
        None:

    """

    if maximum_redirects:
        response = _session.head(url)

        if response.status_code == 301:
            maximum_redirects -= 1
            return head_until_no_redirect(
                response.headers['Location'],
                maximum_redirects
            )
        elif response.status_code == 200:
            return url, response
        else:
            raise HttpError(response.status_code)
    # maximum redirects is 0; we recursively reached the end
    else:
        raise MaxRedirectError()


def searchable_data_from_soup(soup):
    tags_to_return = {}
    for field in FIELDS:
        arg, kwargs = field['soup_find']
        found_tag = soup.find(arg, **kwargs)
        if found_tag:
            tags_to_return[field['name']] = found_tag.text

    return tags_to_return


# TODO: this docstring sucks, also clean all of this up
def fetch_searchable_data(url):
    """Fetch the title and meta tags of a remote
    HTML document, or fail and return None.

    May be expanded in the future.

    Note:
        does note check file extension for mimetype first, becuase more
        searchable data is hoped for than simply content_type

    Arguments:
        url (str): ---

    Returns:
        dict: Dictionary of searchable data...

    """

    searchable_data = {}

    # heuristics
    # first try file extension, if can't tell type then determine with head...
    # once you can get first x bytes for <head> info (meta, title, etc).
    try:
        url, head_response = head_until_no_redirect(url)
    except (HttpError, MaxRedirectError) as e:
        # we can at least try to guess the mimetype from file extension
        mimetype = mimetypes.guess_type(url)
        return {"content_type": mimetype[0]} if mimetype else None

    headers_from_url = head_response.headers
    content_type = headers_from_url['Content-Type'].split(';', 1)[0]

    # bail if we can't handle the type (because it's not "text/html")
    if content_type != "text/html":
        return {"content_type": content_type}

    # we know the content_type is text/html now
    searchable_data['content_type'] = "text/html"

    # First try to only request the first 400 bytes to get all of the
    # desired tags (which will be used to create searchable data).
    #
    # If this fails we request bytes 401 onward and combine,
    # extrapolating what we can
    response = _session.get(url, headers={'Range': 'bytes=0-400'})
    soup = bs4.BeautifulSoup(response.text, 'html.parser')
    more_searchable_data = searchable_data_from_soup(soup)

    # we couldn't find all of the tags we wanted in
    # the first 400 bytes of the response
    if not len(more_searchable_data) == len(FIELDS):
        # Store the old response text so we can skip getting it again
        old_response_text = response.text
        # Get the full page, but skip the part we already have (skip the
        # first 400 bytes), combining this new part with
        # the old_response_text!
        new_response = _session.get(url, headers={'Range': 'bytes=401-'})
        soup = bs4.BeautifulSoup(old_response_text + new_response.text, 'html.parser')

    searchable_data.update(searchable_data_from_soup(soup))
    return searchable_data
