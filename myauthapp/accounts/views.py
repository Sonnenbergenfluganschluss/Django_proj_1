from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib import messages
from django.http import JsonResponse  # если нужен AJAX
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, date
import re
import os
import pytz
from itertools import cycle

animal = ["крыса", "бык", "тигр", "кролик", "дракон", "змея", "лошадь", "коза", "обезьяна", "петух", "собака", "свинья"]
stihiya = ["дерево", "дерево", "огонь", "огонь", "почва", "почва", "металл", "металл", "вода", "вода"]
in_yan = ["ян", "инь"]

vis_yaer = [1920, 1924, 1928, 1932, 1936, 1940, 1944, 1948, 1952, 1956, 1960, 1964, 1968, 
            1972, 1976, 1980, 1984, 1988, 1992, 1996, 2000, 2004, 2008, 2012, 2016, 2020, 
            2024, 2028, 2032, 2036, 2040, 2044, 2048, 2052]

moon_palace = dict({1: [1920, 1942, 0, 1987, 2009, 2032], 2: [0, 1943, 1965, 1988, 2010, 0], 
    3: [1921, 1944, 1966, 0, 2011, 2033], 4: [1922, 0, 1967, 1989, 2012, 2034], 
    5: [1923, 1945, 1968, 1990, 0, 2035], 6: [1924, 1946, 0, 1991, 2013, 2036], 
    7: [0, 1947, 1969, 1992, 2014, 0], 8: [1925, 1948, 1970, 0, 2015, 2037], 
    9: [1926, 0, 1971, 1993, 2016, 2038], 10: [1927, 1949, 1972, 1994, 0, 2039], 
    11: [1928, 1950, 0, 1995, 2017, 2040], 12: [0, 1951, 1973, 1996, 2018, 0], 
    13: [1929, 1952, 1974, 0, 2019, 2041], 14: [1930, 0, 1975, 1997, 2020, 2042], 
    15: [1931, 1953, 1976, 1998, 0, 2043], 16: [1932, 1954, 0, 1999, 2021, 2044], 
    17: [0, 1955, 1977, 2000, 2022, 0], 18: [1933, 1956, 1978, 0, 2023, 2045], 
    19: [1934, 0, 1979, 2001, 2024, 2046], 20: [1935, 1957, 1980, 2002, 0, 2047], 
    21: [1936, 1958, 0, 2003, 2025, 2048], 22: [0, 1959, 1981, 2004, 2026, 0], 
    23: [1937, 1960, 1982, 0, 2027, 2049], 24: [1938, 0, 1983, 2005, 2028, 2050], 
    25: [1939, 1961, 1984, 2006, 0, 2051], 26: [1940, 1962, 0, 2007, 2029, 2052], 
    27: [0, 1963, 1985, 2008, 2030, 0], 28: [1941, 1964, 1986, 0, 2031, 2053]})

sec_step = {1:27, 2:2, 3:2, 4:5, 5:7, 6:10, 7:12, 8:15, 9:18, 10:20, 11:23, 12:25}


man = ["Liv.1", "Liv.4", "Liv.3", "Gb.37/Liv.3", "Liv.5/Gb.40", "Liv.2", "Liv.8", 
    "Kid.1", "Kid.7", "Kid.3", "Bl.58/Kid.3", "Kid.4/Bl.64", "Kid.2", "Kid.10", 
    "Lu.11", "Lu.8", "Lu.9", "Co.6/Lu.9", "Co.4/Lu.7", "Lu.10", "Lu.5", 
    "Ht.9/Hg.9", "Ht.4/Hg.5", "Ht.7/Hg.7", "Si.7/Ht.7/Hg.7", 
    "Ht.5/Hg.6/Si.4", "Ht.8/Hg.8", "Ht.3/ Hg.3"]

woman = ["Gb.41", "Gb.44", "Gb.34", "Gb.37/Liv.3", "Liv.5/Gb.40", "Gb.38", "Gb.43", 
    "Bl.65", "Bl.67", "Bl.40", "Bl.58/Kid.3", "Kid.4/Bl.64", "Bl.60", "Bl.66", 
    "Co.3", "Co.1", "Co.11", "Co.6/Lu.9", "Co4/Lu.7", "Co.5", "Co.2", 
    "Si.3", "Si.1", "Si.8", "Si.7/Ht.7/Hg.7", "Ht.5/Hg.6/Si.4", "Si.5", "Si.2"]

sky = {'甲': ':green[甲]',
        '乙': ':green[乙]',
        '丙': ':red[丙]',
        '丁': ':red[丁]',
        '戊': ':orange[戊]',
        '己': ':orange[己]',
        '庚': ':darkgray[庚]',
        '辛': ':darkgray[辛]',
        '壬': ':blue[壬]',
        '癸': ':blue[癸]'}

earth = {'子': ':blue[子]',
        '丑': ':orange[丑]',
        '寅': ':green[寅]',
        '卯': ':green[卯]',
        '辰': ':orange[辰]',
        '巳': ':red[巳]',
        '午': ':red[午]',
        '未': ':orange[未]',
        '申': ':darkgray[申]',
        '酉': ':darkgray[酉]',
        '戌': ':orange[戌]',
        '亥': ':blue[亥]'}

color_dict = {'甲':'green', '乙':'green', '丙':'red', '丁':'red', '戊':'orange', '己':'orange', '庚':'grey', '辛':'grey', '壬':'blue', '癸':'blue',
                '子':'blue', '丑':'orange', '寅':'green', '卯':'green', '辰':'orange', '巳':'red', '午':'red', '未':'orange', '申':'grey', '酉':'grey', '戌':'orange', '亥':'blue'}

color_dict_earth = {'子':'blue', '丑':'orange', '寅':'green', '卯':'green', '辰':'orange', '巳':'red', '午':'red', '未':'orange', '申':'grey', '酉':'grey', '戌':'orange', '亥':'blue'}


def local_css(file_name):
    with open(file_name) as f:
        print('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)


def read_files():       
    cities = pd.read_csv("accounts/data/cities.csv")
    earth_legs = pd.read_csv("accounts/data/earth_legs.csv")
    sky_hands = pd.read_csv("accounts/data/sky_hands.csv")
    planets = pd.read_csv("accounts/data/planets.csv")
    moon_palace_df = pd.read_csv("accounts/data/moon_palace.csv")
    calendar = pd.read_csv("accounts/data/calendar.csv")
    cicle = pd.read_csv("accounts/data/cicle.csv")
    seasons = pd.read_csv("accounts/data/seasons.csv")
    veto = pd.read_csv("accounts/data/veto.csv")
    return cities, earth_legs, sky_hands, planets, moon_palace_df, calendar, cicle, seasons, veto


def background(color):
    return np.where(f"color: {color};", None)

def get_month(our_date):
    stih = cycle(stihiya)
    anim = cycle(animal)
    inyan = cycle(in_yan)  
    start_month = date(1924, 1, 1)
    end_months=(our_date.year-start_month.year)*12 + our_date.month + 1
    lst = []
    for i in range(end_months):
        lst.append(f"{next(anim)} {next(inyan)} {next(stih)}".capitalize())
    return lst[-1]


# Функция для окрашивания отдельных слов
def highlight_words(text):
    highlighted_text = text
    if text[0] in color_dict.keys():
        highlighted_text = text.replace(text[0], f'<span style="color:{color_dict[text[0]]};font-weight: bold">{text[0]}</span>')
        highlighted_text = highlighted_text.replace(text[1], f'<span style="color:{color_dict[text[1]]};font-weight: bold">{text[1]}</span>')
    else:
        highlighted_text = text.replace(" ", "<br>")
    return highlighted_text
########################################  Создаём приложение ######################################

cities, earth_legs, sky_hands, planets, moon_palace_df, calendar, cicle, seasons, veto = read_files()
calendar['date'] = pd.to_datetime(calendar['date'])

@login_required
def home(request):




    
    # # Обработка данных (пример)
    # context = {
    #     'current_date': datetime.now().strftime("%d.%m.%Y"),
    #     # Добавьте другие переменные, которые нужно передать в шаблон
    # }
    
    # if request.method == 'POST':
    #     # Обработка POST-запроса с данными формы
    #     birthday = request.POST.get('birthday')
    #     birthday = pd.to_datetime(birthday).strftime("%d.%m.%Y")

    #     # our_date = request.POST.get('our_date')
    #     # our_date = pd.to_datetime(our_date, dayfirst=True).strftime("%d.%m.%Y")

    #     # city = request.POST.get('city')
        
    #     # Здесь добавьте вашу логику обработки даты и города
    #     # ...
        
    #     # Добавьте результаты в контекст
    #     context.update({
    #         'birthday': birthday,
    #         # 'our_date': our_date,
    #         # 'city': city,
    #         # Другие результаты вычислений
    #     })
    
    # try:
    #     birthday = pd.to_datetime(birthday, dayfirst=True).strftime("%d.%m.%Y")
    #     # birthday = str(pd.to_datetime(birthday, dayfirst=True)).split()[0]
    #     # st.markdown(f'Дата рождения: **{pd.to_datetime(birthday).strftime("%d.%m.%Y")}**')

    #     if pd.to_datetime(birthday) < pd.to_datetime(seasons.loc[2, str(pd.to_datetime(birthday).year)]):
    #         year_v = calendar[calendar['date']==pd.to_datetime(pd.to_datetime(birthday)-timedelta(days=51))]['years'].values[0]
    #     else:
    #         year_v = calendar[calendar['date']==pd.to_datetime(birthday)]['years'].values[0]

    #     mv = calendar[calendar['date']==pd.to_datetime(birthday)]['months'].values[0]
    #     if pd.to_datetime(birthday) < pd.to_datetime(seasons[seasons['Месяц']==mv.split()[0]][str(pd.to_datetime(birthday).year)].values[0]):
    #         month_v = calendar[calendar['date']==pd.to_datetime(pd.to_datetime(birthday)-timedelta(days=21))]['months'].values[0]
    #     else:
    #         month_v = calendar[calendar['date']==pd.to_datetime(birthday)]['months'].values[0]
    #     day_v = calendar[calendar['date']==pd.to_datetime(birthday)]['days'].values[0]
    #     day_ier = cicle[cicle["Название_calendar"] == day_v]["Иероглиф"].values[0]
    #     month_ier = cicle[cicle["Название_calendar"] == month_v]["Иероглиф"].values[0]
    #     year_ier = cicle[cicle["Название_calendar"] == year_v]["Иероглиф"].values[0]


    #     birthday_df = pd.DataFrame(columns=["День", "Месяц", "Год"], data=None)
    #     birthday_df["День"] = [
    #         f"{cicle[cicle['Название_calendar'] == day_v]['Название_Русский'].values[0]}",
    #         day_ier
    #     ]
    #     birthday_df["Месяц"] = [
    #         f"{cicle[cicle['Название_calendar'] == month_v]['Название_Русский'].values[0]}",
    #         month_ier
    #     ]
    #     birthday_df["Год"] = [
    #         f"{cicle[cicle['Название_calendar'] == year_v]['Название_Русский'].values[0]}",
    #         year_ier
    #     ]
        
    #     birthday_df['День'] = birthday_df['День'].apply(highlight_words)
    #     birthday_df['Месяц'] = birthday_df['Месяц'].apply(highlight_words)
    #     birthday_df['Год'] = birthday_df['Год'].apply(highlight_words)
        
    #     styled_df_b = birthday_df.to_html(
    #             classes='table table-striped table-hover',
    #             table_id='styled_df_b',
    #             escape=False,
    #             index=False,  # Не показывать индексы
    #             # border=0,     # Без границ
    #             justify='center'  # Выравнивание
    #         )
        
    #     context.update({
    #         'styled_df_b' : styled_df_b,
    #     })
    # #     st.write(styled_df_b, unsafe_allow_html=True)
    # except:
    #     print("Некорректная дата. Попробуйте снова")
    
    return render(request, 'accounts/home.html')








def process_birthday(request, calendar=calendar, 
                     cicle=cicle, seasons=seasons, highlight_words=highlight_words):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            birthday = data.get('birthday')
            print(birthday)
            try:
                birthday = pd.to_datetime(birthday).strftime("%d.%m.%Y")
                if pd.to_datetime(birthday) < pd.to_datetime(seasons.loc[2, str(pd.to_datetime(birthday).year)]):
                    year_v = calendar[calendar['date']==pd.to_datetime(pd.to_datetime(birthday)-timedelta(days=51))]['years'].values[0]
                else:
                    year_v = calendar[calendar['date']==pd.to_datetime(birthday)]['years'].values[0]

                mv = calendar[calendar['date']==pd.to_datetime(birthday)]['months'].values[0]
                if pd.to_datetime(birthday) < pd.to_datetime(seasons[seasons['Месяц']==mv.split()[0]][str(pd.to_datetime(birthday).year)].values[0]):
                    month_v = calendar[calendar['date']==pd.to_datetime(pd.to_datetime(birthday)-timedelta(days=21))]['months'].values[0]
                else:
                    month_v = calendar[calendar['date']==pd.to_datetime(birthday)]['months'].values[0]
                day_v = calendar[calendar['date']==pd.to_datetime(birthday)]['days'].values[0]
                day_ier = cicle[cicle["Название_calendar"] == day_v]["Иероглиф"].values[0]
                month_ier = cicle[cicle["Название_calendar"] == month_v]["Иероглиф"].values[0]
                year_ier = cicle[cicle["Название_calendar"] == year_v]["Иероглиф"].values[0]


                birthday_df = pd.DataFrame(columns=["День", "Месяц", "Год"], data=None)
                birthday_df["День"] = [
                    f"{cicle[cicle['Название_calendar'] == day_v]['Название_Русский'].values[0]}",
                    day_ier
                ]
                birthday_df["Месяц"] = [
                    f"{cicle[cicle['Название_calendar'] == month_v]['Название_Русский'].values[0]}",
                    month_ier
                ]
                birthday_df["Год"] = [
                    f"{cicle[cicle['Название_calendar'] == year_v]['Название_Русский'].values[0]}",
                    year_ier
                ]
                
                birthday_df['День'] = birthday_df['День'].apply(highlight_words)
                birthday_df['Месяц'] = birthday_df['Месяц'].apply(highlight_words)
                birthday_df['Год'] = birthday_df['Год'].apply(highlight_words)
                
                styled_df_b = birthday_df.to_html(
                        classes='table table-striped table-hover',
                        table_id='styled_df_b',
                        escape=False,
                        index=False,  # Не показывать индексы
                        # border=0,     # Без границ
                        justify='center'  # Выравнивание
                    )
            except:
                print("Некорректная дата. Попробуйте снова")
            
            result = {
                'success': True,
                'birthday_result': birthday,
                'birthday_table': styled_df_b
            }
            return JsonResponse(result)
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})



def process_city(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            city = data.get('city')
            
            # Ваши вычисления для города
            result = {
                'success': True,
                'city_result': f"Обработан город: {city}",
                'time_data': {}  # Результаты для времени
            }
            return JsonResponse(result)
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль обновлен!')
            return redirect('profile')
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

