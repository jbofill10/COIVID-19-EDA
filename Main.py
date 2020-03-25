import json
import os
import pandas as pd

from tqdm import tqdm

from EDA import task1_index as task1


def main():
    # Not interested in loading a large DataFrame every time, so I only have it run once if the pickle doesn't exist
    if not os.path.exists('Data/pickles/covid_pickle'):
        print('Generating pickle...')
        df = pd.DataFrame(columns=['title', 'abstract', 'body'])
        root = 'Data/CORD-19-research-challenge/'
        file_paths = list()
        for path, dirs, files in os.walk(root):
            dirs[:] = [d for d in dirs if d not in 'extras']
            for name in files:
                file_paths.append(os.path.join(path, name))

        for path in tqdm(file_paths):
            full_abstract = ''
            full_body = ''
            with open(path, 'r') as file:
                data = json.load(file)
                title = data['metadata']['title']
                for x in data['abstract']:
                    abstract = x['text']
                    full_abstract += abstract

                for x in data['body_text']:
                    body = x['text']
                    full_body += body

            temp = pd.DataFrame([[title, full_abstract, full_body]], columns=['title', 'abstract', 'body'])
            df = df.append(temp)

        df = df.reset_index()
        print('Saving DataFrame so you don\'t need to create it again!')
        df.to_pickle('Data/pickles/covid_pickle')
    else:
        df = pd.read_pickle('Data/pickles/covid_pickle')

    task1.task_1(df)


if __name__ == '__main__':
    main()
