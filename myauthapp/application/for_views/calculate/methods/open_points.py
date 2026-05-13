from ...constants import open_sky_points, ustya, najafa, color_dict
import datetime

def get_additional_points(day_iero, solartime):
    lst_time = solartime.split(':')
    current_time = datetime.time(int(lst_time[0]), int(lst_time[1]), 0)
    now_datetime = datetime.datetime(2000, 1, 1, int(lst_time[0]), int(lst_time[1]), 0)
    next_time = now_datetime + datetime.timedelta(minutes=28, seconds=48)
    
    # поиск для 'Открытые точки структуры небесных стволов':
    for k, v in open_sky_points.items():
        if v[0] <= current_time < v[1]:
            current_time_slot = [v[0].strftime('%H:%M'), v[1].strftime('%H:%M')]
            current_point = k.capitalize()
        if v[0] <= next_time.time() < v[1]:
            next_point = k.capitalize()
            time_slot = [v[0].strftime('%H:%M'), v[1].strftime('%H:%M')]
        else:
            next_point = '-'
            time_slot = ['-', '-']
            
    # Поиск для 'Метод укрепления изначального Ян':
    for k, v in ustya.items():
        if v[0] <= current_time < v[1]:
            current_slot = [v[0].strftime('%H:%M'), v[1].strftime('%H:%M')]
            cur_point = k.capitalize()  

    # Поиск точек Najafa
    for k, v in najafa.items():
        if k==day_iero[0]:
            current_day = v
            if current_time < current_day['change_day']:
                points_of_space = current_day['points_of_space'][0]
            else:
                points_of_space = current_day['points_of_space'][1]
            
            points_of_time = current_day['points_of_time']
            for k, v in points_of_time.items():
                if v[0] <= current_time < v[1]:
                    point_of_time = k.capitalize()

            last_28_minutes = current_day['last_28_minutes']
            for k, v in last_28_minutes.items():
                if v[0] <= current_time < v[1]:
                    point_of_last_28_minutes = k.capitalize()
                    last_datetime = datetime.datetime(2000, 1, 1, int(v[1].hour), int(v[1].minute))
                    last_time = last_datetime - datetime.timedelta(minutes=27, seconds=0)
                    last_28_minutes_slot = (last_time.strftime('%H:%M'), v[1].strftime('%H:%M'))

    color_point = "#4a78b6"
            
    result = f'''
            <div class=container>
                <div style='font-weight: bold;'>Открытые точки структуры небесных стволов:</div>
                <div class=container style=padding:20px;>
                    <div> 
                        На текущий момент, с {current_time_slot[0]} до {current_time_slot[1]}, 
                        открыты точки: <span style='color:{color_point}; font-weight: bold;'>{current_point}</span>. 
                        <br>Следующий временной промежуток с {time_slot[0]} до {time_slot[1]}, 
                        открыты точки: <span style='color:{color_point}; font-weight: bold;'>{next_point}</span>. 
                    </div>
                </div>
            </div>
            <div class=container>
                <div style='font-weight: bold;'>Метод укрепления изначального Ян:</div>
                <div class=container style=padding:20px;>
                    <div> 
                        1. Последовательно одной иглой соединяем точки: 
                        <span style='color:{color_point}; font-weight: bold;'>Cv4</span>, 
                        <span style='color:{color_point}; font-weight: bold;'>Cv5</span>, 
                        <span style='color:{color_point}; font-weight: bold;'>Cv6</span>. <br>
                        2. Вспомогательная точка - <span style='color:{color_point}; font-weight: bold;'>Kid16</span> 
                        ставится билатерально. <br>
                        3. <span style='font-weight: bold;'>Перед извлечением игл</span> стимулируем точку-устье канала согласно времени: <br>
                        c {current_slot[0]} до {current_slot[1]} - точка <span style='color:{color_point}; font-weight: bold;'>{cur_point}</span>. 
                    </div>
                </div>
            </div>
            <div class=container>
                <div style='font-weight: bold;'>Метод Na ja fa:</div>
                <div class=container style=padding:20px;>
                    <div> 
                        Небесный ствол дня сегодня: <span style='color: {color_dict[day_iero[0]]}; font-weight: bold;'>{day_iero[0]}</span> <br>
                        Точки времени: <span style='color:{color_point}; font-weight: bold;'>{point_of_time}</span>. <br>
                        Точки пространства: <span style='color:{color_point}; font-weight: bold;'>{points_of_space}</span>. <br>
                        Точки последних 28 минут стража <span style='color:{color_point}; font-weight: bold;'>{point_of_last_28_minutes}</span>, активны с {last_28_minutes_slot[0]} по {last_28_minutes_slot[1]}: . <br>
                    </div>
                </div>
            </div>
        '''        
    return result
        