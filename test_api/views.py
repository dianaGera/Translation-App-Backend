from django.shortcuts import render
import requests


def get_word(request):
    query = 'query{allEnWord(word: "Rest"){edges{node{id, word, translate{ edges{ node{id, word}}},collocation {enCollocation, ruCollocation}}}}}'
    url = requests.get(f"http://127.0.0.1:8000/graphql/#query={query}")
    url = requests.get('http://127.0.0.1:8000/graphql/#query=%7BallEnWord('
                       'word%3A%20%22Rest%22)%20%7B%0A%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20node%20%7B%0A%20%20'
                       '%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20word%0A%20%20%20%20%20%20%20%20translate%20%7B%0A%20%20%20%20%20%20%20%20%20%20edges%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20node%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20id%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20word%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20collocation%20%7B%0A%20%20%20%20%20%20%20%20%20%20enCollocation%0A%20%20%20%20%20%20%20%20%20%20ruCollocation%0A%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%7D%0A%20%20%20%20%7D%0A%20%20%7D%0A%7D%0A')
    response = url.json()
    print(url)
    print(response)
    return render(request, 'home.html')
