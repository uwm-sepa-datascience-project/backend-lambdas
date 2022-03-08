import sqlalchemy as db

def main():
    db_string = 'postgresql://localhost/winstepsepa?user=raghuveernaraharisetti'
    engine = db.create_engine(db_string)
    connection = engine.connect()
    metadata = db.MetaData()
    school = db.Table('School', metadata, autoload=True, autoload_with=engine)
    print(school.columns.keys())
    print(repr(metadata.tables['School']))

    query = db.select([school])
    ResultProxy = connection.execute(query)
    ResultSet = ResultProxy.fetchall()
    print(ResultSet[:3])

if __name__ == "__main__":
    main()
