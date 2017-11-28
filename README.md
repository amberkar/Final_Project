# Final_Project
The purpose of my project is to create a database showing events occurring in Denver, Colorado and Ann Arbor, Michigan. I will use Oath to help gather data from the Eventbrite API and then store them into Postgres databases using SQL with Python3.

I expect that my output for the Postgres database will consist of
- 1 table containing events in Ann Arbor ( within 20 miles)
- 1 table containing events in Denver ( within 20 miles)
- 1 table that combines the events in Denver and Ann Arbor and lists the top 10 least expensive events for the next 30 days


Part 1 Setup
- create a virtual environment and install required modules
- create a caching system

Part 2 Class Structure
- __init__: setup all attributes
- __repr__
- contains__


Part 3 Retrieve Desired Data
- create a function for Ann Arbor events with 20 miles
- create a function for Denver events within 20 miles
- create a function for Ann Arbor event prices
- create a function for Denver event prices

Part 4: Storing Data into Postgre database
- create a database table for Ann Arbor events within 20 miles
- create a database table for Denver events within 20 miles
- create a database that looks at price and sorts event from lowest to highest price

Part 5: Visualizations
- Use Plotty to visualize data from databases

Part 6: Test Suite
- test caching system
- test database tables
- test classes


Part 7: Miscellaneous
- requirements.txt
- add secret data file(without my key)
