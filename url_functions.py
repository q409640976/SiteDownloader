from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError


def verify_url(link, timeout_sec=1):
    """Checks if url is valid by checking the header."""
    try:
        return urlopen(link, timeout=timeout_sec).getcode() == 200
    except (HTTPError, URLError, ValueError):
        return False


def get_all_potential_urls(init_link):
    """Scrapes all potential urls on webpage. May not be valid urls."""
    curr_links = []
    html = urlopen(init_link)
    soup = BeautifulSoup(html.read(), 'html.parser')
    # for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
    for link in soup.findAll('a'):
        curr_link = link.get('href')
        if type(curr_link) == str:
            curr_links.append(curr_link)

    return curr_links


def get_all_urls(link, add_to=None, roots=None):
    """Gets all verified urls in the link such that root is present and not currently in the list
    they are getting added on to."""
    if roots is None:
        roots = ['', '']
    if add_to is None:
        add_to = []
    urls = []
    potential_urls = get_all_potential_urls(link)
    print(potential_urls)
    for potential_url in potential_urls:

        if roots[0] in potential_url or roots[1] in potential_url:
            if potential_url not in add_to and verify_url(potential_url):
                add_to.append(potential_url)
                urls.append(potential_url)

        # sometimes root + potential_url may be a valid web page
        else:

            for root in roots:
                new_pot_url = 'http://' + root + potential_url
                if new_pot_url not in add_to and verify_url(new_pot_url):
                    add_to.append('http://' + root + potential_url)
                    urls.append('http://' + root + potential_url)

    return urls


def remove_from_str(term, strs_to_remove):
    """Removes all strings in the list (or characters from string) from the term."""
    for str_to_remove in strs_to_remove:
        term = term.replace(str_to_remove, '')
    return term


def get_roots(link):
    """Retrieves root link."""
    link = remove_from_str(link, ['http://', 'https://'])
    if link[-1] != '/':
        main_link = ''
        for item in link.split('/')[:-1]:
            main_link += item + '/'
        return [main_link, remove_from_str(main_link, ' ~\"<>#%{}|\\^[]`')]
    return [link, remove_from_str(link, ' ~\"<>#%{}|\\^[]`')]


def get_all_urls_recursive(link_r, links_r, roots=None):
    """Recursive function to retrieve urls."""
    if not roots:
        roots = get_roots(link_r)
    for sub_link in get_all_urls(link_r, links_r, roots):
        get_all_urls_recursive(sub_link, links_r, roots)


def get_urls(link):
    """Fetches website urls via recursion."""
    links = []
    get_all_urls_recursive(link, links)
    return links
