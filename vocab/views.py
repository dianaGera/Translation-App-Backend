from django.shortcuts import render
from django.db.models.functions import Length
from .models import EnWord


def get_word(request, word):
    if request.method == "POST":
        query = request.POST.get('q')
        search = EnWord.objects.filter(word__startswith=query).order_by(Length('word')).prefetch_related('translate')
        return render(request, 'home.html', {'search': search, 'var': True, 'query': query})
    if word == '_search':
        return render(request, 'home.html', {'var': False})
    else:
        search = EnWord.objects.prefetch_related(
            'translate',
            'part_of_speech',
            'collocation',
            'phrase',
            'cognate_word',
        ).get(id=word)
        return render(request, 'home.html', {'search': search, 'var': 'details'})