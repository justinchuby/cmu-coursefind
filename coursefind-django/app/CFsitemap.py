try:
    import catalogsearcher_es
except:
    from . import catalogsearcher_es


def generateSitemap(index=None):
    if index is None:
        index = catalogsearcher_es.getCurrentIndex()
    query = """{
                "query" : {
                    "match_all" : {}
                },
                "fields": []
                }"""
    servers = ['courseapi-scotty.rhcloud.com:80']
    response = catalogsearcher_es.fetch(index, query, servers, 3000)
    if "hits" in response and response['hits']['hits'] != []:
        courseids = [elem['_id'] for elem in response['hits']['hits']]
    output = ""
    for courseid in courseids:
        output += "https://www.cmucoursefind.xyz/{}/{}\n".format(
            index.strip(), courseid.strip())
    return output
