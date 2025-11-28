from flask import Flask , request, jsonify
from graphene import Schema
from duckdb import DuckDBPyConnection
from db_access.migrations import Migrations

from api.budget import *
from api.wages import *

class Query(BudgetQuery, WagesQuery):
    pass

class Mutation(WagesMutation, BudgetMutation):
    pass

def seed_data() -> DuckDBPyConnection:
    mig = Migrations("egresos_sueldos.db")
    mig.create_tables()
    mig.load_egresos_from_json("data/egresos_cajeme_2025.json")
    mig.load_sueldos_from_json("data/sueldos_grouped.json")
    return mig.get_data_access()



app = Flask(__name__)
db = seed_data()

schema = Schema(query=Query, mutation=Mutation)

@app.route("/graphql", methods=["POST"])
def graph_server():
    data = request.get_json()
    res = schema.execute( data['query'] , variables=data.get('variables') )
    
    return jsonify({
        'data'  : res.data,
        'errors': [str(err) for err in res.errors] if res.errors else None
    })

app.run()


