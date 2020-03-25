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
    
    for text in body_text:
        for sent in text.split('. '):
            if 'incubation' in sent:
                temp = re.findall('\d[1-9]{1,2}\sday', sent)
                if len(temp) > 0:
                    for find in temp:
                        incubation_occurrences.append(find[0:find.index(' ')])

    incubation_df = pd.DataFrame({'days':incubation_occurrences}, index=range(0,len(incubation_occurrences)))
    incubation_df=incubation_df.sort_index()
    
    print(incubation_df['days'].value_counts().sort_index())
    
    
    plt.hist(incubation_df['days'].value_counts(), bins=50)
    plt.xlabel("Incubation Time in Days")
    plt.xlim(0,96)
    plt.ylabel("")
    plt.show()