# Caching system is adapted from oauth1_twitter_caching.py that was shown in class
# OAuth2 system is adapted from facebook_oauth.py that was shown in class
from requests_oauthlib import OAuth2Session
import json
from datetime import datetime
from secret_data import app_key, client_secret
import webbrowser
import sqlite3
from sqlite3 import *
import plotly
import plotlyconfig
import plotly.plotly as py
import plotly.graph_objs as go

APP_KEY = app_key
CLIENT_SECRET = client_secret
AUTHORIZATION_BASE_URL = 'https://www.eventbrite.com/oauth/authorize'
TOKEN_URL = 'https://www.eventbrite.com/oauth/token'
REDIRECT_URI = 'https://www.programsinformationpeople.org/runestone/oauth'
EVENTS_REQUEST_URL = "https://www.eventbriteapi.com/v3/events/search"
FORMATS_REQUEST_URL = "https://www.eventbriteapi.com/v3/formats/"
CATEGORIES_REQUEST_URL = "https://www.eventbriteapi.com/v3/categories/"
DATABASE_NAME = 'Eventbrite.db'
EVENTS_TABLE = 'Events'
FORMATS_TABLE = 'Formats'
CATEGORIES_TABLE = 'Categories'
eventbrite_session = False

# ------- Caching -------

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"
DEBUG = False
EVENTS_CACHE_FNAME = "events_cache_contents.json"
FORMATS_CACHE_FNAME = "formats_cache_contents.json"
CATEGORIES_CACHE_FNAME = "categories_cache_contents.json"

try:
    with open(EVENTS_CACHE_FNAME, 'r', encoding='utf-8-sig') as cache_file:
        cache_json = cache_file.read()
        EVENTS_CACHE_DICTION = json.loads(cache_json)
except:
    EVENTS_CACHE_DICTION = {}

try:
    with open(FORMATS_CACHE_FNAME, 'r', encoding='utf-8-sig') as cache_file:
        cache_json = cache_file.read()
        FORMATS_CACHE_DICTION = json.loads(cache_json)
except:
    FORMATS_CACHE_DICTION = {}

try:
    with open(CATEGORIES_CACHE_FNAME, 'r', encoding='utf-8-sig') as cache_file:
        cache_json = cache_file.read()
        CATEGORIES_CACHE_DICTION = json.loads(cache_json)
except:
    CATEGORIES_CACHE_DICTION = {}


def has_cache_expired(timestamp_str, expire_in_days):
    now = datetime.datetime.now()
    cache_timestamp = datetime.datetime.strptime(timestamp_str, DATETIME_FORMAT)
    delta = now - cache_timestamp
    delta_in_days = delta.days
    return delta_in_days > expire_in_days


def get_from_cache(identifier, dictionary):
    identifier = identifier.upper()
    if identifier in dictionary:
        data_assoc_dict = dictionary[identifier]
        if has_cache_expired(data_assoc_dict['timestamp'],data_assoc_dict["expire_in_days"]):
            if DEBUG:
                print("Cache has expired for {}".format(identifier))
            del dictionary[identifier]
            data = None
        else:
            data = dictionary[identifier]['values']
    else:
        data = None
    return data


def set_in_data_cache(identifier, data, expire_in_days, cache_diction, cache_fname):
    identifier = identifier.upper()
    cache_diction[identifier] = {
        'values': data,
        'timestamp': datetime.datetime.now().strftime(DATETIME_FORMAT),
        'expire_in_days': expire_in_days
    }
    with open(cache_fname, 'w', encoding='utf-8-sig') as cache_file:
        cache_json = json.dumps(cache_diction)
        cache_file.write(cache_json)


def create_request_identifier(url, params_diction):
    sorted_params = sorted(params_diction.items(),key=lambda x:x[0])
    params_str = "_".join([str(e) for l in sorted_params for e in l])
    total_ident = url + "?" + params_str
    return total_ident.upper()


# ------- OAuth2 -------

def get_data_from_api(request_url, service_ident, params_diction, cache_diction, cache_fname, expire_in_days=7):
    ident = create_request_identifier(request_url, params_diction)
    data = get_from_cache(ident, cache_diction)
    if data:
        if DEBUG:
            print("Loading from data cache: {}... data".format(ident))
    else:
        if DEBUG:
            print("Fetching new data from {}".format(request_url))
        response = make_eventbrite_request(request_url, params_diction)
        data = response.json()
        set_in_data_cache(ident, data, expire_in_days, cache_diction, cache_fname)
    return data


def make_eventbrite_request(url, params=None):
    global eventbrite_session

    if not eventbrite_session:
        start_eventbrite_session()
    if not params:
        params = {}
    return eventbrite_session.get(url, params=params)


def start_eventbrite_session():
    global eventbrite_session

    try:
        token = get_saved_token()
    except FileNotFoundError:
        token = None

    if token:
        eventbrite_session = OAuth2Session(APP_KEY, token=token)
    else:
        eventbrite_session = OAuth2Session(APP_KEY, redirect_uri=REDIRECT_URI)
        authorization_url, state = eventbrite_session.authorization_url(AUTHORIZATION_BASE_URL)
        print('Opening browser to {} for authorization'.format(authorization_url))
        webbrowser.open(authorization_url)
        redirect_response = input('Paste the full redirect URL here: ')
        print("Got the url...")
        token = eventbrite_session.fetch_token(TOKEN_URL, client_secret=CLIENT_SECRET,
                                               authorization_response=redirect_response.strip())
        save_token(token)


def get_saved_token():
    with open('token.json', 'r') as f:
        token_json = f.read()
        token_dict = json.loads(token_json)
        return token_dict


def save_token(token_dict):
    with open('token.json', 'w') as f:
        token_json = json.dumps(token_dict)
        f.write(token_json)


class Database:

    def __init__(self, db_name):
        self.name = db_name
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()

    def __repr__(self):
        rep = 'Database Name: ' + self.name.split('.')[0] + '\n\n'
        self.cursor.execute('''SELECT * FROM sqlite_master WHERE type='table' ''')
        all_tables = self.cursor.fetchall()
        table_names = {}
        for each in all_tables:
            table_names[each[1]] = []
        for each in table_names:
            cursor = self.db.execute('select * from '+each)
            column_names = [description[0] for description in cursor.description]
            table_names[each] = column_names
        rep += 'Tables with columns: \n'
        ctr = 1
        for each in table_names:
            value = table_names[each]
            rep += str(ctr) + '. ' + each + ': '
            for a in value:
                rep += a + ' | '
            rep = rep[:-1] + '\n'
            ctr += 1
        return rep

    def __contains__(self, item):
        self.cursor.execute('''SELECT * FROM sqlite_master WHERE type='table' ''')
        all_tables = self.cursor.fetchall()
        table_names = []
        for each in all_tables:
            table_names.append(each[1])
        return item in table_names

    def create_events_table(self, events_data):
        data = events_data['events']
        try:
            self.cursor.execute(''' CREATE TABLE Events(id INTEGER UNIQUE, name TEXT, url TEXT, status TEXT, category_id TEXT, format_id TEXT) ''')
        except:
            if DEBUG:
                print("Events Table Already Exists")
        finally:
            for each in data:
                self.cursor.execute('''INSERT OR IGNORE INTO events(id, name, url, status, category_id, format_id) VALUES(?,?,?,?,?,?)''', (each['id'],
                                                                                                                   each['name']['text'],
                                                                                                                   each['url'],
                                                                                                                   each['status'],
                                                                                                                   each['category_id'],
                                                                                                                   each['format_id']))
            self.db.commit()

    def create_formats_table(self, formats_data):
        data = formats_data['formats']
        try:
            self.cursor.execute(''' CREATE TABLE Formats(format_id TEXT UNIQUE, name TEXT, short_name TEXT) ''')
        except:
            if DEBUG:
                print("Formats Table Already Exists")
        finally:
            for each in data:
                self.cursor.execute('''INSERT OR IGNORE INTO Formats(format_id, name, short_name)
                                  VALUES(?,?,?)''', (each['id'],
                                                     each['name'],
                                                     each['short_name'],))
            self.db.commit()

    def create_categories_table(self, categories_data):
        data = categories_data['categories']
        try:
            self.cursor.execute(''' CREATE TABLE Categories(category_id TEXT UNIQUE, name TEXT, short_name TEXT) ''')
        except:
            if DEBUG:
                print("Category Table Already Exists")
        finally:
            for each in data:
                self.cursor.execute('''INSERT OR IGNORE INTO Categories(category_id, name, short_name)
                                  VALUES(?,?,?)''', (each['id'],
                                                     each['name'],
                                                     each['short_name'],))
            self.db.commit()

    def read_from_table(self):
        print("Showing all categories")
        self.cursor.execute('''SELECT category_id, name FROM Categories''')
        all_rows = self.cursor.fetchall()
        for row in all_rows:
            # row[0] returns the first column in the query (name), row[1] returns email column.
            print('{0} : {1}'.format(row[0], row[1]))

        print()
        print("Showing all formats")
        self.cursor.execute('''SELECT format_id, name FROM Formats''')
        all_rows = self.cursor.fetchall()
        for row in all_rows:
            # row[0] returns the first column in the query (name), row[1] returns email column.
            print('{0} : {1}'.format(row[0], row[1]))

    def get_event_from_format(self):
        print("Showing all formats")
        self.cursor.execute('''SELECT format_id, name FROM Formats''')
        all_rows = self.cursor.fetchall()
        for row in all_rows:
            # row[0] returns the first column in the query (name), row[1] returns email column.
            print('{0} : {1}'.format(row[0], row[1]))
        running = True
        while True:
            choice = input("Select a format to see those events, press q to quit: ")
            if choice != 'q': # get all formats
                self.cursor.execute('SELECT e.name, status FROM Events e JOIN Formats f on e.format_id = f.format_id WHERE f.format_id = ' + choice)
                rows = self.cursor.fetchall()
                print(rows)
            else:
                running = False
                break
        return

    def group_by_formats(self):
        self.cursor.execute('''SELECT format_id, name FROM Formats''')
        all_formats = self.cursor.fetchall()
        formats = {}
        for eachf in all_formats:
            self.cursor.execute('SELECT e.name FROM Events e JOIN Formats f on e.format_id = f.format_id WHERE f.format_id = ' + eachf[0])
            events_format = self.cursor.fetchall()
            formats[eachf[1]] = [x[0] for x in events_format]
        return formats

    def group_by_categories(self):
        self.cursor.execute('''SELECT category_id, name FROM Categories''')
        all_categories = self.cursor.fetchall()
        categories = {}
        for eachc in all_categories:
            self.cursor.execute('SELECT e.name FROM Events e JOIN Categories c on e.category_id = c.category_id WHERE c.category_id = ' + eachc[0])
            events_category = self.cursor.fetchall()
            categories[eachc[1]] = [x[0] for x in events_category]
        return categories


events_data = get_data_from_api(EVENTS_REQUEST_URL, None, {}, EVENTS_CACHE_DICTION, EVENTS_CACHE_FNAME, 7)
formats_data = get_data_from_api(FORMATS_REQUEST_URL, None, {}, FORMATS_CACHE_DICTION, FORMATS_CACHE_FNAME, 7)
categories_data = get_data_from_api(CATEGORIES_REQUEST_URL, None, {}, CATEGORIES_CACHE_DICTION, CATEGORIES_CACHE_FNAME, 7)


db = Database(DATABASE_NAME)
db.create_events_table(events_data)
db.create_formats_table(formats_data)
db.create_categories_table(categories_data)
# print(db)
# print('Events' in db)

format_events_ = db.group_by_formats()
category_events_ = db.group_by_categories()


def show_events_by_formats(format_events):
    string = '------------------------------------\n'
    string += 'List of all formats and its events:\n'
    out_ctr = 1
    for each in format_events:
        value = format_events[each]
        if len(value) > 0:
            string += str(out_ctr) + '. ' + each + '\n'
            inr_ctr = 1
            for event in value:
                string += '\t' + str(inr_ctr) + '. ' + event + '\n'
                inr_ctr += 1
            out_ctr += 1
    print(string)


def show_events_by_categories(category_events):
    string = '------------------------------------\n'
    string += 'List of all categories and its events:\n'
    out_ctr = 1
    for each in category_events:
        value = category_events[each]
        if len(value) > 0:
            string += str(out_ctr) + '. ' + each + '\n'
            inr_ctr = 1
            for event in value:
                string += '\t' + str(inr_ctr) + '. ' + event + '\n'
                inr_ctr += 1
            out_ctr += 1
    print(string)
################# Plot.ly################
plotly.tools.set_credentials_file(username=plotlyconfig.username, api_key=plotlyconfig.api_key)

def plot_events_by_formats(format_events):
    labels = []
    values = []
    for each in format_events:
        labels.append(each)
        value = format_events[each]
        values.append(len(value))

    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], filename='Events by Formats')

def plot_events_by_categories(category_events):
    labels = []
    values = []
    for each in category_events:
        labels.append(each)
        value = category_events[each]
        values.append(len(value))

    trace = go.Pie(labels=labels, values=values)
    py.plot([trace], filename='Events by Categories')


show_events_by_formats(format_events_)
show_events_by_categories(category_events_)
try:
    plot_events_by_formats(format_events_)
    plot_events_by_categories(category_events_)
except:
     print("Error in using plotly, Please follow instructions in Readme.md")
