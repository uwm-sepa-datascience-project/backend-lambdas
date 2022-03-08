from contextlib import contextmanager
import sqlalchemy as db
from sqlalchemy.engine import create
from sqlalchemy.orm import session
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.engine.create import create_engine
from .dbmodels import Study

db_string = 'postgresql://localhost/winstepsepa?user=raghuveernaraharisetti'

def as_api_result(rows):
    result = []
    for row in rows:
        result.append(row[0].serialize)
    return result


def get_engine(connection_string):
    return create_engine(connection_string)

def get_sessionmaker():
    return sessionmaker(autoflush=True, autocommit=False, bind=get_engine(db_string))

def create_session():
    return get_sessionmaker()()

@contextmanager
def db_session():
    session = create_session()
    yield session
    session.close()

def db_execute(session, query):
    ResultProxy = session.execute

def is_studyid_valid(studyid, session):
    """
    Returns true if the given study id is valid i.e. exists in db
    """
    query = db.select([Study]).where(Study.columns.id == studyid)
    row = session.execute(query).fetchone()
    return row is not None

    

    

