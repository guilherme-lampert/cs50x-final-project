# recon

This is my very first project and it was made to complete the CS50x course from Harvard. For this exercise, I created a Flask application that uses the free IMF API to fetch data and return results in the form of charts. I also practiced the creation of user accounts and login sessions.

Since this is my first project, I understand that the code has a lot of room for improvement and I know this can only be achieved through practice and more projects. Thank you!

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

# Features

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
