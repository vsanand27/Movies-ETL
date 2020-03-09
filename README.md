# Movies-ETL
Download movies for Data Wrangling

# Background
Amazing Prime loves the dataset and wants to keep it updated on a daily basis. Britta needs to create an automated pipeline that takes in new data, performs the appropriate transformations, and loads the data into existing tables.

Link to file: 

# Purpose
1)	Develop Python script utilizing Jupyter notebook that performs all three ETL steps: 
      a.	Wikipedia
      b.	Kaggle data
      c.	Rating data

2)	Adding try-except blocks will make the automated ETL script more robust to handle potentially unforeseen errors due to changes in the underlying data.

3)	Extract, Clean, and transform the data automatically utilizing ETL function.

4)	Export new data into PostgreSQL.

# Assumptions

# As we embarked down the journey to develop ETL function, we assumed the following:

  1)	For Simplification, we developed 3 global functions: Weki, Kagel, and Rate: a) Note: the functions only work when ETL function passes parameter through, b) Having global functions to call upon results in easy maintenance without touching other parts of code and preventing further breakdown of code.

2)	To help ease of use and troubleshooting, all the 3 functions are equipped with Try-Except blocks
 
           a All Try Except statement prints two message: first section of code and second error message  

            b. Wiki function: Try Except are in the following sections that are more prone to errors, Re-naming column name, duplicate rows, columns w/ 90% of values missing, box office in dollars, budget, Date, and Run time

            c. Kagel function: Try Except statements are used when removing bad data and Changing data types

            d. Rate function: Try Except statements are used for date time stamp conversions
  
3)	ETL main function: is where all the activities Extract, Clean, transform, and Export takes place:
      a.	3 parameters are passed to ETL function that provides them path to each of the files
      b.	The three function called upon within ETL function to  Extract, Clean, and transform the datasets.  
      c.	The movie data-frame is developed with-in the ETL function
      d.	Columns with missing data are dropped ie. video
      e.	Movie dataset is re-ordered and the columns re-named
      f.	Rating count is calculated and dataframes are build to merge pivot
      g.	Lastly, cleaned data is put forth in 3 objects: a) movie_df, rating_counts, and movies with rating dataframe is extract.

4)	The data frames within ETL function are then imported into pgAdmin 4 where they are stored in tables utilizing SQL

