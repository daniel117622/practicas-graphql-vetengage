import graphene

class CategoriaEgreso(graphene.ObjectType):
    category_id   = graphene.Int()
    category_name = graphene.String()

class Egreso(graphene.ObjectType):
    codigo            = graphene.String()
    descripcion       = graphene.String()
    importe           = graphene.String()
    import_float      = graphene.Float()
    importe_formatted = graphene.String()
    category_id       = graphene.Int()