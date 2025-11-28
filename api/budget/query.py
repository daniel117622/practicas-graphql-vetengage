from graphene import ObjectType , List , Int
from .model import CategoriaEgreso, Egreso
import logging
from db_access import Migrations

class BudgetQuery(ObjectType):
    budgets = List(Egreso, category_id=Int())
    budget_categories = List(CategoriaEgreso)

    def resolve_budgets(root, info, category_id=None):
        try:
            if category_id:
                q, p = "SELECT * FROM Egresos WHERE category_id = ?", [category_id]
                result = Migrations.connection.execute(q, p).fetchall()
                logging.info(f"Query: {q} Params: {p} Rows: {len(result)}")
            else:
                q, p = "SELECT * FROM EGRESOS", []
                result = Migrations.connection.execute(q).fetchall()
                logging.info(f"Query: {q} Rows: {len(result)}")
            return [
                Egreso(
                    codigo=r[0],
                    descripcion=r[1],
                    importe=r[2],
                    import_float=r[3],
                    importe_formatted=r[4],
                    category_id=r[5]
                ) for r in result
            ]
        except Exception as e:
            logging.error(str(e))
            return []

    def resolve_budget_categories(root, info):
        try:
            q = "SELECT * FROM CategoriaEgreso"
            result = Migrations.connection.execute(q).fetchall()
            logging.info(f"Query: {q} Rows: {len(result)}")
            return [CategoriaEgreso(category_id=r[0], category_name=r[1]) for r in result]
        except Exception as e:
            logging.error(str(e))
            return []