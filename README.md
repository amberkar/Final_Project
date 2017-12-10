# Eventbrite Databases in Python
The project is to showcase skills gathered during my semester in SI-507! I utilized the Eventbrite API to visualize the types( categories_) of events Eventbrite offers.

## Usage
Type the following command to run the program:

```python3 final_project_code.py```

* The requirement for the code to work is [Python 3](https://www.python.org/downloads/)
* The whole ```code.py``` file is divided in to different sections
* Database name is built-in to the code, if you wish to change the database name, change it in the line number ```22```
* The following modules needed to be installed in the python virtual environment
	1. ```requests_oauthlib```
	2. ```sqlite3```
	3. ```plotly (more on this later)```
* All the necessary constants are predefined at immediately after python imports.
* The requirements for the project are generated in the ```requirements.txt``` file generated using ```pipreqs```

## Evenbrite API Details
* If you do not already have an eventbrite account you will need one to get your own app key and client_secret, this can be gathered by following the below link https://www.eventbrite.com/myaccount/apps/new/
* Once you create your account and have the app key and client_secret please add that information to the secret_data.py file

## Code Division

The code is divided in to few major functions and a class which are explained below
#### Database
* How to initialize it

	``` db = Database('<name of the database file>')```

* Three functions are defined to create the Following tables
	 1. Events
	 	* Event ID
	 	* Event Name
	 	* Event Status
	 	* Event Category ID
	 	* Event Format ID
	 2. Formats
	 	* Format ID
	 	* Format Name
	 	* Format Short Name
	 3. Categories
	 	* Category ID
	 	* Category Name
	 	* Category Short Name
* The Format ID of the Formats table and Category ID of the Categories table are used a join key to join the respective tables and get the required data.

### Output

Running the code performs the following operations in this order

1. Initially it checks if there exists a cached data of all the three tables, if Yes then the data from the cache is loaded if it is not expired according to the token value. If the token is expired or cache is absent, then it fetched the data using multiple API calls to the endpoint of Eventbrite.(NOTE the caching system utilized was adapter from the Caching system is adapted from oauth1_twitter_caching.py that was shown in class additionally the OAuth2 system is adapted from facebook_oauth.py that was shown in class as well)
2. Later the program creates the respective tables in the databases and inserts any new data that needs to be inserted and creates as and when required.
3. Finally the events the retrieved by a join and group by of categories and formats individually ans displyed on the console in a systematic format. Many more ways of functions can be written to get the data in other desired formats and scope for improvement of the system is always available in this case.
4. Also a two pie charts will be generated if the requirements for [Plotly](https://plot.ly/python/) are met. The account needs to be setup online and will be outlined briefly below.

In the end when you run final_project_code.py you will receive the below output:
		* catergories_cache_contents.json
		* Eventbrite.db - database file when opened has 3 tables ( Categories, Events and Formats-------Note* I used DB Browser for SQLite to view the database information)
		* events_cache_contents.json
		* formats_cache_contents.json
		* token.json
		* 2 plot.ly pie charts that will appear via browser

### Plotly setup
* Run the following command inside the python 3 virtual environment

	```pip install plotly```

* Create an account in the plot.ly website and get an API key following the instructions given [here](https://plot.ly/python/getting-started/).
* Go to the Python compiler inside the terminal by typing the following or your equivalent command of entering a python compiler.

	```python3```

* Follow the instructions in the above plot.ly link and create add your credentials to the file "secret_data".
