import xml.etree.ElementTree as ElementTree
import urllib2

from db_connection import *
from model import *

print('Downloading general agencies info...')
agenciesReader = urllib2.urlopen('http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterOrgaos')
agenciesXml = agenciesReader.read()
print('Parsing agencies\' information...')
agenciesDataTree = ElementTree.fromstring(agenciesXml)

agenciesList = []
i = 0
for agency in agenciesDataTree:
    agencyAttributes = agency.attrib
    chamberId = agencyAttributes['id']
    acronym = agencyAttributes['sigla'].strip()
    description = agencyAttributes['descricao']

    #TODO: on the next feature development, get correctly this info
    active = True

    print('Inserting info from ' + acronym + ' into the database...')
    newAgency = ChamberAgencyDTO(chamberId, acronym, description, active)
    ChamberAgencyDAO.insertAgencyOnDB(newAgency)

    print('Downloading member information from ' + acronym)

    agencyReader = None
    try: #if the chamber's shitty API fucks me up, I ignore the members of the agency
        agencyReader = urllib2.urlopen('http://www.camara.gov.br/SitCamaraWS/Orgaos.asmx/ObterMembrosOrgao?IDOrgao=' +
                chamberId)
    except:
        print('7x1')
        continue

    agencyXml = agencyReader.read()
    agencyDataTree = ElementTree.fromstring(agencyXml)
    agencyMembers = agencyDataTree.find('membros')

    if(len(agencyMembers) == 0):
        print(acronym + ' has no member registered on the chamber')
        continue

    idPresident = agencyMembers.find('Presidente').findtext('ideCadastro')
    print('Inserting president ' + agencyMembers.find('Presidente').findtext('nome') + ' relation into DB')
    presidentParticipation = FedDeputyAgencyParticipationDTO(idPresident, chamberId, 'P')
    FedDeputyAgencyParticipationDAO.insertParticipationOnDB(presidentParticipation)

    idFirstVp = agencyMembers.find('PrimeiroVice-Presidente').findtext('ideCadastro')
    print('Inserting first VP ' + agencyMembers.find('PrimeiroVice-Presidente').findtext('nome') + ' relation into DB')
    firstVpParticipation = FedDeputyAgencyParticipationDTO(idFirstVp, chamberId, 'F')
    FedDeputyAgencyParticipationDAO.insertParticipationOnDB(firstVpParticipation)

    idSecondVp = agencyMembers.find('SegundoVice-Presidente').findtext('ideCadastro')
    print('Inserting second VP ' + agencyMembers.find('SegundoVice-Presidente').findtext('nome') + ' relation into DB')
    secondVpParticipation = FedDeputyAgencyParticipationDTO(idSecondVp, chamberId, 'S')
    FedDeputyAgencyParticipationDAO.insertParticipationOnDB(secondVpParticipation)

    idThirdVp = agencyMembers.find('TerceiroVice-Presidente').findtext('ideCadastro')
    print('Inserting third VP ' + agencyMembers.find('TerceiroVice-Presidente').findtext('nome') + ' relation into DB')
    thirdVpParticipation = FedDeputyAgencyParticipationDTO(idThirdVp, chamberId, 'T')
    FedDeputyAgencyParticipationDAO.insertParticipationOnDB(thirdVpParticipation)

    idRapporteur = agencyMembers.find('Relator').findtext('ideCadastro')
    print('Inserting rapporteur ' + agencyMembers.find('Relator').findtext('nome') + ' relation into DB')
    rapporteurParticipation = FedDeputyAgencyParticipationDTO(idRapporteur, chamberId, 'R')
    FedDeputyAgencyParticipationDAO.insertParticipationOnDB(rapporteurParticipation)

    for member in agencyMembers.findall('membro'):
        idMember = member.findtext('ideCadastro')
        print('Inserting member ' + member.findtext('nome') + ' relation into DB')
        memberParticipation = FedDeputyAgencyParticipationDTO(idMember, chamberId, 'M')
        try:
            FedDeputyAgencyParticipationDAO.insertParticipationOnDB(memberParticipation)
        except:
            print(idMember)
