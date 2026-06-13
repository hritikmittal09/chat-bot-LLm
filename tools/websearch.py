from langchain_community.tools import DuckDuckGoSearchRun


def web_search(q):
    search = DuckDuckGoSearchRun()
    result = search.run(q)
    #print(result)
    return result

if __name__== "__main__":
    print(web_search("tell me all about Ra.one movie"))