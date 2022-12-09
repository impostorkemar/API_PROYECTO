from sqlalchemy import Table, Column
from sqlalchemy.sql.sqltypes import Integer, String, Date, Numeric, Float
from config.db import meta, engine

consultas = Table("consulta", meta, 
    Column("texto", String(10), primary_key=True)    
)

meta.create_all(engine)