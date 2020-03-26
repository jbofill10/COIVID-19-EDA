from tqdm import tqdm

import matplotlib.style as style
import matplotlib.pyplot as plt
import pandas as pd
import os
import seaborn as sns


def symptoms(df):
    if not os.path.exists('Data/pickles/symptoms_pickle'):
        common_symptoms = ['fever', 'chills', 'cough', 'sore throat',
                           'runny nose', 'headache', 'fatigue', 'vomiting',
                           'shortness of breath', 'dizziness']

        text = df['body'].values

        symptom_freq = list()

        for x in tqdm(text):
            for sent in x.split('.'):
                for symp in common_symptoms:
                    if symp in sent:
                        symptom_freq.append(symp)

        symptoms_df = pd.DataFrame(symptom_freq, columns=['symptom'])
        symptoms_df.to_pickle('Data/pickles/symptoms_pickle')

    else:
        symptoms_df = pd.read_pickle('Data/pickles/symptoms_pickle')
    symp_vals = symptoms_df['symptom'].value_counts().sort_values()

    plt.figure(figsize=(21, 10))
    sns.set(style="darkgrid")
    sns.barplot(x=symp_vals.values, y=list(range(0, len(symp_vals.index))), orient='h', palette='Spectral')
    plt.yticks(list(range(0, len(symp_vals.index))), [i.capitalize() for i in symp_vals.index], fontsize=15)
    plt.xlabel('Times Mentioned in Literature', fontsize=20)
    plt.xticks(fontsize=15)
    plt.ylabel('Symptoms', fontsize=20)
    plt.title('Common Symptoms Flu found in COVID-19 Literature', fontsize=22)
    plt.savefig('Charts/corona_symptoms.png')
    plt.show()
