import wikipedia
from utils.spech import speak

def wiki_summary(topic: str, sentences: int = 4) -> str:
    try:
        # Step 1: search for closest matching titles
        search_results = wikipedia.search(topic)
        if not search_results:
            return f"No results found for '{topic}'."
        
        # Step 2: pick the first search result
        best_match = search_results[0]
        
        # Step 3: fetch summary of the matched page
        summary = wikipedia.summary(best_match, sentences=sentences, auto_suggest=False, redirect=True)
        return f"Topic: {best_match}\n\n{summary}"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    userInput = input("topic : ")
    result = wiki_summary(userInput)
    print(result)
    speak(result)
