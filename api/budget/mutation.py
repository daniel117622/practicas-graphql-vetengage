import graphene

class DummyMutation(graphene.Mutation):
    ok = graphene.Boolean()

    @staticmethod
    def mutate(root, info):
        return DummyMutation(ok=True)

class BudgetMutation(graphene.ObjectType):
    def mutate(root, info):
        return DummyMutation(ok=True)