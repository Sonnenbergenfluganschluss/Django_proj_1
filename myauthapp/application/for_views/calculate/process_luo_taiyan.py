import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .methods.taiyanbafa import get_luo_taiyan

@login_required
@csrf_exempt
def process_luo_taiyan(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            needed_channel1 = data.get('needed_channel1')
            needed_channel2 = data.get('needed_channel2')            

            # Вычисляем результат
            result = get_luo_taiyan(needed_channel1, needed_channel2)

            return JsonResponse({
                'success': True,
                'result': result
            })
        except Exception as e:
            return JsonResponse({
                'success': False, 
                'error': str(e)
            })
    
    return JsonResponse({'success': False, 'error': 'Only POST method allowed'})