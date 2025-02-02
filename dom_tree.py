from bs4 import BeautifulSoup

with open("text_3.html", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

def print_dom_tree(element, indent=0):
    print(" " * indent + element.name if element.name else "")
    for child in element.children:
        if child.name:
            print_dom_tree(child, indent + 2)

print_dom_tree(soup)
