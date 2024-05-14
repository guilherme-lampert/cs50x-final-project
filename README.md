# recon
#### Video Demo:  <https://youtu.be/LPd1VWT4BFo>
#### Description:
RECON (Real Economic Data) is a web application that makes the process of getting and understanding economic data more accessible. With recon, people that never had contact with this type of information can easily understand it through our charts and/or use it when they download it.

## Tools used in this project
For this project, i used the following tools/programming languages:

* Python
* Flask, Werkzeug and Jinja2
* Pandas
* SQLite3 and Python's SQLite library
* JavaScript and Chart JS
* HTML, CSS and Bootstrap

## .py files

### __init__.py
Contains the factory application, `create_app()`. This function sets some configuration (secret key for sessions and the database path) and registers the blueprints used in the application, along with a function that closes the database connection every time a response is sent back to the user.

### auth.py
Is the blueprint responsible for handling authentication features.

#### `sign_up()`:
When called with a GET request, simply loads the templates/auth/signup.html template. When called via POST, checks if all the information sent in the form is correct and, in case they are, registers the user, sending them to the login page.

##### `login()`:
When called with a GET request, simply loads the templates/auth/login.html template. When When called via POST, checks if all the information sent in the form is correct and, in case they are, logs the user in, redirecting them to the index page.

#### `logout()`:
When called (only via GET), clears the current session and redirects the user to the index page, effectively logging the user out.

#### `load_logged_in_user():`
This is function is called every time a request is made. Basically, it checks if the user that made the request has a session cookie containing the user id. In case they do, the app loads the information about this user from the database into a Flask function called `g`, which is basically a dictionary provided by Flask. According to flask documentation, this variable is used to manage resources during a request.

### db.py

#### `get_db()`:
Creates a connection with the database by checking if this connection is not already is stored in the `g` variable. If not, the function gets a sqlite3 object and stores it in `g["db"]` so that the app can use it. 

#### `close_db()`:
Effectively closes the connection with the database by popping the `db` key from the `g` dict.

#### `init_app()`:
Ensures that the `close_db` function will be called after each response to close the connection.

### base.py

#### `index()`:
Loads the index page by rendering the templates/base/index.html template.

#### `tutorial()`:
Loads the tutorial page, rendering the templates/tutorial.html template.

### query.py

#### `index()`:
Loads the refined query menu, rendering the templates/query/index.html template.

#### `country_summary()`:
Loads the result page for a country. Basically, it checks if the country parameter was sent and if this parameter (acronym) is in the database. Then, it gets the API data and prepares it to be sent when rendering the templates/query/result.html template.

#### `refined_query_result()`:
Loads the result page for a specific query. It checks if the parameters in the query index are correct. Then, it gets the API data and prepares it to be sent when rendering the templates/query/result.html template.

#### `index_search_query_country()`:
Handles the autocomplete index menu. Whenever a GET request for this route is made, it searches for all the countries in the database that have the letters sent. The algorithm also checks if the word has more than 2 words. If it doesn't, it simply returns all the words that START with the letters sent, if it does, it returns all the countries that have the words sent, not mattering where they are positioned in the name of the countries.

#### `download()`:
Handles download requests. It is the route to be called then the user clicks the 'download' button. It basically generates a pandas dataframe and returns it in the response headers. Then, the Javascript in templates/query/result.html deals with the rest.

#### `save_query()`:
Handles save query requests. Everytime this route is called, it should receive a JSON file with all the information that a normal query has. If everything is ok and the query was named, it saves the query in the database. The queries can then be accessed in the templates/user/queries.html template. 

### user.py

#### `account()`:
Loads the account page getting the user's data from the database.

#### `change_username()`:
First, it checks if the new username and password were sent, and if everything is correct, it changes the username in the database.

#### `change_password()`:
Checks if the current password, new password and confirmation were sent. If everything is correct, it changes the user's password in the database.

#### `change_full_name()`:
Simply gets the first and last name and updates them in the database.

#### `delete_account()`:
Deletes the account if it correctly receives the user password and confirmation. This route will delete not only the user, but also the queries this user did.

#### `queries()`:
When called by a GET request, it simply loads the user queries. When a POST request is made, it redirects the user to the seat
If get, loads the user queries. If POST, redirects to the search `refined_query_result()` view whit the data that was sent to the route.

#### `delete_query()`:
Gets the id of the query and deletes it from the database.

### utils.py

#### `check_password(password):`:
With the help of a regex, checks if the user's password is valid when registering or changing it.

#### `login_required(view):`:
Decorator used when the login is required in a view. If the user tries to access a route that requires login, the decorator will return a 401 error.

#### `logoff_required(view)`:
Decorator used when the user can't be logged in. If the user tries to access a route that has this decorator, the decorator will redirect the user to the index page.

#### `load_countries()`:
Loads the countries from the database and returns them in a sqlite3 object


#### `load_indicators()`:
Loads the indicators from the database and returns them in a sqlite3 object

#### `load_categories():`:
Simply returns a list with all the categories in the database. They are hardcoded in the function because i need them in that exact order.

#### `get_api_data(countries, indicators, start_year, end_year)`:
Contacts the API data with the information that was sent to it. If there are no data, returns None. If there are data, it modifies the data return by the IMF API to include information such as categories and name of each country, returning a dictionary.

#### `get_df(data)`:
Receives a dictionary returned by `get_api_data()` and returns a pandas dataframe.

#### `load_user_queries(user_id)`:
Loads all the queries from the user and returns it, using a big SQL query that uses multiple JOINs. 

### recon.db
It is the database file that contains necessary information. The schema was designed as it follows:

- **user table**
id, username, password, first_name, last_name

- **country table**
id, name, acronym

- **indicator table**
id, acronym, label, category, description, unit

- **query table**
id, name, start_year, end_year, date, user_id

- **query_country table**
query_id, country_id

- **query_indicator table**
query_id, indicator_id

*The acronyms are used for API requests*

## templates

The templates folder hold the html files used in the project. I am not going to comment all of them, only the ones that used JS.

### base/index.html
Uses the static/js/base_index.js file. This file handles the AJAX requests to the `index_search_query_country()` view and modify the GET parameters before they are sent so that the correct parameter is sent.

### base/tutorial.html
This file simply uses Chart JS to plot the charts used in the explanation. The charts are always the same because the data is hard coded.

### query/index.html
Uses the static/js/query_index.js file. This file:
* Checks if no more than 5 checkboxes were selected
* Gives functionality to the clear and select all buttons
* Modify GET parameters before sending the form

### query/result.html
Receives a JSON with all the data sent from the `refined_query_result()` or `country_summary()` views. Then, it modifies it and uses this modified JSON to plot all the charts in the correct order (defined by the `load_categories()` function). Not only that, the scripts in this file also requests and handles the file sent by the `download()` view. It also sends a JSON file to `save_query()` to save the query when the save button is clicked.

## static

### img
There are only 2 images used in the project. The credits for them are given at the end of this README.

### js
Holds the JS files used in the project. They were already talked about.

### style
Only 2 CSS files were used, and they have just 2 and 1 styles being applied. Basically, they are just being used for the index image.

# ========= Features =========

## Everyone can access
Without creating an account, you have acces to the two main features of the application.

### Country summary
Search for any country of your choice and get a summary with the main macroeconomic characteristics of that country, such as the inflation rate, GDP, unemployment, and other topics. For that, all you have to do is go to the homepage, type the name of the country, hit the search button and wait. The application will display the data for the last 10 years of the country you chosed.

Tip: Don’t stop typing if you didn’t locate your country. In some cases, you must type more than 2 letters for it to appear. (Ex: The Bahamas will only appear after you typed Bah).

### Refined query
If you want to query more than just one country you can also do that. Just click on the 'Query' button at the navigation bar and you can select up to 5 countries of your choice, any indicator you want, and a time period that goes from 1980 to 2029. The result page will display everything that you asked for in the form of charts, except the information that is not available in the API. For instance, if you query the unemployment rate for China before 2017, you will get a page saying "No result was found for your query.", that is because China didn't provided this data.

## Features only registered users can access
If you create an account, you will have access to two exclusive features.

### Download
Download any query you made by hitting the 'Download' button at the end of a result page. You will be able to export your data to a CSV file and use it any way you want.

### Save query
Save your queries so that you can access them later without manually selecting everything again and again. You can save up to 10 queries and delete them any time you want.

# Charts
There are two different types of charts that can be plotted, depending on the selected period. If you select more than one year, the app will plot a line chart, but if you only select one year, a bar chart will appear.

## Line chart
Line charts are better when you want to visualize time series. In our case, that is exactly what we are doing with 2 or more years.

## Bar chart
Bar charts work better when you need to compare two or more 'things', in a moment of time. That's why we change the plotting to bar charts when you select only one year.

# Data source

## International Monetary Fund (IMF)
The IMF is a major financial agency of the United Nations with 190 member countries. The IMF provides an API that is very intuitive and can be used for free.

## World Economic Outlook (WEO)
The WEO is a survey published twice a year by the IMF staff. After its release, the data used in the survey is available to use in the IMF API, thats where I get the data from.

# The indicators
From the World Economic Outlook, i selected 15 indicators to be used in the queries, divided by 5 categories:

* National Accounts (7)
* People (2)
* Prices (2)
* Government finance (2)
* Balance of payments (2). 

# User options

If you want to modify/delete your account, you have the following options:

* Change your full name
* Change your username
* Change your password
* Delete your account

# Credits

## Homepage image

### Photo by Osman Rana, Unplsah

**Osman Rana profile:**
https://unsplash.com/pt-br/@osmanrana?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash

**Image link:**
https://unsplash.com/pt-br/fotografias/vista-aerea-do-edificio-alto-durante-o-dia-xJueGJJHnWs?utm_content=creditCopyText&utm_medium=referral&utm_source=unsplash

## User page icon

### User icons created by kmg design - Flaticon
https://www.flaticon.com/free-icons/user

## Favicon

### Designed by freepik
https://www.flaticon.com/br/icone-gratis/base-de-dados_1104982

## recon logo
For the logo i simply used a bootstrap icon:
https://icons.getbootstrap.com/icons/database/

# Additional information

The application was designed for a minimum width of 320px.

VScode is not originally configured to support jinja inside of Javascript, but i needed it to generate the charts. The article bellow may help you configure you environment to support this.

## Jinja, Javascript and VScode:
https://stackoverflow.com/questions/67735534/what-is-the-correct-way-to-put-in-jinja-code-to-javascript

## Official Flask documentation to use JSON:
https://flask.palletsprojects.com/en/3.0.x/patterns/javascript/