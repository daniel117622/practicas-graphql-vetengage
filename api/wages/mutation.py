import graphene

class DummyMutation(graphene.Mutation):
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info):
        return DummyMutation(ok=True)

class WagesMutation(graphene.ObjectType):
    dummy = DummyMutation.Field()