import re
from typing import List, Any

import redis 
from redis_lru import RedisLRU

from models import Author, Quote

client = redis.StrictRedis(host='localhost', 
                           port=6379, 
                           password=None, 
                           encoding='utf-8')
cache = RedisLRU(client)


@cache
def find_by_tag(tag: str) -> list[str | None]:
    print(f"Find by {tag}")
    quotes = Quote.objects(tags__iregex=tag)
    result = [q.quote for q in quotes]
    return result


@cache
def find_by_author(author: str) -> list[list[Any]]:
    print(f"Find by {author}")
    authors = Author.objects(fullname__iregex=author)
    result = {}
    for a in authors:
        quotes = Quote.objects(author=a)
        result[a.fullname] = [q.quote for q in quotes]
    return result


if __name__ == '__main__':
    while True:
        input_var = input("Enter a tag to find or 'exit' to quit: ")
        if input_var == 'exit':
            break
        else:    
            tag = re.split(r'[:,]', input_var)

        match tag[0].strip():
            case 'name':
                print(find_by_author(tag[1].strip()))
            case 'tag':
                print(find_by_tag(tag[1].strip()))
            case 'tags':
                result = set()
                for t in tag[1:]:
                    quotes = find_by_tag(t.strip())
                    for quote in quotes:
                        result.add(quote)
                print(result)
            case _:
                print("You entered a wrong data!")












    # print(find_by_tag(('life',)))
    # print(find_by_tag(('life',)))

    # print(find_by_author('in'))
    # print(find_by_author('in'))
    # quotes = Quote.objects().all()
    # print([e.to_json() for e in quotes])
    