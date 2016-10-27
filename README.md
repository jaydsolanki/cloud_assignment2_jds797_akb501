# Cloud Computing: Assignment 1 Tweet Map

### Group Members

|Net ID | Name|
|----|----|
|jds797|Jay Dharmendra Solanki|
|akb501|Aniket Krishna Bhandarkar|


<p> This is the Assignment for the course Cloud Computing at NYU Tandon school of Engineering </p>
<p> This Assignment is in Python. There are 3 modules in the project:</p>

  1. Web Application which is scaled by deploying it to AWS ElasticBeanstalk in Django Framework
  2. AWS Elastic Search for finding text quickly
  3. Python code to add tweets in the AWS Elastic Search in Real Time
  
<p> Following are the dependecies for Web Application </p>

  1. Django Framework
    * Install using `pip install django`
  2. wheel
    * Install using `pip install wheel`
  3. certifi
    * Install using `pip install certifi`
  4. elastic search
    * Download the Elasticsearch executable to run locally. To run on AWS ElasticBeanstalk or EC2, start an AWS Elastic Search Cluster on AWS
    * Install using `pip install elasticsearch`
  5. Google Maps Javascript API
    * Get from `https://developers.google.com/maps/documentation/javascript/`
  6. Bootstrap
    * Get from `http://getbootstrap.com/`
  7. jQuery v1.x
    * Get from `https://code.jquery.com/` by selection `jQuery 1.x`
    
<p> To get started with the application there are some steps to be followed </p>
  1. Download/Clone the project
  2. Run 
     * `python manage.py migrate`
  3. Make sure you have stated ElasticSearch service at localhost or at AWS. If you run on AWS make sure to get the url for accessing the elastic search. Then run
     * `python populate_index.py <index_name> <host for elasticsearch>`
     where replace `<index_name>` with the name of the index you want to create and 
     replace `<host for elasticsearch>` with the Elastic Search Host url (pass an empty string ("") for localhost)
     This may take a while and after that your Elasticsearch index will be created and populated
  4. Open `Assignment1/settings.py` and change the variables `INDEX_NAME` and `HOST_NAME` as per your configuration
  5. To run it locally, run
     *`python manage.py runserver`
     The web appication will be accesible from `localhost:8000`
     <br> To run on ElasticBeanstalk make sure you have installed EB cli. Follow the steps from `http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html#python-django-deploy`.
     1. `eb init -p python2.7 cloud-assignment`
     2. `eb init`
     3. `eb create django-env`
     4. `eb open` <br/>
     After the above steps the website will open
  6. For live tweets make sure you have your own Twitter
     1. `consumer_key`
     2. `consumer_secret`
     3. `access_token`
     4. `access_toekn_secret`<br/>
     You can get it from from `https://apps.twitter.com/`
     Once you have the credentials. Start an EC2 server and make a cronjob for 
     * `python live_elastic_search.py <index_name> <host of elastic search>`<br/>
     to run it with the index name and host of elastic search, it will populate the index in real time and the web application will use the indexed data
     
### Features

<p>This project gives 2 search functionalities</p>
  1. Search tweets for speicific keywords and visualize on a World Map
  2. Click on Map to get a location and search tweets within 'N' KMs from that selected point using `geo_spatial` search
  
### Output
##### Home Page
![alt tag](https://github.com/jaydsolanki/cloud_assignment_jds797_akb501/blob/master/Screenshots/02_HomePage.png)

##### AWS Elastic Search
![alt tag](https://github.com/jaydsolanki/cloud_assignment_jds797_akb501/blob/master/Screenshots/01_elasticsearch_aws.png)

##### Keyword Search Output
![alt tag](https://github.com/jaydsolanki/cloud_assignment_jds797_akb501/blob/master/Screenshots/06_Query.png)

##### GeoSearch Query
<p> The green marker is what User Selected and the distance will be calculated from the green marker </p>
![alt tag](https://github.com/jaydsolanki/cloud_assignment_jds797_akb501/blob/master/Screenshots/04_geo_search.png)
    
##### GeoSearch Query Output
![alt tag](https://github.com/jaydsolanki/cloud_assignment_jds797_akb501/blob/master/Screenshots/05_geosearc_result.png)

##### EC2 instance for running Live Tweet input 
![alt tag](https://github.com/jaydsolanki/cloud_assignment_jds797_akb501/blob/master/Screenshots/08_ec2_instance_for_live_data.png)

##### Elastic Beanstalk used
![alt tag](https://github.com/jaydsolanki/cloud_assignment_jds797_akb501/blob/master/Screenshots/07_elastic_beanstalk.png)

<br>

### Url for the Project on Beanstalk: `http://django-env.m3txbp3s2c.us-west-2.elasticbeanstalk.com/`
