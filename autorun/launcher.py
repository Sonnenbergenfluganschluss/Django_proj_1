import os
import sys
import subprocess
import webbrowser
import time
import socket
import threading
import tkinter as tk
from tkinter import messagebox

class DjangoLauncher:
    def __init__(self):
        # Путь к проекту (можно указать в настройках)
        self.project_path = r"C:/hronopunktura/myauthapp"
        self.port = 8000
        self.process = None
        
    def find_free_port(self):
        """Находит свободный порт"""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            return s.getsockname()[1]
    
    def check_project(self):
        """Проверяет наличие проекта"""
        if not os.path.exists(self.project_path):
            return False, f"Папка проекта не найдена:\n{self.project_path}"
        
        manage_path = os.path.join(self.project_path, 'manage.py')
        if not os.path.exists(manage_path):
            return False, f"Файл manage.py не найден:\n{manage_path}"
        
        return True, "OK"
    
    def run_server(self):
        """Запускает Django сервер"""
        try:
            # Проверяем проект
            ok, msg = self.check_project()
            if not ok:
                messagebox.showerror("Ошибка", msg)
                return
            
            # Находим свободный порт
            self.port = self.find_free_port()
            
            # Переходим в папку проекта
            os.chdir(self.project_path)
            
            # Проверяем наличие виртуального окружения
            venv_python = os.path.join(self.project_path, 'venv', 'Scripts', 'python.exe')
            if os.path.exists(venv_python):
                python_exe = venv_python
            else:
                python_exe = 'python'
            
            # Запускаем сервер
            cmd = [python_exe, 'manage.py', 'runserver', f'127.0.0.1:{self.port}']
            
            # Создаем процесс
            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                cwd=self.project_path,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            
            # Открываем браузер после запуска
            def open_browser():
                time.sleep(3)
                webbrowser.open(f'http://127.0.0.1:{self.port}')
            
            threading.Thread(target=open_browser, daemon=True).start()
            
            # Показываем GUI с управлением
            self.show_control_panel()
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить сервер:\n{str(e)}")
    
    def show_control_panel(self):
        """Показывает панель управления"""
        root = tk.Tk()
        root.title("Chronos Server")
        root.geometry("300x150")
        root.resizable(False, False)
        
        # Иконка (опционально)
        try:
            root.iconbitmap('app.ico')
        except:
            pass
        
        # Информация
        tk.Label(
            root, 
            text=f"Сервер запущен на порту {self.port}", 
            font=('Arial', 10)
        ).pack(pady=10)
        
        tk.Label(
            root, 
            text=f"http://127.0.0.1:{self.port}", 
            font=('Arial', 10, 'bold'),
            fg='blue'
        ).pack(pady=5)
        
        # Кнопки
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame,
            text="Открыть в браузере",
            command=lambda: webbrowser.open(f'http://127.0.0.1:{self.port}'),
            width=20
        ).pack(pady=5)
        
        tk.Button(
            btn_frame,
            text="Остановить сервер",
            command=lambda: self.stop_server(root),
            bg='red',
            fg='white',
            width=20
        ).pack(pady=5)
        
        # Обработка закрытия окна
        root.protocol("WM_DELETE_WINDOW", lambda: self.stop_server(root))
        
        root.mainloop()
    
    def stop_server(self, root):
        """Останавливает сервер"""
        if self.process:
            self.process.terminate()
            self.process = None
        
        root.quit()
        root.destroy()
        sys.exit(0)

if __name__ == '__main__':
    launcher = DjangoLauncher()
    
    # Можно указать путь через аргумент командной строки
    if len(sys.argv) > 1:
        launcher.project_path = sys.argv[1]
    
    launcher.run_server()