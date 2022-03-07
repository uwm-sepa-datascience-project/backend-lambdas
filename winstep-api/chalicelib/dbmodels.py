from sqlalchemy import create_engine, Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY

import uuid
from datetime import datetime

db_string = 'postgresql://localhost/winstepsepa?user=raghuveernaraharisetti'
base = declarative_base()
db = create_engine(db_string, pool_pre_ping=True, connect_args={'options': '-csearch_path={}'.format('public')})
Session = sessionmaker(db)
session = Session()

class School(base):
    __table_name__ = "School"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)

class Study(base):
    __table_name__ = "Study"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    name = Column(String, nullable=False)
    createdDate = Column(TIMESTAMP, default=datetime.now(), nullable=False)
    description = Column(String, nullable=False)
    organism = Column(String, nullable=False)
    sampleSize = Column(int, nullable=True)

class Observations(base):
    __table_name__ = "Observations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    studyId = Column(UUID(as_uuid=True), ForeignKey(column="Study.id"), nullable=False)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    collectionTime = Column(int, nullable=False)

class ObservationsData(base):
    __table_name__ = "ObservationsData"
    teamId = Column(UUID(as_uuid=True), ForeignKey("ProjectTeam.id"))
    value = Column(JSONB, nullable=False)
    collectedAt = Column(TIMESTAMP, default=datetime.now(), nullable=False)

class Student(base):
    __table_name__ = "Student"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schoolId = Column(UUID(as_uuid=True), ForeignKey(column="School.id"), nullable=False, )
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    pronous = Column(String, nullable=False)

class Researcher(base):
    __table_name__ = "Researcher"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schoolId = Column(UUID(as_uuid=True), ForeignKey(column="School.id"),nullable=False, )
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)

class Instructor(base):
    __table_name__ = "Instructor"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schoolId = Column(UUID(as_uuid=True), ForeignKey(column="School.id"), nullable=False, )
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)

class ExperimentGroups(base):
    __table_name__ = "ExperimentGroups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    observationIds = Column(ARRAY(UUID(as_uuid=True)), nullable=False)

class Project(base):
    __table_name__ = "Project"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    studyId = Column(UUID(as_uuid=True), ForeignKey(column="Study.id"))
    instructorId = Column(UUID(as_uuid=True), ForeignKey(column="Instructor.id"))
    experimentGroups = Column(ARRAY(UUID(as_uuid=True)))

class ProjectTeam(base):
    __table_name__ = "ProjectTeam"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    projectId = Column(UUID(as_uuid=True), ForeignKey(column="Project.id"))
    status = Column(String, nullable=False)
    name = Column(String, nullable=False)
    studentIds = Column(ARRAY(UUID(as_uuid=True)), nullable=False)
    startDate = Column(TIMESTAMP, nullable=False)
    endDate = Column(TIMESTAMP, nullable=True)
    academicYearRangeStart = Column(int, nullable=False)
    academicYearRangeEnd = Column(int, nullable=False)

