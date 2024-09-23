from mongoengine import Document, StringField, ReferenceField, CASCADE, ListField
from mongoengine import connect

connect(host="mongodb+srv://konoval:1985@cluster0.30d35.mongodb.net/hw08?retryWrites=true&w=majority&appName=Cluster0", 
        ssl=True)

class Author(Document):
    fullname = StringField(required=True, unique=True)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    meta = {"collection": "authors"}


class Quote(Document):
    author = ReferenceField(Author, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=15))
    quote = StringField()
    meta = {"collection": "quotes"}
