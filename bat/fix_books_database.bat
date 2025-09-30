@echo off
<div class="container">
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-body p-0">
                        
                        <div class="pdf-container">
                            <iframe src="/media/books/pdfs/veb-dizayn-dlya-nachinayuschih.pdf#toolbar=1&amp;navpanes=1&amp;scrollbar=1" width="100%" height="100%" frameborder="0" style="border: none;">
                                <p>Ваш браузер не поддерживает отображение PDF файлов. 
                                   <a href="/media/books/pdfs/veb-dizayn-dlya-nachinayuschih.pdf" target="_blank">Открыть в новой вкладке</a>
                                </p>
                            </iframe>
                        </div>
                        
                    </div>
                </div>
            </div>
        </div>
    </div>chcp 65001
echo ========================================
echo    Исправление базы данных для книг
echo ========================================
echo.

echo [1/3] Создание миграций...
python manage.py makemigrations books

echo.
echo [2/3] Применение миграций...
python manage.py migrate

echo.
echo [3/3] Создание тестовых данных...
python fix_database.py

echo.
echo ========================================
echo    Исправление завершено!
echo ========================================
echo.
echo Теперь вы можете перейти на:
echo http://127.0.0.1:8001/books/
echo.
pause

