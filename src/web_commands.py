import webbrowser

def search_google(query: str):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Pesquisando por: {query}"

COMMANDS = {
    "google": lambda: search_google(input("O que deseja pesquisar? "))
}
