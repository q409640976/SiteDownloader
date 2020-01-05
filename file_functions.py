import os
from urllib.request import urlopen
import url_functions as uf
import time

# note to self: make it so that you can download webpages.


def download_all_from_url(main_url, filetype_exts, path='assets'):
    """Downloads files from the website"""
    create_folder(path)
    print("""
=============================================
Fetching urls...
=============================================
    """)
    start_time = time.time()
    urls = uf.get_urls(main_url)
    print("""
=============================================
Finished fetching urls.
Now Downloading urls.
=============================================
    """)
    print("Time taken to fetch URLS:" + str(time.time() - start_time))
    start_time = time.time()
    print("# of urls: " + str(len(urls)))

    for url in urls:

        print("Downloading...")

        # download from it if it is a wanted filetype
        if check_if_file(url, filetype_exts):
            download_by_url(url, path + '/')

        # look for urls on that website and download if possible
        else:
            sub_urls = uf.get_all_urls(url, roots=uf.get_roots(main_url))

            for sub_url in sub_urls:
                # download from it if it is a wanted filetype
                if check_if_file(sub_url, filetype_exts):
                    download_by_url(sub_url, path + '/')

        print("Downloaded contents from: " + url)

    print("Time taken to download URLS:" + str(time.time() - start_time))


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
    file = open(folderpath + url.split('/')[-1], 'wb')
    file.write(data)
    file.close()


def create_folder(foldername='assets'):
    """Creates folder if it does not exist already"""
    if not os.path.exists(foldername):
        os.makedirs(foldername)
