from .models import EnWord, RuWord, Collocation, Phrase, PartOfSpeech, CognateWord
from graphene_django import DjangoObjectType


class EnWordType(DjangoObjectType):
    class Meta:
        model = EnWord
        fields = '__all__'


class RuWordType(DjangoObjectType):
    class Meta:
        model = RuWord
        fields = '__all__'


class CollocationType(DjangoObjectType):
    class Meta:
        model = Collocation
        fields = '__all__'


class PhraseType(DjangoObjectType):
    class Meta:
        model = Phrase
        fields = '__all__'


class CognateWordType(DjangoObjectType):
    class Meta:
        model = CognateWord
        fields = '__all__'


class PartOfSpeechType(DjangoObjectType):
    class Meta:
        model = PartOfSpeech
        fields = '__all__'