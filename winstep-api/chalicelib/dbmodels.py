from sqlalchemy import create_engine, Column, TIMESTAMP, TEXT
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import session, sessionmaker
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import ARRAY, Integer

import uuid
from datetime import datetime

base = declarative_base()


class ToDictMixin:
    @property
    def serialize(self):
        result = {}
        for col in self._model_cols:  # type: ignore
            value = getattr(self, col, None)
            result[col] = str(value)
        return result

class School(base, ToDictMixin):
    __tablename__ = "School"
    _model_cols = ["id", "name"]
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(TEXT)

class Study(base, ToDictMixin):
    __tablename__ = "Study"
    _model_cols = ["id", "title", "name", "createdDate", "description", "organism"]
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    createdDate = Column(TIMESTAMP(timezone=True), default=datetime.now(), nullable=False)
    description = Column(TEXT, nullable=False)
    organism = Column(TEXT, nullable=False)

class Observations(base, ToDictMixin):
    __tablename__ = "Observations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    studyId = Column(UUID(as_uuid=True), ForeignKey(column="Study.id"), nullable=False)
    name = Column(TEXT, nullable=False)
    type = Column(TEXT, nullable=False)
    collectionTime = Column(TIMESTAMP(timezone=True), nullable=False)

class ObservationsData(base, ToDictMixin):
    __tablename__ = "ObservationsData"
    observationId = Column(UUID(as_uuid=True), primary_key=True)
    teamId = Column(UUID(as_uuid=True), ForeignKey("ProjectTeam.id"), primary_key=True)
    value = Column(JSONB, nullable=False)
    collectedAt = Column(TIMESTAMP(timezone=True), default=datetime.now(), nullable=False)

class Student(base, ToDictMixin):
    __tablename__ = "Student"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schoolId = Column(UUID(as_uuid=True), ForeignKey(column="School.id"), nullable=False, )
    firstName = Column(TEXT, nullable=False)
    lastName = Column(TEXT, nullable=False)
    pronous = Column(TEXT, nullable=False)

class Researcher(base, ToDictMixin):
    __tablename__ = "Researcher"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schoolId = Column(UUID(as_uuid=True), ForeignKey(column="School.id"),nullable=False, )
    firstName = Column(TEXT, nullable=False)
    lastName = Column(TEXT, nullable=False)

class Instructor(base, ToDictMixin):
    __tablename__ = "Instructor"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    schoolId = Column(UUID(as_uuid=True), ForeignKey(column="School.id"), nullable=False, )
    firstName = Column(TEXT, nullable=False)
    lastName = Column(TEXT, nullable=False)

class ExperimentGroups(base, ToDictMixin):
    __tablename__ = "ExperimentGroups"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(TEXT, nullable=False)
    observationIds = Column(ARRAY(UUID(as_uuid=True)), nullable=False)

class Project(base, ToDictMixin):
    __tablename__ = "Project"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    studyId = Column(UUID(as_uuid=True), ForeignKey(column="Study.id"))
    instructorId = Column(UUID(as_uuid=True), ForeignKey(column="Instructor.id"))
    experimentGroups = Column(ARRAY(UUID(as_uuid=True)), default=[])

class ProjectTeam(base, ToDictMixin):
    __tablename__ = "ProjectTeam"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    projectId = Column(UUID(as_uuid=True), ForeignKey(column="Project.id"), nullable=False)
    status = Column(TEXT, nullable=False)
    name = Column(TEXT, nullable=False)
    studentIds = Column(ARRAY(UUID(as_uuid=True)), nullable=False, default=[])
    startDate = Column(TIMESTAMP(timezone=True), nullable=False)
    endDate = Column(TIMESTAMP(timezone=True), nullable=True)

