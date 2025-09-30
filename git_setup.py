#!/usr/bin/env python3
import subprocess
import sys
import os

def run_command(command):
    """Выполняет команду и возвращает результат"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, encoding='utf-8')
        print(f"Команда: {command}")
        print(f"Код выхода: {result.returncode}")
        if result.stdout:
            print(f"Вывод: {result.stdout}")
        if result.stderr:
            print(f"Ошибки: {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"Ошибка выполнения команды: {e}")
        return False

def main():
    print("=== Настройка Git репозитория ===")
    
    # Проверяем, что мы в Git репозитории
    if not os.path.exists('.git'):
        print("Ошибка: Не найден .git каталог. Убедитесь, что вы находитесь в Git репозитории.")
        return
    
    # Добавляем файлы
    print("\n1. Добавляем файлы в Git...")
    if not run_command('git add .'):
        print("Ошибка при добавлении файлов")
        return
    
    # Проверяем статус
    print("\n2. Проверяем статус...")
    run_command('git status')
    
    # Создаем первый коммит
    print("\n3. Создаем первый коммит...")
    if not run_command('git commit -m "Initial commit: Django knowledge base project"'):
        print("Ошибка при создании коммита")
        return
    
    print("\n=== Git репозиторий готов! ===")
    print("\nСледующие шаги:")
    print("1. Создайте репозиторий на GitHub.com")
    print("2. Скопируйте URL репозитория")
    print("3. Выполните команды:")
    print("   git remote add origin <URL_ВАШЕГО_РЕПОЗИТОРИЯ>")
    print("   git branch -M main")
    print("   git push -u origin main")

if __name__ == "__main__":
    main()
