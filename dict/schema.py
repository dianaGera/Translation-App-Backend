import graphene
import vocab.schema


class Query(vocab.schema.Query, graphene.ObjectType):
    pass


class Mutaion(vocab.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutaion)