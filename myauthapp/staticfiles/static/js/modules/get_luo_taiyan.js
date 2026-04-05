document.addEventListener('DOMContentLoaded', function() {
    const predictionForm = document.getElementById('predictionForm');
    const luoTaiyanResult = document.getElementById('luoTaiyanResult');
    
    if (predictionForm) {
        predictionForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const needed_сhannel1 = document.getElementById('needed_channel1').value;
            const needed_сhannel2 = document.getElementById('needed_channel2').value;
            
            if (!needed_сhannel1) {
                luoTaiyanResult.innerHTML = "<div class='alert alert-warning'>Пожалуйста, выберите канал</div>";
                return;
            }
            // if (!needed_сhannel2) {
            //     luoTaiyanResult.innerHTML = "<div class='alert alert-warning'>Пожалуйста, выберите канал</div>";
            //     return;
            // }
            
            // Показываем индикатор загрузки
            luoTaiyanResult.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div></div>';
            
            // Отправляем AJAX запрос
            fetch('/process-luo-taiyan/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': '{{ csrf_token }}'
                },
                body: JSON.stringify({
                    needed_channel1: needed_сhannel1,
                    needed_channel2: needed_сhannel2
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    luoTaiyanResult.innerHTML = data.result;
                } else {
                    luoTaiyanResult.innerHTML = `<div class="alert alert-danger">Ошибка: ${data.error}</div>`;
                }
            })
            .catch(error => {
                luoTaiyanResult.innerHTML = `<div class="alert alert-danger">Ошибка сети: ${error}</div>`;
            });
        });
    }
});