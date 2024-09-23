import json

from mongoengine import connect
from mongoengine.errors import NotUniqueError

from models import Author, Quote

connect(host="mongodb+srv://konoval:1985@cluster0.30d35.mongodb.net/hw08?retryWrites=true&w=majority&appName=Cluster0", 
        ssl=True)

if __name__ == '__main__':
    
    with open('authors.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            try:
                author = Author(fullname=el.get('fullname'), 
                                born_date=el.get('born_date'),
                                born_location=el.get('born_location'),
                                description=el.get('description'))
                author.save()
            except NotUniqueError:
                print(f"The author alreade exists {el.get('fullname')}")


    with open('qoutes.json', encoding='utf-8') as fd:
        data = json.load(fd)
        for el in data:
            author, *_ = Author.objects(fullname=el.get('author'))
            quote = Quote(quote=el.get('quote'), 
                          tags=el.get('tags'),
                          author=author)
            quote.save()
