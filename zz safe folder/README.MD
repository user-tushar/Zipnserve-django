# First we have to create Home of website ..
# Generally we have to create Multiple Apps for the e-commerce website ... 
# Like , First  we create Category Userapp
# then, create models in category and add that model to admin pannel.
# install the pillow package. (pip install pillow)
# make migrations & migrate .
# create super user .
--> username : adminself
--> email : if you want you can give else just hit enter
--> password : rootzip
# in admin pannel .. we are using username & pass to log in to admin pannel ..
# but in interprise level we use email to log-in .. so for that we have to create out own custom user model.
# so, for that we have to creat an Account Userapp
# now create  a custom Account model for  normal user login, super user login and account input.

# we have to add add this to ssettings.py 
--> AUTH_USER_MODEL = 'accounts.Account'
# it saying to django that we are using "Account" authentication user model  which is inside "accounts" userapp
# now register to admin pannel but before that delete the previous admin data ... just by simply deleting  database file & 001 & 002 file from migrations folder of category app.
# Now make migrations & migrate .
# create super user .
# Now u will see .. insted of username,password ... it is asking Email, username, first_name, last_name, password .. Bcoz of our custom model.
--> email : rajatkupatra19@gmail.com
--> username : adminself
--> first_name : Tushar
--> last_name : Patra
--> password : rootzip
--> url path for access the admin pannel `SecurityZiPRo0TtUsHAr`
<!--* insted of admin/ you have to write SecurityZiPRo0TtUsHAr/ this. -->

# Our Main Admin is in Account Userapp .. coz in settings .. we've configured that .
--> AUTH_USER_MODEL = 'accounts.Account'
# we are using "Account" authentication user Admin model  which is inside "accounts" userapp  
# and .. we are registering all user app's model through admin.py  into Account's user Admin. 


<!--* -------------------------------------------------------------------------------------------------------- -->
<!--* ========================================= SECURITY =============================================================== -->
<!--*------------------------------------------------------------------------------------------------------  -->



<!--** =================================HIDING SENSITIVE FILES & INFO FOR ALL THE USERS================================================== -->


# We have to hide the sensitive information from the users or  if we publically post the project to github .. then we need to hide the sensitive info ... SO
To store the sensitive information ... we use python decouple Package ... and we have to install it ``` pip install python-decouple ```

--> then we have to configure this in settings.py ``` from decouple import config ```
--> add the " .env " file into " .gitignore " file ... 
# .gitignore 
--> this is a file we have to create to prevent pushing sensitive information or files into Git Hub ... while we push our code to the git Hub.
--> in this file whatever file we include ... that file will get ignored and don't get publiccally upload on github.

# /*Now back to config*/

--> now create a " .env " named file in the root directory.
--> now copy the sensitive information there ... without the quotation (" ") and without the space before or after (=) sign.
-->and now remove the information 
--> pass the config('key') in the original information page ... where you have copied 

* example 
- email (key) = "xyz.com" (value) 
- we copied the entire key & value and store it in '.env' file without quotation.
``` email=xyz.com ``` 
- and now we removed the value and there we pass the key of that data.
``` email = config('email') ``` <!-- internally, it will be come with quotation and value likee  emaill = "xyz.com" -->

- it by default give string type value 
- if there is a value which is a intiger type , then we have to convert it by adding another argument .

- ex
email  = 520
copied to .env = ``` email=520 ``` 
email = config('email', cast=int)
<!-- without cast it will come like this email  = "520" ,
with cast email = 520 -->

same for boolean value --->
email  = True
copied to .env = ``` email=True ``` 
email = config('email', cast=bool)
<!-- without cast it will come like this email  = "True" ,
with cast email = True -->

<!--*=============================================================  -->




<!--** =================================SHOWING SENSITIVE FILES & INFO FOR SOME SELECTED USERS================================================== -->

# just copy the .env structure and create a new file named .env-sample and paste there but remove the values keep the key ... so your code will be secure ... but the user know that this thing is necessary to be added. 



<!--* $$$$$$$$$$$$$$$$$$$$$$$$$$$$$ # CHANGE THE ADMIN URL FOR SECURITY PURPOSE $$$$$$$$$$$$$$$$$4 -->
# we know we that we can access admin pannel through /admin url .. every body does so it's necessary to change the url ... for that 
--> go to project folder. (The main one : where settings.py exists that one)
--> in that folder go to urls.py
--> you'll see one url path
which have ``` path('admin/', admin.site.urls), ```
--> just remove the `admin/` and give a strong and different name in that place .. 
--> in my case i've given this `SecurityZiPRo0TtUsHAr` 

<!-- *$$$$$$$$$$$$$$$$$$$$$$$$$$  # ADVANCE ADMIN PANNEL PROTECTION $$$$$$$$$$$$$$$$$$ -->

# We can use a package called ``` pip install django-admin-honeypot ```

# What is django-admin honeypot ?
--> See, we have changed the Admin url path.
--> If someone tries to access our Admin pannel ... what this package will do...
- Even though the admin pannel is not avilavle at that 'Admin/' url .. This package will duplicate the django admin login pannel. 
- And the fraudster will think that ,this is the django admin pannel and try to logging in in this .
- but, this package what will do .. it will just record his login attempts and his IP address  and show it to you . 
- if he trying hard to get access of your site or hack your site .. then you can  block his IP Address ..

<!--* Configuration in -->
    
--> GO to project folder just add this ``` 'admin_honeypot', ``` to settings.py installed apps.
--> Go to project folder and create a new path in urls.py named
``` path('admin/',include('admin_honeypot.urls', namespace='admin_honeypot')), ```



<!--* ===================================================================== -->

<!-- one more feature i have to add ...  -->
# if we stay inactive for too long time then it will logout us automatically.
--> we have to install a package called
``` pip install django-session-timeout ```
--> This we have to add in settings.py > middleware
    'django_session_timeout.middleware.SessionTimeoutMiddleware',
``` 'django_session_timeout.middleware.SessionTimeoutMiddleware', ```
--> This we have to add anywhere in settings.py 
``` SESSION_EXPIRE_SECONDS = 3600 ```
# 3600 for 1 hour , 60 for 1 min
# after 1hr it will automatically log you out.
``` SESSION_EXPIRE_AFTER_LAST_ACTIVITY = True ```
--> after logout it will go to this page
``` SESSION_TIMEOUT_REDIRECT = 'accounts/signin' ```
