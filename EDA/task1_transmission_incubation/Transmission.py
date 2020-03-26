import spacy
import pandas as pd
import os
import json
import matplotlib.pyplot as plt
import matplotlib.style as style
from spacy.matcher import Matcher

from tqdm import tqdm


def transmission(df):
    style.use('seaborn-poster')
    style.use('ggplot')

    if not os.path.exists('Data/pickles/transmission_pickle'):
        transmit_keywords = ['transmit', 'transmission']
        findings = dict()
        paper_id_tracker = set()
        temp_papers = list()

        transmission_papers = pd.DataFrame(columns=['paper_id', 'title', 'abstract', 'body'])
        body_text = df['body'].values

        nlp = spacy.load("en_core_web_sm", disable=['ner', 'parser'])
        nlp.add_pipe(nlp.create_pipe('sentencizer'))
        matcher = Matcher(nlp.vocab)

        for i in transmit_keywords:
            matcher.add(i, build_transmission_pattern(i))

        index = 0
        for i in tqdm(body_text):
            spacy.prefer_gpu()
            texts = i.split('.')
            for docs in nlp.pipe(texts, disable=['parser', 'ner', 'entity_linker']):
                for match_id, start, end in matcher(docs):
                    if df.loc[index]['paper_id'] not in paper_id_tracker:
                        paper_id_tracker.add(df.loc[index]['paper_id'])
                        temp_papers.append([df.loc[index]['paper_id'], df.loc[index]['title'], df.loc[index]['abstract'], df.loc[index]['body']])
                    if str(docs[start:end]) in findings:
                        findings[str(docs[start:end]).lower()] += 1
                    else:
                        findings[str(docs[start:end]).lower()] = 1
            index += 1

        with open('Data/pickles/transmission_count', 'w') as data:
            json.dumps(findings, data)

        for i in temp_papers:
            transmission_papers = pd.concat([transmission_papers, pd.DataFrame([[i[0], i[1], i[2], i[3]]],
                                                                               columns=['paper_id', 'title', 'abstract',
                                                                                        'body'])])

        transmission_papers.to_pickle('Data/pickles/transmission_pickle')
    else:

        transmission_techniques = ['aerosol', 'contact', 'surface', 'breathing']

        transmission_papers = pd.read_pickle('Data/pickles/transmission_pickle')

        transmission_medium_freq = list()

        for x in tqdm(transmission_papers['body']):
            for sent in x.split('. '):
                if 'transmission' in sent:
                    for type in transmission_techniques:
                        if type in sent:
                            transmission_medium_freq.append(type)

        transmission_papers.head()
        freq_list = list()

        with open('Data/pickles/transmission_count', 'r') as data:
            findings = json.load(data)

        for i in findings:
            for x in range(0, findings[i]):
                freq_list.append(i)

        findings_df = pd.DataFrame(freq_list, columns=['variation'])
        transmission_mediums_df = pd.DataFrame(transmission_medium_freq, columns=['medium'])
        print(transmission_mediums_df['medium'].value_counts())
        colors = ['#51c4e9', '#4a47a3', '#ad62aa', '#eab9c9']
        plt.pie(transmission_mediums_df['medium'].value_counts(),
                labels=[i.capitalize() for i in transmission_mediums_df['medium'].value_counts().index],
                autopct='%1.1f%%', startangle=90, shadow=True, textprops={'fontsize': 15}, colors=colors)

        plt.title("Common Transmission Mediums Mentioned", fontsize=25)
        plt.savefig('Charts/TransmissionMediums.png')
        plt.show()

        test = findings_df['variation'].value_counts()
        test['test'] = range(0,7)
'''
        plt.hist(freq_list, bins=5, histtype='bar',
                 ec='white', linewidth=1.2, color='#005082')
        plt.title('Word Frequency from NLP on COVID-19 Scientific Literature', fontsize=21)
        plt.xticks(range(0, len(findings)),
                   sorted(map(lambda x:x.capitalize(),list(findings.keys()))),
                   rotation=25)
        plt.xlabel('Different Variations of "Transmission" in COVID-19 Literature',
                   fontsize=20, color='black')
        plt.ylabel('Frequency',
                   fontsize=20, color='black')
        plt.savefig('Charts/TransmissionFreq')
        plt.show()
'''

def build_transmission_pattern(keyword):
    return [[{'LEMMA': keyword.lower()}]]
