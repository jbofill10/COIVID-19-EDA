import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style


def incubation(df):
    style.use('seaborn-poster')
    style.use('ggplot')
    # I'm thinking of looking for strings with incubation to start
    incubation_occurrences = list()

    body_text = df['body'].values
    counter = 0
    for text in body_text:
        for sent in text.split('. '):
            if 'incubation' in sent:
                temp = re.findall('[1-9]{1,2}\S*\sday|s$', sent)
                if len(temp) > 0:
                    for find in temp:
                        find = re.sub('\D', ' ', find)
                        house = find.strip().split(' ')
                        for nums in house:
                            try:
                                incubation_occurrences.append(int(nums))
                            except:
                                continue

    print(len(incubation_occurrences))
    print(counter)

    incubation_df = pd.DataFrame({'days': incubation_occurrences}, index=range(0, len(incubation_occurrences)))
    incubation_df = incubation_df.sort_index()

    print(int(round(incubation_df['days'].mean())))

    plt.hist(incubation_df['days'].value_counts(), bins=75, color='purple')
    plt.xlabel("Incubation Time in Days", fontsize=20, color='black')
    plt.ylabel('Frequency Found in Literature', fontsize=20, color='black')
    plt.title('Distribution of Incubation Periods', fontsize=23, color='black')
    plt.xlim(1, 62)
    plt.rcParams['axes.grid'] = True
    plt.savefig('Charts/IncubHist')
    plt.show()
