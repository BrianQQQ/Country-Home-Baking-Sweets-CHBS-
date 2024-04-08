# Country Home Baking & Sweets (CHBS)

This project is a web based application and is made for the client Suzanne Hill to expand her company's presence and give customers an easier way to 
purchase her products. The web app contains functionalities that gives customer a smooth and easy process when navigating the website.

## Table of Contents

- [Acknowledgement](#acknowledgement)
- [Techstack](#techstack)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Authors](#Authors)

# Acknowledgement

- [Django Ecommerce Website by Denis Ivy] https://www.youtube.com/watch?v=obZMr9URmVI&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng&index=2
- [Python and Django full stack tutorial] https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/learn/lecture/6616116?start=15#overview

# Tech Stack

**client:** Bootstarp, Css, Html, Javascript, Python

**Server:** Django, 

# Installation

1. Clone the repository: `git clone https://github.com/BrianQQQ/Country-Home-Baking-Sweets-CHBS-'
2. Navigate to the project directory: `cd ecommerce`
3. Install dependencies: `pip install -r requirements.txt`
4. run database.sql on mysql workbench
5. Migrate the database to your machines database: 'python manage.py migrate'
6. If you want to use the existing data run: 'python manage.py loaddata data_dump'
7. Go to settings.py in the ecommerce folder, scroll down to the bottom, under DATABASES variable, configure your SQL USER name and PASSWORD, under #SMTP/EMAIL Configuration put in the email you want the customers information to be sent to. 

# Usage

- To run the web application run 'python manage.py runserver' in your terminal, you will be be given a link, 
click on it and the browser will open with the homepage.
- If you want to create admin user (superuser) through terminal, under Team_03/ecommerce folder, open terminal and type `python manage.py createsuperuser`, follow the step to configure a new admin user.
- To use Google Authentication, remeber to set correct gmail account for the admin user(superuser).
- You can navigate thorough the users cart, menupage, and the contact page. add any item you want to your cart through the menu page.
- Then go to you cart page and click on checkout, you will be directed to a checkout page there the usere fills their information and checks out, 
an email of the customer deails and order details will be sent to the email you enter in No. 7 of the installation guide.
- To make changes to the database you can use the admin portal whic can be accessed by adding '/admin' to the link provided wne running the application
- To make changes to the data loaded in step 5 of the installation guide the username is 'suzanne' and password is 'suzannehill'
- NOTE: you have to be logged out of the admin portal to be a guest user

## Contributing

If you would like to contribute to the project, follow these steps:

1. Fork the project.
2. Create a new branch for your feature: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add new feature'`
4. Push to the branch: `git push origin feature-name`
5. Open a pull request.

# References

1. Django Ecommerce: https://www.youtube.com/watch?v=_ELCMngbM0E&list=PL-51WBLyFTg0omnamUjL1TCVov7yDTRng
2. Deploy Django App to Heroku: https://www.youtube.com/watch?v=6DI_7Zja8Zc&list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p&index=17
3. Django Official Documents: https://docs.djangoproject.com/en/5.0/

# Authors

- Po Jui Feng
- Yonging Ge
- Jinqui Hong
- Zoe Gong
- Keite Gularte

  
