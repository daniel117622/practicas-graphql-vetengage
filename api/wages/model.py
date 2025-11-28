import graphene

class CategoriaLaboral(graphene.ObjectType):
    category_id   = graphene.Int()
    category_name = graphene.String()

class EmpleadoEnCategoria(graphene.ObjectType):
    position_id    = graphene.Int()
    position       = graphene.String()
    lower_wage     = graphene.Float()
    upper_wage     = graphene.Float()
    employee_count = graphene.Int()
    category_id    = graphene.Int()