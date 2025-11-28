import json
import duckdb

class Migrations:
    def __init__(self, db_path=":memory:"):
        self.con = duckdb.connect(db_path)

    def create_tables(self):
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS CategoriaLaboral (
                category_id INTEGER PRIMARY KEY,
                category_name TEXT
            );
        """)
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS EmpleadoEnCategoria (
                position_id INTEGER PRIMARY KEY,
                position TEXT,
                lower_wage DOUBLE,
                upper_wage DOUBLE,
                employee_count INTEGER,
                category_id INTEGER REFERENCES CategoriaLaboral(category_id)
            );
        """)
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS CategoriaEgreso (
                category_id INTEGER PRIMARY KEY,
                category_name TEXT
            );
        """)
        self.con.execute("""
            CREATE TABLE IF NOT EXISTS Egresos (
                codigo VARCHAR PRIMARY KEY,
                descripcion TEXT,
                importe VARCHAR,
                import_float DOUBLE,
                importe_formatted TEXT,
                category_id INTEGER REFERENCES CategoriaEgreso(category_id)
            );
        """)

    def get_data_access(self):
        return self.con

    def load_egresos_from_json(self, json_path="data/egresos_cajeme_2025.json"):
        with open(json_path, "r", encoding="utf-8") as fp:
            egresos = json.load(fp)
        for cat_key, items in egresos.items():
            cat_id = int(cat_key.split(":")[0].strip())
            cat_name = cat_key.split(":")[1].strip()
            self.con.execute(
                "INSERT OR IGNORE INTO CategoriaEgreso (category_id, category_name) VALUES (?, ?)",
                [cat_id, cat_name]
            )
            for i in items:
                self.con.execute("""
                    INSERT OR REPLACE INTO egresos
                    (codigo, descripcion, importe, import_float, importe_formatted, category_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, [
                    i["codigo"],
                    i["descripcion"],
                    i["importe"],
                    i["import_float"],
                    i["importe_formatted"],
                    cat_id
                ])

    def load_sueldos_from_json(self, json_path="data/sueldos_grouped.json"):
        with open(json_path, "r", encoding="utf-8") as fp:
            sueldos = json.load(fp)

        for cat_key, items in sueldos.items():
            cat_id = int(cat_key.split(":")[0].strip())
            cat_name = cat_key.split(":")[1].strip()
            self.con.execute(
                "INSERT OR IGNORE INTO CategoriaLaboral (category_id, category_name) VALUES (?, ?)",
                [cat_id, cat_name]
            )
            for i in items:
                self.con.execute("""
                    INSERT OR REPLACE INTO EmpleadoEnCategoria
                    (position_id, position, lower_wage, upper_wage, employee_count, category_id)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, [
                    i["position_id"],
                    i["position"],
                    i["lower_wage"],
                    i["upper_wage"],
                    i["employee_count"],
                    cat_id
                ])

if __name__ == '__main__':
    from pprint import pprint
    mig = Migrations("duck.db")
    mig.create_tables()
    mig.load_egresos_from_json("data/egresos_cajeme_2025.json")
    mig.load_sueldos_from_json("data/sueldos_grouped.json")
    con = mig.get_data_access()

    print("SHOW TABLES")
    pprint(con.execute("SHOW TABLES").fetchall())

    print("CategoriaLaboral")
    pprint(con.execute("SELECT * FROM CategoriaLaboral LIMIT 5").fetchall())

    print("EmpleadoEnCategoria")
    pprint(con.execute("SELECT * FROM EmpleadoEnCategoria LIMIT 5").fetchall())

    print("CategoriaEgreso")
    pprint(con.execute("SELECT * FROM CategoriaEgreso LIMIT 5").fetchall())

    print("Egreso")
    pprint(con.execute("SELECT * FROM Egresos LIMIT 5").fetchall())