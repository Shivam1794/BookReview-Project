README.md

# BookReview Recommendation

Using this repository code, we are building an ML model which would recommend the books based on provided book and its details.


## Details

Overall following are the steps involved :

1. Data Gathering : We'll fetch the data from online available resources and store them in PostgreSQL Database

2. Insert the fetched data into PostgreSQL Database under tables named as "Books" and "Review"

3. Create a Machine Learning Recommendation System using Cosine Similarity to fetch the recommendations

4. Create a test dataset and find the recommendations for the books in test dataset

5. Deploy Endpoints for direct access to Get/Update Books and their details or to Delete books from the PostgreSQL Database
## config.py

This file contains the configuration setup to connect Python to PostgreSQL Database

**Changes required in this file for further usage:**

Create a seperate **database.ini** file with below content in it:
**************************
[postgresql]

host=localhost -> your hostname

database=bookreview -> Database Name

user=postgres -> Your User Name

password= **** -> Your password

*********************************

## PostgreSQL.py

This Python file includes the steps:
1. Data Fetching : We are scraping data from various online sources. 
Following were the resources used: 
- Openlibrary.org
- goodreads.com
- GoogleBooks

2. Inserting the fetched records into PostgreSQL Database
**Note:** Please install and setup PostgreSQL before performing this step.

**Changes to be done in this file to further use:**
1. Change key=***xyz*** to your key in googleapis.com url
2. User-Agent as required (mostly not required for Windows)
## ML_Model.py

This is the Python file which is building the recommendation system for the books fetched.

**Input** 

We need a Dataframe with all books and its details which we are extracting from the PostgreSQL database

**Methodology Used:**

We are computing the **cosine similarity matrix** based on features :
- summary of book
- genre of book 
- average rating of book

To encorporate embedding of *summary* feature in our similarity matrix, I have used Word2Vec model however TF-IDF (not recommended) or Glove could also be used. 

**Output**

The final output we get comprises of a Table structured Dataframe consisting of all Books and their corresponding recommended books 

***************************
***************************


At the end we also have a section where we can try testing with new books as test dataset and it will provide the recommendation based on the books our model is trained on.

The last cell of this Jupyter notebook contains code to pickle the model for further usage wherever required -> we'll be using it in our flask_api.py file

## flask_api.py

This Python file defines the endpoints which can be used to fetch data from table, update book records, delete book records, see the recommendations etc.

**Note:** 

To use POST/PUT endpoint functionality please use below format in BODY section of tool you are using. I used POSTMAN to test the endpoints.

Following is the body part:

{

  "title": "Under the Greenwood Tree or, The Mellstock quire",

  "author": "Thomas Hardy",

  "genre": "Fiction",

  "year_published": 1929,

  "summary": "1929 repr, a rural painting of the dutch school with a map of wessex, calf, co., hardy, leather, macmillan &, macmillan’, or, s pocket library, the mellstock quire, the wessex novels, thomas hardy, thomas literature, under the greenwood tree"
  
}

********************

**Changes to be done in this file to further use:**

1. Change the username, password, host and database name in app.config command (line 8)
2. Change the pickle file name (line 29) based on the file name which was used in last cell in ML_Model.py file
# Deployment

### Docker File Creation Step:

1. Create a Dockerfile
2. Based on OS, select the appropriate base image -> This will contain the Operating System and some other pre-installed packages.
3. In working directory copy the requirement.txt and then install those dependencies
4. Copy rest of the application code into the container
5. Define command that will 
6. Now run the docker image locally or push it on dockerhub or AWSrun the application
6. Name the image (app_image_name)
7. Run Docker container
docker run -d -p 8080:80 app_image_name

### CI/CD Workflow setup

1. Create a GitHub actions workflow which will trigger on any push/pull request to/from main branch
2. Check out code from GitHub repo
3. Install dependencies
4. Run Unit tests
5. Build Docker image using "Dockerfile" explained above
6. Now run the docker image locally or push it on dockerhub or on AWS server (EC2)