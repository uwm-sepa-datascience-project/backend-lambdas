import uuid
import sqlalchemy as db

from chalice.app import Chalice
from chalice.app import BadRequestError, NotFoundError
from chalicelib import db_utils
from chalicelib.dbmodels import Observations, ObservationsData, Project, ProjectTeam, School

app = Chalice(app_name='winstep-api')


@app.route('/')
def index():
    return {'hello': 'world'}

@app.route("/getObservationsForStudy/{studyid}")
def get_observations_for_study(studyid):
    """
    Returns observation ids for given study id

    Throws:
    1. 404, if study id is not found
    """
    # 1. Check if study is valid
    # 2. Query Observations table to get all rows with given study id
    with db_utils.db_session() as session:
        if not db_utils.is_studyid_valid(studyid, session):
            return NotFoundError("Invalid studyid {studyid}, not found in the database")
        query = db.select([Observations]).where(Observations.columns.studyId==studyid)
        rows = session.execute(query).fetchall()
        return db_utils.as_api_result(rows)

@app.route("/instructor/getProjects")
def instructor_get_projects():
    """
    Returns all the projects created by the instructor
    """
    # TODO: get the userid from the auth service
    userid = "1"
    # get all the project ids for this user
    with db_utils.db_session() as session:
        query = db.select([Project]).where(Project.columns.instructorId == userid)
        rows = session.execute(query).fetchall()
        return db_utils.as_api_result(rows)
    

@app.route("/getTeams/{projectid}")
def get_teams(projectid):
    """
    Retrusn all teams given projectid
    """
    with db_utils.db_session() as session:
        query = db.select([ProjectTeam]).where(ProjectTeam.columns.projectId == projectid)
        rows = session.execute(query).fetchall()
        return db_utils.as_api_result(rows)

@app.route("/getObservationData/{teamid}")
def get_observation_data(teamid):
    """
    Returns all the observation data for given team id
    """
    with db_utils.db_session() as session:
        query = db.select([ObservationsData]).where(ObservationsData.columns.teamId == teamid)
        rows = session.execute(query).fetchall()
        return db_utils.as_api_result(rows)

@app.route("/getAllSchools")
def get_all_schools():
    """
    Returns all schools
    """
    with db_utils.db_session() as session:
        query = db.select([School])
        rows = session.execute(query).fetchall()
        return db_utils.as_api_result(rows)

@app.route("/newSchool")
def createNewSchool():
    """
    Create new school
    """
    with db_utils.db_session() as session:
        school = School()
        school.name = "UWM"  # type: ignore
        session.add(school)
        session.commit()

# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
