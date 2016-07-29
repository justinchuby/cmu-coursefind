try:
    import catalogsearcher_es, utilities
except:
    from . import catalogsearcher_es, utilities


def generateSitemap(index=None):
    courseids = []
    output = ""
    course_index = index
    if index == "all_courses":
        course_index = "courses"
    if index is None:
        index = utilities.getCurrentIndex()
    query = """{
                "query" : {
                    "match_all" : {}
                },
                "fields": []
                }"""
    servers = ['courseapi-scotty.rhcloud.com:80']
    response = catalogsearcher_es.fetch(index, query, servers, 5000)
    if "hits" in response and response['hits']['hits'] != []:
        courseids = [elem['_id'] for elem in response['hits']['hits']]
    else:
        return False
    for courseid in courseids:
        output += "https://www.cmucoursefind.xyz/{}/{}\n".format(
            course_index.strip(), courseid.strip())
    return output
