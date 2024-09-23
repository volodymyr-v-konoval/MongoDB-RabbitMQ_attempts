from mongoengine import connect, Document, BooleanField, StringField


connect(host="mongodb+srv://konoval:1985@cluster0.30d35.mongodb.net/hw08?retryWrites=true&w=majority&appName=Cluster0", 
        ssl=True)

class Contact(Document):
    fullname = StringField(required=True, unique=True)
    email = StringField(max_length=50)
    sent = BooleanField(default=False)
    meta = {"collection": "rabbitMQ"}
