from socket import if_nameindex
from venv import create
import typesense
import csv
import json, os
 
from dotenv import load_dotenv

load_dotenv()
TYPESENSE_API_KEY = os.getenv('TYPESENSE_API_KEY')

client = typesense.Client({
  'nodes': [{
    'host': '35.204.119.30',  # For Typesense Cloud use xxx.a1.typesense.net
    'port': '8108',       # For Typesense Cloud use 443
    'protocol': 'http'    # For Typesense Cloud use https
  }],
  'api_key': TYPESENSE_API_KEY, 
  'connection_timeout_seconds': 5
})

def create_schema():
    schema = {
    'name': 'experiments',
    'fields': [
        {
        'name'  :  'Klantnaam',
        'type'  :  'string',
        'facet': True,
        },
        {
        'name'  :  'Situatie',
        'type'  :  'string'
        },
        {
        'name'  :  'Actie',
        'type'  :  'string'
        },
        {
        'name'  :  'Resultaat (kwantitatief)',
        'type'  :  'string'
        },
        {
        'name'  :  'Resultaat (metric)',
        'type'  :  'string'
        },
        {
        'name'  :  'Beschrijving resultaat',
        'type'  :  'string'
        },
        {
        'name'  :  'Experiment owner',
        'type'  :  'string',
        'facet': True
        },
        {
        'name'  :  'Aangemaakt',
        'type'  :  'string'
        },
        {
        'name'  :  'Waar heb je wat getest?',
        'type'  :  'string'
        },
        {
        'name'  :  'Visuals',
        'type'  :  'string',
        'index': False,
        'optional': True
        },
        {
        'name'  :  'E-commerce/Leadgen',
        'type'  :  'string',
        'facet': True
        },
        {
        'name'  :  'Apparaatcategorie',
        'type'  :  'string',
        'facet': True
        },
        {
        'name'  :  'Funnel',
        'type'  :  'string',
        'facet': True
        },
        {
        'name'  :  'Wat kunnen andere hiermee?',
        'type'  :  'string'
        }

    ]
    }

    client.collections.create(schema)


def csv_to_json(csv_path):
     
    data = []
     
    with open(csv_path, 'r', encoding='utf-8-sig' ) as csvf:
        csvReader = csv.DictReader(csvf)
        [data.append(rows) for rows in csvReader]
            
    return data


def recreate_schema():
    client.collections['experiments'].delete()
    create_schema()        
 
def import_documents():
    recreate_schema()
    experiments = csv_to_json(r'G:\Gedeelde drives\FS drive\Teams\D&A\Stageopdrachten\Experiment Database\04 POCs\04 TYPESENSE\SEA Experimenten.csv')
    print(experiments)
    experiments = [experiment for experiment in experiments if experiment["Klantnaam"]]
    client.collections['experiments'].documents.import_(experiments, {'action': 'create'})

   


def search(q):
    search_parameters = {
    'q'         : q,
    'query_by'  : ['Titel'],
    # 'sort_by'   : 'num_employees:desc',
    'num_typos': 1
    }

    results = client.collections['experiments'].documents.search(search_parameters)

    print(results)




if __name__ == '__main__':
    # recreate_schema()
    # import_documents()
    search('carl')
