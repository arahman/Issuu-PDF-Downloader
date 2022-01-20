import re
import urllib
import os

def main():
    import core.downloader as downloader

    print("Starting...\n")
    url = input("Enter the url of the PDF:")

    # Check that the URL provided by the user points to the entire document
    # and not to a specific page (e.g. https://issuu.com/user/docs/doc
    # instead of https://issuu.com/user/docs/doc/18)
    url_end = re.search(r'(.+)/\d+/?$', url)
    if url_end:
        # If there is a page number at the end of the URL
        print('The URL provided points to a specific page in the document.')
        url_without_page_number = url_end.group(1)
        print('Using the following URL instead:')
        print(url_without_page_number)
        url = url_without_page_number
    else:
        # If the URL points to the entire document, without any page number
        pass

    url_open1 = str(urllib.request.urlopen(url).read().decode("utf-8"))

    # Credits to https://txt2re.com/ for the regex (Almost all of it)
    # Sorry, I'm not lazy, but I hate making regex's
    re1 = '.*?'
    re2 = '((?:http|https)(?::\\/{2}[\\w]+)(?:[\\/|\\.]?)(?:[^\\s"]*)(?:png|jpg))'

    rg = re.compile(re1+re2, re.IGNORECASE | re.DOTALL)
    m = rg.search(url_open1)
    if m:
        httpurl = m.group(1)
        print('Starting from URI: ' + httpurl)
        filelist = downloader.downloader(httpurl)
        print('Started pdf creation...')
        filename = list(filter(None, url.split('/'))).pop()
        command = 'convert ' + " ".join(filelist) + ' ' + filename + '.pdf'
        print('running: ' + command)
        os.system(command)
        print('Completed pdf creation...')

        for f in filelist:
            fname = f.rstrip() # or depending on situation: f.rstrip('\n')
            if os.path.isfile(fname):
                os.remove(fname)
    else:
        print("Error! No image was found")


if __name__ == '__main__':
    main()
