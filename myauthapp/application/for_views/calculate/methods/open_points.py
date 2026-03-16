from ...constants import open_sky_points
import datetime

def get_open_points(solartime):
    lst_time = solartime.split(':')
    current_time = datetime.time(int(lst_time[0]), int(lst_time[1]), 0)
    for k, v in open_sky_points.items():
        if v[0] <= current_time < v[1]:
            point = k.capitalize()
    result = f'''
            <div>
                <p> На текущий момент открыты точки: <span style='color:blue;'>{point}</span>. </p>
            </div>
        '''        
    return result