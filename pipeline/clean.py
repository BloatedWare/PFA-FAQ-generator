from bs4 import BeautifulSoup
import fetch

REMOVE_TAGS = ["script", "style", "noscript", "svg", "nav", "footer", "header", "aside", "form", "button", "input", "label"]

def clean_html_to_text(html: str) -> str:
    #create a tree from the html text so we can easily traverse
    soup = BeautifulSoup(html, "html.parser")
    
    #i remove the tags from the list i have above
    for tag in soup.find_all(REMOVE_TAGS):
        tag.decompose() #deletes tag 
    
    #extract title if it exists
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    #each "chunk" is just extracted data, a token of kind, a part of the information, all will be added to a chunks list for organization purposes 
    chunks = []
    if title:
        chunks.append(f"TITLE: {title}")
    
    #go the the tree (soup) and find all elements in the list below
    #if len is greater than 2 (chosen so that values like: '-' '|' 'OK' and other stuff that might not be that useful is removed)
    #can remove this criteria ofc but will keep it
    #label header text with it's header (will help with themes (same thing with TITLE: title_text))
    #for lists and paragraphs, the chunk wasn't labeled since it's just normal text
    for elem in soup.find_all(["h1", "h2", "h3", "li", "p"]):
        txt = elem.get_text(" ", strip=True)
        if txt and len(txt) > 2:
            if elem.name in ["h1", "h2", "h3"]:
                chunks.append(f"{elem.name.upper()}: {txt}")
            else:
                chunks.append(txt)
    
    text = "\n".join(chunks)
    return text

test_url = "https://www.bloomcoffee.ma/"
print(f"output of url({test_url}):\n{clean_html_to_text(fetch.fetch_html(test_url))}")
