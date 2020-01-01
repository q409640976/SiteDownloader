import os
from urllib.request import urlopen
import url_functions as uf


def download_all_from_url(main_url, filetype_exts, path='assets'):
    """Downloads files from the website"""
    create_folder(path)
    urls = uf.get_urls(main_url)

    for url in urls:

        # download from it if it is a wanted filetype
        if check_if_file(url, filetype_exts):
            download_by_url(url, path + '/')

        # look for urls on that website and download if possible
        else:
            sub_urls = uf.get_all_urls(url, root=uf.get_root(main_url))

            for sub_url in sub_urls:
                # download from it if it is a wanted filetype
                if check_if_file(sub_url, filetype_exts):
                    download_by_url(sub_url, path + '/')


def check_if_file(url, filetype_exts):
    """Check if url corresponds to one of the user's desired filetypes.
    NOTE: should probably consider that if not specified, can be HTML."""
    is_file = False
    for filetype_ext in filetype_exts:
        if filetype_ext in url:
            is_file = True
            break
    return is_file


def download_by_url(url, folderpath):
    """Download the file/website itself."""
    response = urlopen(url)
    data = response.read()
    file = open(folderpath + url.split('/')[-1], 'w')
    file.write(data)
    file.close()


def create_folder(foldername='assets'):
    """Creates folder if it does not exist already"""
    if not os.path.exists(foldername):
        os.makedirs(foldername)