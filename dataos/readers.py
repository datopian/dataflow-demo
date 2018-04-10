import urllib.request as request

def get(url):
    print(url)
    # cache = join('tmp', 'List_of_S%26P_500_companies.html')
    # request.urlretrieve(source, cache)
    return request.urlopen(url)

