import subprocess
import csv
import fnmatch
import os
import zipfile
import glob
import chardet
from datetime import datetime

from db_connection import *
from model import *
from helpers import *

files_top_dir = '../crawlers/files/'

def setup():
    # clean the files folder
    subprocess.call("rm -rf files", shell=True, cwd="../crawlers/")
    subprocess.call("mkdir files", shell=True, cwd="../crawlers/")
    # runs the crawler
    cmdscrappy = "scrapy crawl parties-crawler -o ./files/parties.csv -t csv"
    p = subprocess.call(cmdscrappy.split(), shell=False, cwd="../crawlers")

def generate_links(crawled_file):
    with open(crawled_file) as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)  # csv has just one row
        states = row['states'].split(",")
        parties = row['parties'].split(",")
        link = row['link']
        links = []
        for state in states:
            volatile_slink = link
            volatile_slink = volatile_slink.replace("state", state)
            for party in parties:
                volatile_plink = volatile_slink
                volatile_plink = volatile_plink.replace("party", party)
                links.append(volatile_plink)
    return links

def download_zipfiles():
    for link in links:
        download_file(link, files_top_dir)

def get_csv_files():
    csv_dir = files_top_dir + 'csv/'

    for file in glob.glob(files_top_dir + '*.zip'):
        zf = zipfile.ZipFile(file, 'r')
        for name in zf.namelist():
            if name.endswith('.csv'):
                outfile = open(os.path.join(csv_dir, os.path.basename(name)), 'wb')
                outfile.write(zf.read(name))
                outfile.flush()
                outfile.close()

    matches = []
    for root, dirnames, filenames in os.walk(files_top_dir):
        for filename in fnmatch.filter(filenames, '*.csv'):
            matches.append(os.path.join(root, filename))

#if all the functions are executed until here, we should have all the csv files in a folder crawlers/files/csv

def fill_party_table(crawled_file):

    with open(crawled_file) as csvfile:
        reader = csv.DictReader(csvfile)
        row = next(reader)  # csv has just one row
        parties = row['parties'].split(",")
        state = 'sp'
        prefix = 'filiados'

    csv_dir = files_top_dir + 'csv/'
    s = '_'
    for party in parties:
        seq = (prefix,party,state)
        file_name = s.join(seq) + '.csv'
        with open(csv_dir+file_name) as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.DictReader(csvfile,dialect=dialect)
            row = next(reader)  # only the first row matters
            acronym = row['SIGLA DO PARTIDO'].decode('cp1252')
            name = row['NOME DO PARTIDO'].decode('cp1252')
            if 'PARTIDO' not in name:
                query = name + ' partido'
            else:
                query = name
            addkeywords = ["Brasil","partido",acronym]
            photoUrl = wiki_image('pt',query,addkeywords)
            print [acronym,name,photoUrl]

            newParty = PartyDTO(name, acronym, photoUrl)
            partyId = PartyDAO.insertPartyInDB(newParty)

def fill_filiation_table():
    csv_dir = files_top_dir + 'csv/'
    count = 0

    candidates_2010 = filter_consulta_cand(".*", "2010")
    candidates_2014 = filter_consulta_cand(".*", "2014")
    candidates = candidates_2010 + candidates_2014
    cand_dict = {}
    for candidate in candidates:
        num = int(candidate.split(";")[27])
        cand_dict[num] = candidate

    print "cand_2010", len(candidates_2010)
    print "cand_2014", len(candidates_2014)
    print "candidates", len(candidates)
    print len(cand_dict)

    for file in os.listdir(csv_dir):
        #print("Searching for filiation data in file " + file)
        with open(csv_dir+file) as csvfile:
            dialect = csv.Sniffer().sniff(csvfile.read(1024))
            csvfile.seek(0)
            reader = csv.DictReader(csvfile,dialect=dialect)
            for row in reader:
                try:
                    num = int(row['NUMERO DA INSCRICAO'].decode('cp1252'))
                    situation = (row['SITUACAO DO REGISTRO'].decode('cp1252'))
                except ValueError:
                    num = 0;
                if (num in cand_dict) and (situation != 'CANCELADO'):
                    candidate = cand_dict.get(num)
                    cand_name = candidate.split(";")[10]
                    cand_bdate = candidate.split(";")[26]
                    if cand_name == "WALDEMIR MOKA MIRANDA DE BRITO":
                        print '\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH'
                        print cand_name, cand_bdate
                        print '\n'
                    try:
                        d = datetime.strptime(cand_bdate, "%d-%b-%y")
                    except ValueError:
                        d = datetime.strptime(cand_bdate, "%d/%m/%Y")
                    if d > datetime.now():
                        d = datetime(d.year - 100, d.month, d.day)
                    cand_bdate = d.strftime('%Y-%m-%d')
                    #cand_bdate = '-'.join(reversed(cand_bdate))
                    if cand_name == "Waldemir Moka Miranda de Britto":
                        print '\nAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAH'
                        print cand_name, cand_bdate
                        print '\n'
                    person = PersonDAO.findPersonbyNameAndBirthDate(cand_name,cand_bdate)
                    if person is not None:
                        count = count + 1
                        print "PERSON "+person.name.encode('utf-8')+" "+situation.encode('utf-8')

    print "NUMBER OF FILIATIONS FOUND: ", count

def parse_csv_files():
    csv_dir = files_top_dir + 'csv/'

    for file in glob.glob(csv_dir):
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)

fill_filiation_table()
