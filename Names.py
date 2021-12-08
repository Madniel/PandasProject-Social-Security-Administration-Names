import matplotlib.pyplot as plt
import numpy as np
import sqlite3
import pandas as pd
years = range(1880, 2020)

def check(tab, year):
    years = tab.index.tolist()
    if year in years:
        return str(int(tab.loc[year]['number']))
    else:
        return str(0)

def calculate_survive(df,df_2,years_live):
    df_2 = pd.pivot_table(df_2, values=['lx', 'dx'], index=['Year', 'Age'], aggfunc=np.sum)
    df_2 = df_2.reset_index().set_index('Year')
    df_2 = df_2.loc[1959:2017 - years_live]
    live = pd.pivot_table(df, values=['number'], index=['year'], aggfunc=np.sum)
    live = live.loc[1959:2017 - years_live]

    sum = np.zeros(len(df_2.loc[df_2['Age'] == 0, 'dx']))
    for year_live in range(years_live):
        temp = df_2.loc[df_2['Age'] == year_live, 'dx'].to_numpy()
        sum = sum + temp
    live['pn'] = live['number'] - sum
    live['survive'] = live['pn'] / live['number']
    return live

def zad1():
    pieces = []
    for year in years:
        columns = ['name', 'sex', 'number']
        path = 'names/yob{}.txt'.format(year)
        df = pd.read_csv(path, names=columns)
        df['year'] = year
        pieces.append(df)
    df = pd.concat(pieces, ignore_index=True)
    print(df)
    return df

def zad2(df):
    df = pd.pivot_table(df, values='number', index=['name'], aggfunc=np.sum)
    print(f'Różnych (unikalnych) imion zostało nadane w tym czasie {len(df)}.')

def zad3(df):
    df = pd.pivot_table(df, values='number', index=['sex', 'name'], aggfunc=np.sum)
    F = len(df.loc[['F'], :])
    M = len(df.loc[['M'], :])
    print(f'Różnych (unikalnych) imion damskich zostało nadane w tym czasie {F}.')
    print(f'Różnych (unikalnych) imion męskich zostało nadane w tym czasie {M}.')

def zad4(df):
    frequency = df.pivot_table(values='number', index=['year'], columns=['sex'], aggfunc=sum)

    frequency_male = []
    frequency_female = []
    df['frequency_male'] = 0
    df['frequency_female'] = 0

    for year in years:
        size_f = frequency['F'][year]
        size_m = frequency['M'][year]
        year_cut = df.loc[(df["year"] == year) & (df["sex"] == 'F'), :]
        frequency_female.append(((year_cut['number']) / size_f).to_numpy())
        year_cut = df.loc[(df["year"] == year) & (df["sex"] == 'M'), :]
        frequency_male.append(((year_cut['number']) / size_m).to_numpy())

    frequency_male = [item for sublist in frequency_male for item in sublist]
    frequency_female = [item for sublist in frequency_female for item in sublist]
    df.loc[(df["sex"] == 'F'), 'frequency_female'] = frequency_female
    df.loc[(df["sex"] == 'M'), 'frequency_male'] = frequency_male
    print(df)
    return df

def zad5(df):
    frequency = df.pivot_table(values='number', index=['year'], columns=['sex'], aggfunc=sum)
    frequency['ratio'] = frequency['F'] / frequency['M']
    sum_of_births = df.pivot_table(values='number', index=['year'], aggfunc=sum)

    fig, ax = plt.subplots(2, 1)
    ax[0].plot(sum_of_births)
    ax[0].set_title('Liczba urodzin na przestrzeni lat', fontsize=12)

    ax[1].plot(frequency['ratio'], 'r')
    ax[1].set_title('Stosunek liczby narodzin dziewczynek do liczby narodzin chłopców', fontsize=12)

    print(
        f'W roku {frequency.ratio.idxmin()} zanotowano najmniejszą różnicę w liczbie urodzeń między chłopcami a dziewczynkami')
    print(
        f'W roku {frequency.ratio.idxmax()} zanotowano największą różnicę w liczbie urodzeń między chłopcami a dziewczynkami')

def zad6(df):
    top_female = []
    top_male = []

    for year in years:
        year_cut = df.loc[(df["year"] == year) & (df["sex"] == 'F'), :].sort_values(by=['number'], ascending=False)
        top_female.append(year_cut.head(1000))

        year_cut = df.loc[(df["year"] == year) & (df["sex"] == 'M'), :].sort_values(by=['number'], ascending=False)
        top_male.append(year_cut.head(1000))

    top_female = pd.concat(top_female, ignore_index=True)
    top_female = pd.pivot_table(top_female, values='number', index=['name'], aggfunc=np.sum)

    top_male = pd.concat(top_male, ignore_index=True)
    top_male = pd.pivot_table(top_male, values='number', index=['name'], aggfunc=np.sum)

    top_female = top_female.sort_values(by=['number'], ascending=False)
    top_male = top_male.sort_values(by=['number'], ascending=False)

    print('Top 1000 najpopularniejszych imion dla dziewczynek')
    print(top_male.head(1000))

    print('Top 1000 najpopularniejszych imion dla chłopców')
    print(top_female.head(1000))

    return top_male , top_female

def zad7(df, top_male, top_female):
    list_top_male = top_male.index.tolist()
    list_top_female = top_female.index.tolist()

    harry = df.loc[(df["name"] == 'Harry') & (df["sex"] == 'M') ,['frequency_male', 'number','year']]
    james = df.loc[(df["name"] == list_top_male[0]) & (df["sex"] == 'M'), ['frequency_male', 'number', 'year']]
    marilin = df.loc[(df["name"] == 'Marilin') & (df["sex"] == 'F') ,['frequency_female', 'number','year']]
    mary = df.loc[(df["name"] == list_top_female[0]) & (df["sex"] == 'F'), ['frequency_female', 'number', 'year']]

    harry.set_index('year', inplace = True)
    marilin.set_index('year', inplace=True)
    james.set_index('year', inplace=True)
    mary.set_index('year', inplace=True)

    fig, ax = plt.subplots()
    ax.plot(harry['number'],label='Harry')
    ax.plot(james['number'],label=f'{list_top_male[0]}')
    ax.plot(mary['number'], label=f'{list_top_female[0]}')
    ax.plot(marilin['number'],label='Marilin')
    ax.set_ylabel('Liczba osób z nadanym imieniem', fontsize=12)
    ax.legend(loc='upper right')

    print(f'Liczba imion z imieniem Harry wynosiła w: \n 1940: '
          + check(harry,1940) + '\n 1980: '
          + check(harry,1980) + '\n 2019: '
          + check(harry,2019))

    print(f'Liczba imion z imieniem James wynosiła w: \n 1940: '
          + check(james,1940) + '\n 1980: '
          + check(james,1980) + '\n 2019: '
          + check(james,2019))

    print(f'Liczba imion z imieniem Mary wynosiła w: \n 1940: '
          + check(mary,1940) + '\n 1980: '
          + check(mary,1980) + '\n 2019: '
          + check(mary,2019))

    print(f'Liczba imion z imieniem Marilin wynosiła w: \n 1940: '
          + check(marilin,1940) + '\n 1980: '
          + check(marilin,1980) + '\n 2019: '
          + check(marilin,2019))

    ax1 = ax.twinx()
    ax1.plot(harry['frequency_male'],':', label='Harry')
    ax1.plot(james['frequency_male'],':', label=f'{list_top_male[0]}')
    ax1.plot(mary['frequency_female'],':', label=f'{list_top_female[0]}')
    ax1.plot(marilin['frequency_female'],':', label='Marilin')
    ax1.set_ylabel("Popularność Imion (linia kropkowana)", fontsize=12)
    ax1.legend(loc='right')

def zad8(df, top_male, top_female):
    top_names_male= top_male.head(1000).index.tolist()
    top_names_female = top_female.head(1000).index.tolist()
    df = df.set_index('name')

    names_m = df.loc[top_names_male,['number','sex','year']].set_index('year')
    names_m = names_m.loc[names_m['sex']=='M']

    names_f = df.loc[top_names_female, ['number', 'sex', 'year']].set_index('year')
    names_f = names_f.loc[names_f['sex']=='F']

    names_m = names_m.pivot_table(values='number', index=['year'], aggfunc=sum)
    names_f = names_f.pivot_table(values='number', index=['year'], aggfunc=sum)

    total_births = pd.pivot_table(df, values='number', index=['year'], columns=['sex'], aggfunc=sum)
    total_births_male = names_m['number']/total_births['M']
    total_births_female = names_f['number']/total_births['F']

    fig, ax = plt.subplots()
    ax.plot(total_births_male, label='Mężczyźni')
    ax.plot(total_births_female, label='Kobiety')
    ax.set_title('Różnorodność imion na przestrzeni lat', fontsize=12)
    ax.legend()
    diffrence = abs(total_births_male - total_births_female)
    print(f'Największą różnicę w różnorodności między imionami męskimi a żeńskimi zaobserwowano w roku {diffrence.idxmax()}')

def zad9(df):
    last_letter = []
    for name in df['name']:
        last_letter.append(name[-1])
    df['last letter'] = last_letter
    df_agregate = df.pivot_table(values='number', index=['year','sex', 'last letter'], aggfunc=sum)
    lista = [1910, 1960, 2015]
    df_agregate_cut=df_agregate.loc[lista]

    total_births = pd.pivot_table(df, values='number', index=['year'], columns=['sex'], aggfunc=sum)
    df_agregate_cut['normalize'] = 0

    df_agregate_cut = df_agregate_cut.reset_index()
    for year in lista:
        df_agregate_cut.loc[(df_agregate_cut['sex']=='M') & (df_agregate_cut['year']==year), 'normalize'] = df_agregate_cut.loc[(df_agregate_cut['sex']=='M') & (df_agregate_cut['year']==year),'number'] / total_births.loc[year,'M']
        df_agregate_cut.loc[(df_agregate_cut['sex']=='F') & (df_agregate_cut['year']==year), 'normalize'] = df_agregate_cut.loc[(df_agregate_cut['sex']=='F') & (df_agregate_cut['year']==year), 'number'] / total_births.loc[year,'F']

    df_agregate_cut = df_agregate_cut.set_index('year')
    df_agregate_cut = df_agregate_cut.loc[df_agregate_cut['sex'] == 'M', ['last letter', 'normalize']]


    a = ord('a')
    alph = [chr(i) for i in range(a, a + 26)]
    x = np.arange(len(alph))

    last_letter_1910 = df_agregate_cut.loc[1910, :]
    letters_1910 = last_letter_1910['last letter'].tolist()
    last_letter_1910 = last_letter_1910['normalize'].tolist()

    indexes= [i for i, item in enumerate(alph) if not item in letters_1910]
    for index in indexes:
        last_letter_1910.insert(index, 0)


    last_letter_1960 = df_agregate_cut.loc[1960, :]
    letters_1960 = last_letter_1960['last letter'].tolist()
    last_letter_1960 = last_letter_1960['normalize'].tolist()
    indexes = [i for i, item in enumerate(alph) if not item in letters_1960]
    for index in indexes:
        last_letter_1960.insert(index, 0)

    last_letter_2015 = df_agregate_cut.loc[2015, :]
    letters_2015 = last_letter_2015['last letter'].tolist()
    last_letter_2015 = last_letter_2015['normalize'].tolist()
    indexes = [i for i, item in enumerate(alph) if not item in letters_2015]
    for index in indexes:
        last_letter_2015.insert(index, 0)

    fig, ax = plt.subplots()
    width = 0.3
    ax.bar(x - width, last_letter_1910, width, label='1910')
    ax.bar(x, last_letter_1960, width, label='1960')
    ax.bar(x + width, last_letter_2015, width, label='2015')
    ax.set_xticks(x)
    ax.set_xticklabels(alph)
    ax.set_title('Popularności ostatniej litery dla mężczyzn', fontsize=12)
    ax.legend()

    df_agregate_cut = df_agregate_cut.reset_index()
    df_agregate_cut = df_agregate_cut.pivot_table(values='normalize', index=['year', 'last letter'], aggfunc=sum).sort_index(ascending=True)
    last_letter_1910 = df_agregate_cut.loc[1910, :]
    last_letter_2015 = df_agregate_cut.loc[2015, :]
    change=abs(last_letter_1910['normalize']-last_letter_2015['normalize'])/last_letter_2015['normalize']
    last_letter_1910['Change']=change
    last_letter_1910=last_letter_1910.sort_values(by=['Change'], ascending=False)
    last_letter_1910=last_letter_1910.head(3)
    last_letter_trend = last_letter_1910.index.tolist()
    print(f'Największy wzrost/spadek między rokiem 1910 a 2015 nastąpił dla \'{last_letter_trend[0]}\'')

    df_agregate['normalize'] = 0
    df_agregate = df_agregate.reset_index()
    df_agregate = df_agregate.set_index('year')
    df_agregate = df_agregate.loc[df_agregate['sex'] == 'M']
    df_agregate['normalize'] = df_agregate['number'] / total_births['M']

    y1 = df_agregate.loc[df_agregate['last letter']==last_letter_trend[0],'normalize']
    y2 = df_agregate.loc[df_agregate['last letter'] == last_letter_trend[1], 'normalize']
    y3 = df_agregate.loc[df_agregate['last letter'] == last_letter_trend[2], 'normalize']

    fig, ax = plt.subplots()
    ax.plot(y1,label=last_letter_trend[0])
    ax.plot(y2,label=last_letter_trend[1])
    ax.plot(y3,label=last_letter_trend[2])
    ax.set_title('Przebieg trendu popularności', fontsize=12)
    ax.legend()

def zad10(df):
    df=df.set_index('name')
    df=df.pivot_table(values='number', index=['name'],
                    columns=['sex'], aggfunc=sum)
    names = df.index.tolist()

    double_names=[]
    for name in names:
        double_name = df.loc[f'{name}']
        if double_name['M']>0 and double_name['F']>0:
            double_names.append(True)
        else:
            double_names.append(False)

    df['double'] = double_names
    df = df.loc[df['double']==True,:]
    df['sum'] = df['F']+df['M']
    df = df.sort_values(by='sum',ascending=False)
    print(df['sum'])
    double_names = df.index.tolist()
    print(f"Najpopularniejszym imieniem męskim i żeńskim jest {double_names[0]}")

def zad11(df,top_male, top_female):
    popularity = df.loc[:,['name','year','frequency_male','frequency_female']]
    popularity = popularity.pivot_table(values={'frequency_male','frequency_female'}, index=['year','name'], aggfunc=sum)
    popularity = popularity.reset_index()
    popularity['popularity']=popularity['frequency_male']/(popularity['frequency_male']+popularity['frequency_female'])

    first = popularity.loc[(popularity['year']>=1880) & (popularity['year']<=1920),:]
    first = first.pivot_table(values={'popularity'}, index=['name'], aggfunc=np.mean)
    temp = first
    first = first.loc[(first['popularity']>0.7),:]
    first_1 = temp.loc[(temp['popularity']<0.3),:]
    temp1 = first.index.tolist()
    temp3 = first_1.index.tolist()

    second = popularity.loc[(popularity['year'] >= 2000) & (popularity['year'] <= 2019), :]
    second = second.pivot_table(values={'popularity'}, index=['name'], aggfunc=np.mean)
    temp = second
    second = second.loc[(second['popularity']<0.3), :]
    second_1 = temp.loc[(temp['popularity']>0.7), :]
    temp2 = second.index.tolist()
    temp4 = second_1.index.tolist()

    temp1 = set(temp1)
    common_elements = list(temp1.intersection(temp2))

    temp3 = set(temp3)
    common_elements_1 = list(temp3.intersection(temp4))
    common_elements_2 = common_elements+common_elements_1

    top_male =top_male.reset_index()
    top_female = top_female.reset_index()

    top_ever = pd.concat([top_male, top_female])
    top_ever = top_ever.pivot_table(values={'number'}, index=['name'], aggfunc=sum)
    top_ever = top_ever.sort_values(by='number',ascending=False)

    pieces=[]
    temp1 = top_ever.index.tolist()
    temp1 = set(temp1)
    common_elements = list(temp1.intersection(common_elements_2))
    top_ever = top_ever.reset_index()
    for name in common_elements:
        temp = top_ever.loc[top_ever['name']==name,:]
        pieces.append(temp)
    disex_names = pd.concat(pieces, ignore_index=True)
    disex_names = disex_names.sort_values(by='number',ascending=False)
    disex_names = disex_names.set_index('name')
    disex_names = disex_names.index.tolist()

    print('Największa zmiana nastąpiła dla ' + disex_names[0] + ' oraz ' + disex_names[1])

    disex_names_first = popularity.loc[popularity['name']==disex_names[0],['year','popularity']].set_index('year')
    disex_names_second = popularity.loc[popularity['name']==disex_names[1], ['year', 'popularity']].set_index('year')

    fig, ax = plt.subplots()
    ax.plot(disex_names_first,label=f'{disex_names[0]}')
    ax.plot(disex_names_second,label=f'{disex_names[1]}')
    ax.set_title('Przebieg trendu dla imion  których zaobserwowana największa zmiana', fontsize=12)
    ax.legend()

def zad12():
    conn = sqlite3.connect("USA_ltper_1x1.sqlite")
    df = pd.read_sql_query("SELECT * FROM USA_mltper_1x1 union all SELECT * FROM USA_fltper_1x1 ORDER BY Year", conn)
    conn.close()
    return df

def zad13(df,df_2):
    df_2 = pd.pivot_table(df_2, values=['lx', 'dx'], index=['Year'], aggfunc=np.sum)
    df_2 = df_2.reset_index().set_index('Year')

    live = pd.pivot_table(df, values=['number'], index=['year'], aggfunc=np.sum)
    live = live.loc[1959:2017, :]

    df_2['pn'] = live['number'] - df_2['dx']
    y = df_2['pn'].tolist()

    print(f'Łączny przyrost nasturalny na przestrzeni lat wyniósł {sum(y)}')

    fig, ax = plt.subplots()
    ax.plot(y, 'g')
    ax.set_title('Przyrost naturalny', fontsize=12)

def zad14(df,df_2):
    years_live = 1
    live = calculate_survive(df, df_2, years_live)
    y1 = live['survive'].tolist()

    fig, ax = plt.subplots()
    ax.plot(y1, 'b',label = years_live)
    ax.set_title('Współczynnik przeżywalności dzieci', fontsize=12)
    return ax

def zad15(df,df_2, ax):
    years_live = 5
    live = calculate_survive(df,df_2,years_live)
    y = live['survive'].tolist()

    ax.plot(y, 'r', label=years_live)
    ax.set_title('Współczynnik przeżywalności dzieci', fontsize=12)
    ax.legend()

def main():
    df = zad1()
    zad2(df)
    zad3(df)
    df = zad4(df)
    zad5(df)
    top_male, top_female = zad6(df)
    zad7(df, top_male, top_female)
    zad8(df, top_male, top_female)
    zad9(df)
    zad10(df)
    zad11(df, top_male, top_female)
    df_2 = zad12()
    zad13(df, df_2)
    ax = zad14(df, df_2)
    zad15(df, df_2, ax)
    plt.show()

main()