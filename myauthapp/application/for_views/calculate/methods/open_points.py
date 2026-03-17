from ...constants import open_sky_points, ustya
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
            
    # Поиск для 'Метод укрепления изначального Ян':
    for k, v in ustya.items():
        if v[0] <= current_time < v[1]:
            current_slot = [v[0].strftime('%H:%M'), v[1].strftime('%H:%M')]
            cur_point = k.capitalize()
        if v[0] <= next_time.time() < v[1]:
            next_point = k.capitalize()
            time_slot = [v[0].strftime('%H:%M'), v[1].strftime('%H:%M')]    
            
    result = f'''
            <div class=container>
                <div style='font-weight: bold;'>Открытые точки структуры небесных стволов:</div>
                <div class=container style=padding:20px;>
                    <div> 
                        На текущий момент, с {current_time_slot[0]} до {current_time_slot[1]}, 
                        открыты точки: <span style='color:#588ed4; font-weight: bold;'>{current_point}</span>. 
                        <br>Следующий временной промежуток с {time_slot[0]} до {time_slot[1]}, 
                        открыты точки: <span style='color:#588ed4; font-weight: bold;'>{next_point}</span>. 
                    </div>
                </div>
            </div>
            <div class=container>
                <div style='font-weight: bold;'>Метод укрепления изначального Ян:</div>
                <div class=container style=padding:20px;>
                    <div> 
                        1. Последовательно одной иглой соединяем точки: 
                        <span style='color:#588ed4; font-weight: bold;'>Cv4</span>, 
                        <span style='color:#588ed4; font-weight: bold;'>Cv5</span>, 
                        <span style='color:#588ed4; font-weight: bold;'>Cv6</span>. <br>
                        2. Вспомогательная точка - <span style='color:#588ed4; font-weight: bold;'>Kid16</span> 
                        ставится билатерально. <br>
                        3. <span style='font-weight: bold;'>Перед извлечением игл</span> стимулируем точку-устье канала согласно времени: <br>
                        c {current_slot[0]} до {current_slot[1]} - точка <span style='color:#588ed4; font-weight: bold;'>{cur_point}</span>. 
                        <br> {day_iero}
                    </div>
                </div>
            </div>
        '''        
    return result
        