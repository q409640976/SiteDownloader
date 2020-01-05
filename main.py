import file_functions as ff


def temp_ui(url=None):
    """Temporary UI for downloading websites."""
    if not url:
        url = input("Type in your url here: ")
    exts = []
    while True:
        potential_ext = input("Type in your desired extensions (i.e. .pdf), or type \"done\" "
                              "when finished: ")
        if potential_ext == "done":
            break
        exts.append(potential_ext)
    ff.download_all_from_url(url, exts)
    print("""
=============================================
Finished! Check the assets folder!
=============================================
        """)


if __name__ == "__main__":

    url = "" # change url here

    if url == "":
        # or change via one line textfile.
        with open('url.txt', 'r') as f:
            url = f.readline()

    temp_ui(url)
