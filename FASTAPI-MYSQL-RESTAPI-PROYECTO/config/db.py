from sqlalchemy import create_engine, MetaData

engine = create_engine("mysql+pymysql://proyecto:proyecto2022@localhost:3306/proyecto")
meta = MetaData()

conn = engine.connect()