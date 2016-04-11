import mysql.connector
from model import *

class DbConnection:
    'Class that will handle the interaction with our MySQL Database'
    def __init__(self):
        self.connection = mysql.connector.connect(user='root', password='',
                                  host='127.0.0.1',
                                  port='3306',
                                  database='main')
        #TODO create verifications for the database connection catching the possible exceptions

    def __del__(self):
        self.connection.close()


class PersonDAO:
    'Data access object for person, include the methods for inserting and retrieving a person from the data base'
    @staticmethod
    def insertPersonOnDB(personDTO):
        #insert a person on the database and returns the unique id of this person on the database
        dbConnection = DbConnection()
        cnx = dbConnection.connection
        cursor = cnx.cursor()
        addPersonRequest = ""
        if not personDTO.profession:
            addPersonRequest = ("INSERT INTO person "
                                "(name, political_name, birth_date, gender, email, photo_url, profession) "
                                "VALUES (%(name)s, %(politicalName)s, %(birthDate)s, %(gender)s, %(email)s,"
                                "%(photoUrl)s, NULL)")
        else:
            addPersonRequest = ("INSERT INTO person "
                                "(name, political_name, birth_date, gender, email, photo_url, profession) "
                                "VALUES (%(name)s, %(politicalName)s, %(birthDate)s, %(gender)s, %(email)s,"
                                "%(photoUrl)s, %(profession)s)")

        cursor.execute(addPersonRequest, personDTO.__dict__)
        id = cursor.lastrowid
        cnx.commit()
        cnx.close()
        return id

    @staticmethod
    def findPersonOnDB():
        #returns a PersonDTO according to the search criteria
        print('Not yet implemented')


class FederalDeputyTermDAO:
    'Data access object for federal deputy term, include the methods for inserting and retrieving a terms from the DB'
    @staticmethod
    def insertTermOnDB(federalDeputyTermDTO):
        #insert a federal deputy term on the database
        dbConnection = DbConnection()
        cnx = dbConnection.connection
        cursor = cnx.cursor()

        addTermRequest = ("INSERT INTO federal_deputy_term "
                          "(id, person_id, state, initial_date, final_date) "
                          "VALUES (%(id)s, %(personId)s, %(state)s, %(initialDate)s, %(finalDate)s)")

        cursor.execute(addTermRequest, federalDeputyTermDTO.__dict__)
        cnx.commit()
        cnx.close()

    @staticmethod
    def findTermById(id):
        #returns a FederalDeputyTermDTO containing the data corresponding to the passed id
        dbConnection = DbConnection()
        cnx = dbConnection.connection
        cursor = cnx.cursor()

        selectTermRequest = ("SELECT * FROM federal_deputy_term WHERE id=" + str(id))

        cursor.execute(selectTermRequest)
        termRow = cursor.fetchone()

        return FederalDeputyTermDTO(termRow[0], termRow[1], termRow[2], termRow[3], termRow[4])

class ChamberAgencyDAO:
    'Data access object for chamber agency, include the methods for inserting and retrieving an agency from the DB'
    @staticmethod
    def insertAgencyOnDB(chamberAgencyDTO):
        #insert a deputies' chamber agency in the database
        dbConnection = DbConnection()
        cnx = dbConnection.connection
        cursor = cnx.cursor()

        addAgencyRequest = ("INSERT INTO chamber_agency "
                          "(id, acronym, description, active) "
                          "VALUES (%(id)s, %(acronym)s, %(description)s, %(active)s)")

        cursor.execute(addAgencyRequest, chamberAgencyDTO.__dict__)
        cnx.commit()
        cnx.close()

    @staticmethod
    def findAgencyById(id):
        #returns a ChamberAgencyDTO containing the data corresponding to the passed id
        dbConnection = DbConnection()
        cnx = dbConnection.connection
        cursor = cnx.cursor()

        selectTermRequest = ("SELECT * FROM chamber_agency WHERE id=" + str(id))

        cursor.execute(selectTermRequest)
        termRow = cursor.fetchone()

        return ChamberAgencyDTO(termRow[0], termRow[1], termRow[2], termRow[3])

class FedDeputyAgencyParticipationDAO:
    """
    Data access object for deputy participation on agencies, include the methods for inserting and retrieving a
    participation from the data base'
    """
    @staticmethod
    def insertParticipationOnDB(fedDeputyAgencyParticipationDTO):
        #insert a deputies' chamber agency participation in the database
        dbConnection = DbConnection()
        cnx = dbConnection.connection
        cursor = cnx.cursor()

        addParticipationRequest = ("INSERT INTO federal_deputy_term_agency_participation "
                          "(federal_deputy_term_id, agency_id, role) "
                          "VALUES (%(federalDeputyTermId)s, %(chamberAgencyId)s, %(role)s)")

        cursor.execute(addParticipationRequest, fedDeputyAgencyParticipationDTO.__dict__)
        cnx.commit()
        cnx.close()

class SenatorTermDAO:
    'Data access object for senator term'
    @staticmethod
    def insertTermOnDB(senatorTermDTO):
        #insert a senator term in the database
        dbConnection = DbConnection()
        cnx = dbConnection.connection
        cursor = cnx.cursor()

        addTermRequest = ("INSERT INTO senator_term "
                          "(id, person_id, state, initial_date, final_date) "
                          "VALUES (%(id)s, %(personId)s, %(state)s, %(initialDate)s, %(finalDate)s)")

        cursor.execute(addTermRequest, senatorTermDTO.__dict__)
        cnx.commit()
        cnx.close()

class SenateCommissionDAO:
    'Data access object for a commission from the senate'
    @staticmethod
    def insertCommissionOnDB(senateCommissionDTO):
        #insert a senate commission in the database
        dbConnection = DbConnection()
        cnx = dbConnection.connection
        cursor = cnx.cursor()

        addCommissionRequest = ("INSERT INTO senate_commission "
                          "(id, acronym, name, active) "
                          "VALUES (%(id)s, %(acronym)s, %(name)s, %(active)s)")

        cursor.execute(addCommissionRequest, senateCommissionDTO.__dict__)
        cnx.commit()
        cnx.close()

class SenateCommissionParticipationDAO:
    """
    Data access object for senator participations on commissions, include the methods for inserting and retrieving a
    participation from the data base
    """
    @staticmethod
    def insertParticipationOnDB(senateCommissionParticipationDTO):
        #insert a senate commision participation in the database
        dbConnection = DbConnection()
        cnx = dbConnection.connection
        cursor = cnx.cursor()

        addParticipationRequest = ("INSERT INTO senator_term_commission_participation "
                          "(senator_term_id, senate_commission_id, role) "
                          "VALUES (%(senatorTermId)s, %(senateCommissionId)s, %(role)s)")

        cursor.execute(addParticipationRequest, senateCommissionParticipationDTO.__dict__)
        cnx.commit()
        cnx.close()
