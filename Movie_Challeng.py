#Import Dependencies
import json
import pandas as pd
import numpy as np
import re

file_dir ='C:/Users/vick_/Desktop/Data Analytics Projects/Movies-ETL'

movies_json=f'{file_dir}/wikipedia.movies.json'

def wiki(movies_json):
    with open(movies_json, mode='r') as file:
        wiki_movies_raw = json.load(file)

    # wiki_movies_df=pd.DataFrame(wiki_movies_raw)

    wiki_movies = [movie for movie in             wiki_movies_raw
               if ('Director' in movie or 'Directed by' in movie)
                   and 'imdb_link' in movie
                   and 'No. of episodes' not in movie]

    # wiki_movie_df=pd.DataFrame(wiki_movies)

    def clean_movie(movie):
        movie = dict(movie) #create a non-destructive copy
        alt_titles = {}
        # combine alternate titles into one list
        for key in ['Also known as','Arabic','Cantonese','Chinese','French',
                    'Hangul','Hebrew','Hepburn','Japanese','Literally',
                    'Mandarin','McCune-Reischauer','Original title','Polish',
                    'Revised Romanization','Romanized','Russian',
                    'Simplified','Traditional','Yiddish']:
            if key in movie:
                alt_titles[key] = movie[key]
                movie.pop(key)
        if len(alt_titles) > 0:
            movie['alt_titles'] = alt_titles

        # merge column names
        def change_column_name(old_name, new_name):
            if old_name in movie:
                movie[new_name] = movie.pop(old_name)
        change_column_name('Adaptation by', 'Writer(s)')
        change_column_name('Country of origin', 'Country')
        change_column_name('Directed by', 'Director')
        change_column_name('Distributed by', 'Distributor')
        change_column_name('Edited by', 'Editor(s)')
        change_column_name('Length', 'Running time')
        change_column_name('Original release', 'Release date')
        change_column_name('Music by', 'Composer(s)')
        change_column_name('Produced by', 'Producer(s)')
        change_column_name('Producer', 'Producer(s)')
        change_column_name('Productioncompanies ', 'Production company(s)')
        change_column_name('Productioncompany ', 'Production company(s)')
        change_column_name('Released', 'Release Date')
        change_column_name('Release Date', 'Release date')
        change_column_name('Screen story by', 'Writer(s)')
        change_column_name('Screenplay by', 'Writer(s)')
        change_column_name('Story by', 'Writer(s)')
        change_column_name('Theme music composer', 'Composer(s)')
        change_column_name('Written by', 'Writer(s)')

        return movie
    
    clean_movies = [clean_movie(movie) for movie in wiki_movies]
    wiki_movies_df = pd.DataFrame(clean_movies)

    # STEP 1 REMOVE DUPLICATE ROWS
    wiki_movies_df['imdb_id'] = wiki_movies_df['imdb_link'].str.extract(r'(tt\d{7})')

    wiki_movies_df.drop_duplicates(subset='imdb_id', inplace=True)

    wiki_columns_to_keep = [column for column in wiki_movies_df.columns if wiki_movies_df[column].isnull().sum() < len(wiki_movies_df) * 0.9]
    
    wiki_movies_df = wiki_movies_df[wiki_columns_to_keep]

    

    # STEP 2: CHANGING DATA TYPES
    box_office = wiki_movies_df['Box office'].dropna() 

    box_office = box_office.apply(lambda x: ' '.join(x) if type(x) == list else x)

    # Change dollar signs
    try:
        form_one = r'\$\s*\d+\.?\d*\s*[mb]illi?on'
        form_two = r'\$\s*\d{1,3}(?:[,\.]\d{3})+(?!\s[mb]illion)'
        box_office = box_office.str.replace(r'\$.*[-—–](?![a-z])', '$', regex=True)

        def parse_dollars(s):
            # if s is not a string, return NaN
            if type(s) != str:
                return np.nan

            # if input is of the form $###.# million
            if re.match(r'\$\s*\d+\.?\d*\s*milli?on', s, flags=re.IGNORECASE):

                # remove dollar sign and " million"
                s = re.sub(r'\$|\s|[a-zA-Z]','', s)

                # convert to float and multiply by a million
                value = float(s) * 10**6

                # return value
                return value

            # if input is of the form $###.# billion
            elif re.match(r'\$\s*\d+\.?\d*\s*billi?on', s, flags=re.IGNORECASE):

                # remove dollar sign and " billion"
                s = re.sub('\$|\s|[a-zA-Z]','', s)

                # convert to float and multiply by a billion
                value = float(s) * 10**9

                # return value
                return value

            # if input is of the form $###,###,###
            elif re.match(r'\$\s*\d{1,3}(?:[,\.]\d{3})+(?!\s[mb]illion)', s, flags=re.IGNORECASE):

                # remove dollar sign and commas
                s = re.sub('\$|,','', s)

                # convert to float
                value = float(s)

                # return value
                return value

            # otherwise, return NaN
            else:
                return np.nan

        wiki_movies_df['box_office'] = box_office.str.extract(f'({form_one}|{form_two})', flags=re.IGNORECASE)[0].apply(parse_dollars)
    
    except:
        print(f'check error - for dollar conversion')
        
        print(box_office[~matches_form_one & ~matches_form_two])
    
     #Parsing the budget
    
     #1 Create a budget variable with the following code:
    budget = wiki_movies_df['Budget'].dropna()

    budget = budget.map(lambda x: ' '.join(x) if type(x) == list else x)

    budget = budget.str.replace(r'\$.*[-—–](?![a-z])', '$', regex=True)

    matches_form_one = budget.str.contains(form_one, flags=re.IGNORECASE)
    matches_form_two = budget.str.contains(form_two, flags=re.IGNORECASE)


     #return wiki_movie_df to put in post gress


#def kagel():
    #kaggle_metadata = pd.read_csv(f'{file_dir}/#movies_metadata.csv',low_memory=False)
    #ratings = pd.read_csv(f'{file_dir}/ratings.#csv')

    

# Pushing