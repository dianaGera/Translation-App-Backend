import json

import graphene
from django.db.models import Q
from django.http import JsonResponse
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType, DjangoListField
from graphene_django.filter import DjangoFilterConnectionField
from .models import EnWord, RuWord, Collocation, Phrase, PartOfSpeech, CognateWord
from .api_type import EnWordType, RuWordType, CollocationType, PhraseType, PartOfSpeechType, CognateWordType


# class Query(graphene.ObjectType):
#     all_en_words = graphene.List(EnWordType)
#     en_word = graphene.Field(EnWordType, word=graphene.String(), pk=graphene.Int())
#     ru_word = graphene.Field(RuWordType, word=graphene.String(required=True))
#
#     def resolve_all_en_words(self, info, **kwargs):
#         return EnWord.objects.prefetch_related(
#             'translate',
#             'collocation',
#             'phrase',
#             'cognate_word',
#             'part_of_speech'
#         ).all()
#
#     def resolve_en_word(self, info, word=None, pk=None):
#         return EnWord.objects.get(Q(word=word) | Q(pk=pk))


class RuWordNode(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = RuWord
        filter_fields = {
            'id': ['exact'],
            'word': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node, )


class EnWordNode(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = EnWord
        filter_fields = {
            'id': ['exact'],
            'word': ['exact', 'icontains', 'istartswith'],
            'translate': ['exact'],
            'translate__word': ['exact', 'icontains'],
        }
        interfaces = (relay.Node, )


class PartOfSpeechNode(DjangoObjectType):
    id = graphene.ID(source='pk', required=True)

    class Meta:
        model = PartOfSpeech
        fields = '__all__'
        filter_fields = {
            'id': ['exact'],
            'part_of_speech': ['exact', 'icontains', 'istartswith']
        }
        interfaces = (relay.Node, )


class Query(graphene.ObjectType):
    translate = relay.Node.Field(RuWordNode)
    all_ru_word = DjangoFilterConnectionField(RuWordNode)

    word = relay.Node.Field(EnWordNode)
    all_en_word = DjangoFilterConnectionField(EnWordNode)

    part_of_speech = relay.Node.Field(PartOfSpeechNode)
    all_parts = DjangoFilterConnectionField(PartOfSpeechNode)


class EnWordInput(graphene.InputObjectType):
    id = graphene.ID()
    word = graphene.String()
    get_word = graphene.String()

    id_ru = graphene.ID()
    ru_word = graphene.List(graphene.String)

    id_part = graphene.ID()
    part = graphene.List(graphene.String)


class CollocationInput(graphene.InputObjectType):
    en_collocation = graphene.String()
    ru_collocation = graphene.String()


class PhraseInput(graphene.InputObjectType):
    en_phrase = graphene.String()
    ru_phrase = graphene.String()


class CognateWordInput(graphene.InputObjectType):
    en_cognate_word = graphene.String()
    ru_cognate_word = graphene.String()


class CreateOrUpdateEnWord(graphene.Mutation):
    class Arguments:
        input = EnWordInput(required=True)
        coll_input = graphene.List(CollocationInput)
        phrase_input = graphene.List(PhraseInput)
        cognate_input = graphene.List(CognateWordInput)
    en_word = graphene.Field(EnWordNode)
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info, input=None, coll_input=None,
               phrase_input=None, cognate_input=None):
        en_word_instance, _ = EnWord.objects.get_or_create(word=input.word)

        def translate(en_word):
            if len(input.ru_word) > 0:
                for word in input.ru_word:
                    ru_word, _ = RuWord.objects.get_or_create(word=word)
                    en_word.translate.add(ru_word), en_word.save()

        def part_of_speech(en_word):
            if len(input.part) > 0:
                for part in input.part:
                    parts, _ = PartOfSpeech.objects.get_or_create(part_of_speech=part)
                    en_word.part_of_speech.add(parts), en_word.save()

        def collocation(en_word):
            if len(coll_input) > 0:
                for coll in coll_input:
                    colls, _ = Collocation.objects.get_or_create(en_collocation=coll["en_collocation"])
                    if colls and 'ru_collocation' in coll:
                        colls.ru_collocation = coll['ru_collocation']
                        colls.save()
                    en_word.collocation.add(colls), en_word.save()

        def phrase(en_word):
            if len(phrase_input) > 0:
                for phr in phrase_input:
                    phrases, _ = Phrase.objects.get_or_create(en_phrase=phr["en_phrase"])
                    if phrases and 'ru_phrase' in phr:
                        phrases.ru_phrase = phr['ru_phrase']
                        phrases.save()
                    en_word.phrase.add(phrases), en_word.save()

        def cognate(en_word):
            if len(cognate_input) > 0:
                for cog in cognate_input:
                    cognates, _ = CognateWord.objects.get_or_create(en_cognate_word=cog["en_cognate_word"])
                    if cognates and 'ru_cognate_word' in cog:
                        cognates.ru_cognate_word = cog['ru_cognate_word']
                        cognates.save()
                    en_word.cognate_word.add(cognates), en_word.save()

        translate(en_word_instance)
        if input.part:
            part_of_speech(en_word_instance)
        if coll_input:
            collocation(en_word_instance)
        if phrase_input:
            phrase(en_word_instance)
        if cognate_input:
            cognate(en_word_instance)

        return CreateOrUpdateEnWord(en_word=en_word_instance)


class UpdateEnWord(graphene.Mutation):
    class Arguments:
        input = EnWordInput()
    en_word = graphene.Field(EnWordNode)

    def mutate(self, info, input):
        en_word_instance = EnWord.objects.get(Q(word=input.get_word) | Q(pk=input.id))
        if en_word_instance:
            en_word_instance.word = input.word
            en_word_instance.save()
        return UpdateEnWord(en_word=en_word_instance)


class DeleteEnWord(graphene.Mutation):
    class Arguments:
        input = EnWordInput()
    en_word = graphene.Field(EnWordNode)

    @staticmethod
    def mutate(root, info, input):

        en_word_instance = EnWord.objects.get(Q(pk=input.id) |
                                              Q(word=input.word) |
                                              Q(word=input.get_word))
        data = {
            'title': "Deleted following",
            'word': en_word_instance,
            'phrases': en_word_instance.phrase.all(),
            'collocations': en_word_instance.collocation.all()
        }
        for relations in en_word_instance.phrase.all():
            relations.delete()
        for relations in en_word_instance.collocation.all():
            relations.delete()
        en_word_instance.delete()
        return None


class Mutation(graphene.ObjectType):
    create_en_word = CreateOrUpdateEnWord.Field()
    update_en_word = UpdateEnWord.Field()
    delete_en_word = DeleteEnWord.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
