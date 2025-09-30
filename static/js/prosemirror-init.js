// Simple Rich Text Editor Initialization
// Упрощенный редактор без ProseMirror, но с функциональностью форматирования

function initProseMirror(widgetId) {
    const textarea = document.getElementById(widgetId);
    const editorContainer = document.getElementById(`editor-${widgetId}`);
    
    if (!textarea || !editorContainer) {
        console.error('Editor: Required elements not found');
        return;
    }
    
    // Создаем динамическую кнопку плюсик
    const plusButton = document.createElement('button');
    plusButton.id = `plus-${widgetId}`;
    plusButton.className = 'block-menu__plus non-removable';
    plusButton.title = 'Добавить элемент';
    plusButton.style.position = 'absolute';
    plusButton.style.width = '24px';
    plusButton.style.height = '24px';
    plusButton.style.display = 'flex';
    plusButton.style.alignItems = 'center';
    plusButton.style.justifyContent = 'center';
    plusButton.style.background = 'white';
    plusButton.style.border = '1px solid #e1e5e9';
    plusButton.style.color = '#929ca5';
    plusButton.style.cursor = 'pointer';
    plusButton.style.zIndex = '1000';
    plusButton.style.opacity = '0.8';
    plusButton.style.borderRadius = '4px';
    plusButton.style.boxShadow = '0 1px 3px rgba(0,0,0,0.1)';
    plusButton.style.pointerEvents = 'auto';
    plusButton.style.transition = 'opacity 0.2s ease';
    plusButton.style.visibility = 'hidden'; // Начально скрыт
    
    plusButton.innerHTML = '<svg class="svg-icon" fill="currentColor" height="16" viewBox="0 0 24 24" width="16">' +
                           '<path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>';
    
    // Добавляем кнопку к контейнеру редактора
    editorContainer.parentNode.appendChild(plusButton);
    
    // Инициализация редактора
    editorContainer.innerHTML = textarea.value || '<p><br></p>';
    editorContainer.setAttribute('data-placeholder', 'Начните писать... Используйте / для команд или нажмите +');
    editorContainer.setAttribute('contenteditable', 'true');
    
    // Команды через /
    const commands = [
        { trigger: '/h1', title: 'Заголовок 1', description: 'Большой заголовок', icon: 'H1', category: 'Заголовки' },
        { trigger: '/h2', title: 'Заголовок 2', description: 'Средний заголовок', icon: 'H2', category: 'Заголовки' },
        { trigger: '/h3', title: 'Заголовок 3', description: 'Маленький заголовок', icon: 'H3', category: 'Заголовки' },
        { trigger: '/p', title: 'Параграф', description: 'Обычный текст', icon: 'P', category: 'Текст' },
        { trigger: '/ul', title: 'Список', description: 'Маркированный список', icon: '•', category: 'Списки' },
        { trigger: '/ol', title: 'Нумерованный список', description: 'Пронумерованный список', icon: '1.', category: 'Списки' },
        { trigger: '/code', title: 'Код-блок', description: 'Контейнер с заголовком и копированием', icon: '&lt;/&gt;', category: 'Код' },
        { trigger: '/quote', title: 'Цитата', description: 'Блок цитаты', icon: '"', category: 'Текст' },
        { trigger: '/bold', title: 'Жирный текст', description: 'Выделить жирным', icon: 'B', category: 'Форматирование' },
        { trigger: '/italic', title: 'Курсив', description: 'Выделить курсивом', icon: 'I', category: 'Форматирование' },
        { trigger: '/underline', title: 'Подчеркнутый', description: 'Подчеркнуть текст', icon: 'U', category: 'Форматирование' },
        { trigger: '/image', title: 'Изображение', description: 'Вставить изображение в контейнер с подписью', icon: '🖼️', category: 'Медиа' },
        { trigger: '/gallery', title: 'Галерея', description: 'Две картинки рядом', icon: '🖼️🖼️', category: 'Медиа' },
        { trigger: '/hr', title: 'Разделитель', description: 'Горизонтальная линия', icon: '—', category: 'Элементы' },
        { trigger: '/link', title: 'Ссылка', description: 'Вставить ссылку', icon: '🔗', category: 'Элементы' },
        { trigger: '/info', title: 'Врезка: Info', description: 'Синяя информационная врезка', icon: 'ℹ️', category: 'Врезки' },
        { trigger: '/success', title: 'Врезка: Success', description: 'Зеленая положительная врезка', icon: '✅', category: 'Врезки' },
        { trigger: '/warning', title: 'Врезка: Warning', description: 'Желтая предупреждающая врезка', icon: '⚠️', category: 'Врезки' },
        { trigger: '/danger', title: 'Врезка: Danger', description: 'Красная критическая врезка', icon: '⛔', category: 'Врезки' },
        { trigger: '/table', title: 'Таблица 2×2', description: 'Мини-таблица с заголовком', icon: '▦', category: 'Таблица' },
        { trigger: '/checklist', title: 'Чек‑лист', description: 'Список задач с чекбоксами', icon: '☑️', category: 'Списки' },
    ];
    
    let commandMenu = null;
    let currentCommand = '';
    let selectedCommandIndex = 0;
    
    // Флаг для отслеживания состояния командного меню и блокировки кнопок
    let isCommandMenuOpen = false;
    let isProcessingCommand = false;
    let lastClickTime = 0;
    
    // Обработчик для кнопки +
    if (plusButton) {
        plusButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            // Проверка на дебаунс (предотвращение двойных кликов)
            const now = Date.now();
            if (now - lastClickTime < 500) {
                return; // Игнорируем клики с интервалом менее 500мс
            }
            lastClickTime = now;
            
            // Предотвращаем многократный вызов командного меню
            if (isCommandMenuOpen || commandMenu || isProcessingCommand) {
                hideCommandMenu();
                return;
            }
            
            // Устанавливаем флаг блокировки
            isCommandMenuOpen = true;
            isProcessingCommand = true;
            
            // Проверяем, есть ли выделенный текст
            const selection = window.getSelection();
            if (selection.toString().trim()) {
                showCommandMenuForSelection();
            } else {
                showCommandMenu();
            }
            
            // Сбрасываем флаг после задержки
            setTimeout(() => {
                isCommandMenuOpen = false;
                
                // Разблокируем обработку команд через дополнительную задержку
                setTimeout(() => {
                    isProcessingCommand = false;
                }, 200);
            }, 300);
        });
        
        // Обработчик для позиционирования кнопки рядом с текущей строкой
        editorContainer.addEventListener('mouseup', updatePlusButtonPosition);
        editorContainer.addEventListener('keyup', updatePlusButtonPosition);
        editorContainer.addEventListener('keydown', updatePlusButtonPosition);
        editorContainer.addEventListener('click', updatePlusButtonPosition);
        editorContainer.addEventListener('focus', updatePlusButtonPosition);
        editorContainer.addEventListener('input', updatePlusButtonPosition);
        editorContainer.addEventListener('scroll', updatePlusButtonPosition);
        window.addEventListener('scroll', updatePlusButtonPosition);
        window.addEventListener('resize', updatePlusButtonPosition);
        
        // Обновление позиции при прокрутке с интервалом
        setInterval(updatePlusButtonPosition, 300);
        
        // Начальное позиционирование
        setTimeout(updatePlusButtonPosition, 100);
        setTimeout(updatePlusButtonPosition, 500);
        setTimeout(updatePlusButtonPosition, 1000);
    }
    
    // Функция для обновления позиции кнопки +
    function updatePlusButtonPosition() {
        if (!plusButton) return;
        
        const selection = window.getSelection();
        if (!selection.rangeCount) return;
        
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
        const editorRect = editorContainer.getBoundingClientRect();
        
        // Получаем текущую строку, где находится курсор
        const currentNode = range.startContainer;
        let currentParagraph = null;
        
        // Находим ближайший родительский элемент p, div, li, h1-h6
        let node = currentNode;
        while (node && node !== editorContainer) {
            if (node.nodeType === 1) { // Элемент
                const tagName = node.tagName.toLowerCase();
                if (tagName === 'p' || tagName === 'div' || tagName === 'li' || 
                    (tagName[0] === 'h' && tagName.length === 2 && !isNaN(tagName[1]))) {
                    currentParagraph = node;
                    break;
                }
            }
            node = node.parentNode;
        }
        
        // Если не нашли параграф, используем позицию курсора
        let cursorTop = rect.top - editorRect.top + editorContainer.scrollTop;
        
        // Если нашли параграф, используем его положение
        if (currentParagraph) {
            const paragraphRect = currentParagraph.getBoundingClientRect();
            cursorTop = paragraphRect.top - editorRect.top + editorContainer.scrollTop;
            cursorTop += paragraphRect.height / 2 - 12; // Центрируем по вертикали
        }
        
        // Проверяем, что позиция находится в видимой части редактора
        if (cursorTop < 0 || cursorTop > editorContainer.offsetHeight) {
            // Если курсор вне видимой области, скрываем кнопку
            plusButton.style.visibility = 'hidden';
            return;
        }
        
        // Устанавливаем кнопку слева от курсора, но внутри формы
        plusButton.style.top = `${cursorTop}px`;
        plusButton.style.left = '10px'; // Размещаем внутри формы слева
        
        // Добавляем визуальное разделение между курсором и кнопкой
        plusButton.style.position = 'absolute';
        plusButton.style.background = '#ffffff';
        plusButton.style.boxShadow = '0 1px 3px rgba(0,0,0,0.15)';
        
        // Создаем визуальное разделение с помощью границы справа
        plusButton.style.borderRight = '2px solid #e1e5e9';
        plusButton.style.paddingRight = '5px';
        
        // Добавляем плавный переход
        plusButton.style.transition = 'top 0.15s ease, left 0.15s ease';
        
        // Показываем кнопку
        plusButton.style.visibility = 'visible';
    }
    
    // Обработчик изменений в редакторе
    editorContainer.addEventListener('input', function() {
        updateTextarea(textarea, editorContainer);
        handleCommandInput();
    });
    
    // Обработчик вставки изображений
    editorContainer.addEventListener('paste', function(e) {
        const items = e.clipboardData.items;
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                e.preventDefault();
                const file = items[i].getAsFile();
                insertImageFromFile(file, editorContainer);
            }
        }
    });
    
    // Обработчик перетаскивания изображений
    editorContainer.addEventListener('dragover', function(e) {
        e.preventDefault();
    });
    
    editorContainer.addEventListener('drop', function(e) {
        e.preventDefault();
        const files = e.dataTransfer.files;
        for (let i = 0; i < files.length; i++) {
            if (files[i].type.startsWith('image/')) {
                insertImageFromFile(files[i], editorContainer);
            }
        }
    });
    
    // Обработчик фокуса
    editorContainer.addEventListener('focus', function() {
        this.classList.add('focused');
    });
    
    editorContainer.addEventListener('blur', function() {
        this.classList.remove('focused');
        hideCommandMenu();
    });
    
    // Переменная для отслеживания последнего нажатия на "/"
    let lastSlashKeyTime = 0;
    
    // Обработчик клавиш
    editorContainer.addEventListener('keydown', function(e) {
        // Обработка команд через /
        if (e.key === '/') {
            // Проверка на двойное нажатие /
            const now = Date.now();
            if (now - lastSlashKeyTime < 500 || isProcessingCommand) {
                // Игнорируем, если прошло меньше 500мс с последнего нажатия
                // или если все еще обрабатывается предыдущая команда
                return;
            }
            lastSlashKeyTime = now;
            
            // Предотвращаем многократный вызов командного меню
            if (isCommandMenuOpen || commandMenu) {
                hideCommandMenu();
                return;
            }
            
            isProcessingCommand = true;
            setTimeout(() => {
                showCommandMenu();
                
                // Разблокируем через задержку
                setTimeout(() => {
                    isProcessingCommand = false;
                }, 300);
            }, 10);
            return;
        }
        
        if (commandMenu) {
            if (e.key === 'ArrowDown') {
                e.preventDefault();
                selectedCommandIndex = Math.min(selectedCommandIndex + 1, commandMenu.children.length - 1);
                updateCommandMenuSelection();
                scrollToSelectedItem();
            } else if (e.key === 'ArrowUp') {
                e.preventDefault();
                selectedCommandIndex = Math.max(selectedCommandIndex - 1, 0);
                updateCommandMenuSelection();
                scrollToSelectedItem();
            } else if (e.key === 'Enter') {
                e.preventDefault();
                executeSelectedCommand();
            } else if (e.key === 'Escape') {
                e.preventDefault();
                hideCommandMenu();
            }
        }
    });
    
    // Обработчик команд через /
    function handleCommandInput() {
        if (isProcessingCommand) return; // Блокируем, если уже обрабатываем команду
        
        const selection = window.getSelection();
        if (selection.rangeCount === 0) return;
        
        const range = selection.getRangeAt(0);
        const text = editorContainer.textContent;
        const cursorPos = range.startOffset;
        
        // Проверяем, есть ли команда в текущей строке
        const lineStart = text.lastIndexOf('\n', cursorPos - 1) + 1;
        const lineText = text.substring(lineStart, cursorPos);
        
        if (lineText.startsWith('/')) {
            // Защита от многократного вызова
            if (isCommandMenuOpen || commandMenu) {
                filterCommands(lineText);
                return;
            }
            
            currentCommand = lineText;
            isProcessingCommand = true;
            
            // Небольшая задержка перед показом меню
            setTimeout(() => {
                showCommandMenu();
                filterCommands(lineText);
                
                // Разблокируем через задержку
                setTimeout(() => {
                    isProcessingCommand = false;
                }, 300);
            }, 10);
        } else if (!lineText.includes('/')) {
            hideCommandMenu();
        }
    }
    
    function showCommandMenu() {
        if (commandMenu) return;
        
        commandMenu = document.createElement('div');
        commandMenu.className = 'command-menu';
        commandMenu.style.position = 'absolute';
        commandMenu.style.zIndex = '1000';
        
        // Позиционируем меню
        const rect = editorContainer.getBoundingClientRect();
        commandMenu.style.left = '20px';
        commandMenu.style.top = '80px';
        
        editorContainer.appendChild(commandMenu);
        
        // Показываем все команды
        commands.forEach((cmd, index) => {
            const item = createCommandMenuItem(cmd, index);
            commandMenu.appendChild(item);
        });
        
        selectedCommandIndex = 0;
        updateCommandMenuSelection();
    }
    
    function showCommandMenuForSelection() {
        if (commandMenu) return;
        
        commandMenu = document.createElement('div');
        commandMenu.className = 'command-menu';
        commandMenu.style.position = 'absolute';
        commandMenu.style.zIndex = '1000';
        
        // Позиционируем меню
        const rect = editorContainer.getBoundingClientRect();
        commandMenu.style.left = '20px';
        commandMenu.style.top = '80px';
        
        editorContainer.appendChild(commandMenu);
        
        // Показываем команды форматирования для выделенного текста
        const formatCommands = commands.filter(cmd => 
            ['bold', 'italic', 'underline', 'code', 'link', 'info', 'success', 'warning', 'danger'].includes(cmd.trigger.replace('/', ''))
        );
        
        formatCommands.forEach((cmd, index) => {
            const item = createCommandMenuItem(cmd, index);
            commandMenu.appendChild(item);
        });
        
        selectedCommandIndex = 0;
        updateCommandMenuSelection();
    }
    
    function createCommandMenuItem(cmd, index) {
        const item = document.createElement('button');
        item.className = 'command-menu-item';
        item.setAttribute('data-command', cmd.trigger);
        
        // Проверяем, находимся ли мы в темной теме
        const isDarkTheme = document.documentElement.getAttribute('data-bs-theme') === 'dark';
        const descriptionColor = isDarkTheme ? '#f8f9fa' : '#333333';
        const titleColor = isDarkTheme ? '#ffffff' : '#212529';
        
        item.innerHTML = `
            <div class="command-menu-item-icon">${cmd.icon}</div>
            <div class="command-menu-item-content">
                <div class="command-menu-item-title" style="color: ${titleColor};">${cmd.title}</div>
                <div class="command-menu-item-description" style="color: ${descriptionColor}; font-weight: 500;">${cmd.description}</div>
            </div>
        `;
        
        item.addEventListener('click', function() {
            executeCommand(cmd);
        });
        
        return item;
    }
    
    function updateCommandMenuSelection() {
        if (!commandMenu) return;
        
        const items = commandMenu.querySelectorAll('.command-menu-item');
        items.forEach((item, index) => {
            if (index === selectedCommandIndex) {
                item.classList.add('selected');
            } else {
                item.classList.remove('selected');
            }
        });
    }
    
    function scrollToSelectedItem() {
        if (!commandMenu) return;
        
        const items = commandMenu.querySelectorAll('.command-menu-item');
        const selectedItem = items[selectedCommandIndex];
        
        if (selectedItem) {
            selectedItem.scrollIntoView({
                behavior: 'smooth',
                block: 'nearest'
            });
        }
    }
    
    function filterCommands(query) {
        if (!commandMenu) return;
        
        // Создаем Set для исключения дубликатов
        const uniqueCommands = new Map();
        
        // Фильтруем команды
        const filteredCommands = commands.filter(cmd => 
            cmd.trigger.toLowerCase().includes(query.toLowerCase()) ||
            cmd.title.toLowerCase().includes(query.toLowerCase())
        );
        
        // Добавляем только уникальные команды (по trigger)
        filteredCommands.forEach(cmd => {
            if (!uniqueCommands.has(cmd.trigger)) {
                uniqueCommands.set(cmd.trigger, cmd);
            }
        });
        
        // Очищаем меню
        commandMenu.innerHTML = '';
        
        // Добавляем элементы меню
        Array.from(uniqueCommands.values()).forEach((cmd, index) => {
            const item = createCommandMenuItem(cmd, index);
            commandMenu.appendChild(item);
        });
        
        selectedCommandIndex = 0;
        updateCommandMenuSelection();
    }
    
    function executeSelectedCommand() {
        if (!commandMenu) return;
        
        const items = commandMenu.querySelectorAll('.command-menu-item');
        if (items[selectedCommandIndex]) {
            const cmd = commands.find(c => c.trigger === items[selectedCommandIndex].getAttribute('data-command'));
            if (cmd) {
                executeCommand(cmd);
            }
        }
    }
    
    function executeCommand(cmd) {
        hideCommandMenu();
        
        // Показываем подсказку о вызванной функции
        showFunctionTooltip(cmd.title);
        
        const selection = window.getSelection();
        const selectedText = selection.toString().trim();
        
        switch (cmd.trigger) {
            case '/h1':
                insertHeading(1, selectedText);
                break;
            case '/h2':
                insertHeading(2, selectedText);
                break;
            case '/h3':
                insertHeading(3, selectedText);
                break;
            case '/p':
                insertParagraph(selectedText);
                break;
            case '/ul':
                insertBulletList(selectedText);
                break;
            case '/ol':
                insertOrderedList(selectedText);
                break;
            case '/code':
                insertCodeBlock();
                break;
            case '/quote':
                insertQuote(selectedText);
                break;
            case '/bold':
                formatText('bold', selectedText);
                break;
            case '/italic':
                formatText('italic', selectedText);
                break;
            case '/underline':
                formatText('underline', selectedText);
                break;
            case '/link':
                insertLink(selectedText);
                break;
            case '/hr':
                insertHorizontalRule();
                break;
            case '/image':
                insertImageContainer();
                break;
            case '/gallery':
                insertGallery();
                break;
            case '/info':
                insertCallout('info');
                break;
            case '/success':
                insertCallout('success');
                break;
            case '/warning':
                insertCallout('warning');
                break;
            case '/danger':
                insertCallout('danger');
                break;
            case '/table':
                insertTable();
                break;
            case '/checklist':
                insertChecklist();
                break;
        }
        
        updateTextarea(textarea, editorContainer);
    }
    
    function insertHeading(level, text) {
        const heading = document.createElement(`h${level}`);
        
        if (window.getSelection().toString() || text) {
            // Используем выделенный текст или переданный параметр
            heading.textContent = text || window.getSelection().toString();
        } else {
            // Создаем пустой элемент и позиционируем курсор внутри
            heading.innerHTML = '<br>';
        }
        
        if (window.getSelection().toString()) {
            replaceSelection(heading);
        } else {
            insertAtCursor(heading);
        }
        
        // Помещаем курсор в начало заголовка
        setCaretToStart(heading);
    }
    
    function insertParagraph(text) {
        const p = document.createElement('p');
        
        if (window.getSelection().toString() || text) {
            // Используем выделенный текст или переданный параметр
            p.textContent = text || window.getSelection().toString();
        } else {
            // Создаем пустой параграф
            p.innerHTML = '<br>';
        }
        
        if (window.getSelection().toString()) {
            replaceSelection(p);
        } else {
            insertAtCursor(p);
        }
        
        // Помещаем курсор в начало параграфа
        setCaretToStart(p);
    }
    
    function insertBulletList(text) {
        const ul = document.createElement('ul');
        const li = document.createElement('li');
        
        if (window.getSelection().toString() || text) {
            // Используем выделенный текст или переданный параметр
            li.textContent = text || window.getSelection().toString();
        } else {
            // Создаем пустой элемент списка
            li.innerHTML = '<br>';
        }
        
        ul.appendChild(li);
        
        if (window.getSelection().toString()) {
            replaceSelection(ul);
        } else {
            insertAtCursor(ul);
        }
        
        // Помещаем курсор в начало элемента списка
        setCaretToStart(li);
    }
    
    function insertOrderedList(text) {
        const ol = document.createElement('ol');
        const li = document.createElement('li');
        
        if (window.getSelection().toString() || text) {
            // Используем выделенный текст или переданный параметр
            li.textContent = text || window.getSelection().toString();
        } else {
            // Создаем пустой элемент списка
            li.innerHTML = '<br>';
        }
        
        ol.appendChild(li);
        
        if (window.getSelection().toString()) {
            replaceSelection(ol);
        } else {
            insertAtCursor(ol);
        }
        
        // Помещаем курсор в начало элемента списка
        setCaretToStart(li);
    }
    
    // Функция для установки курсора в начало элемента
    function setCaretToStart(element) {
        const range = document.createRange();
        const selection = window.getSelection();
        
        // Если элемент пустой, создаем текстовый узел
        if (!element.firstChild) {
            const textNode = document.createTextNode('');
            element.appendChild(textNode);
        }
        
        // Устанавливаем диапазон в начало первого текстового узла
        const firstTextNode = element.firstChild;
        if (firstTextNode.nodeType === Node.TEXT_NODE) {
            range.setStart(firstTextNode, 0);
        } else {
            range.setStart(element, 0);
        }
        range.collapse(true);
        
        // Очищаем текущее выделение и устанавливаем новое
        selection.removeAllRanges();
        selection.addRange(range);
        
        // Обновляем позицию кнопки +
        setTimeout(() => {
            updatePlusButtonPosition();
        }, 50);
    }
    
    // Флаг для предотвращения множественного вызова insertCodeBlock
    let isCodeBlockBeingInserted = false;
    
    function insertCodeBlock() {
        // Предотвращаем множественный вызов
        if (isCodeBlockBeingInserted) {
            return;
        }
        
        isCodeBlockBeingInserted = true;
        
        const language = prompt('Язык кода (например, python, js):', 'text') || 'text';
        const wrapper = document.createElement('div');
        wrapper.className = 'pm-block pm-code';
        wrapper.innerHTML = `
            <div class="pm-code__header">
                <span class="pm-code__lang">${language}</span>
                <button type="button" class="pm-code__copy">Копировать</button>
            </div>
            <pre class="pm-code__body" contenteditable="true"><code class="language-${language}">/* Ваш код */</code></pre>
        `;
        wrapper.querySelector('.pm-code__copy').addEventListener('click', function() {
            const text = wrapper.querySelector('pre').innerText;
            navigator.clipboard.writeText(text);
            this.textContent = 'Скопировано';
            setTimeout(()=> this.textContent='Копировать', 1500);
        });
        insertAtCursor(wrapper);
        
        // Разблокируем через задержку
        setTimeout(() => {
            isCodeBlockBeingInserted = false;
        }, 1000);
    }
    
    function insertQuote(text) {
        const blockquote = document.createElement('blockquote');
        blockquote.textContent = text || 'Цитата';
        
        if (window.getSelection().toString()) {
            replaceSelection(blockquote);
        } else {
            insertAtCursor(blockquote);
        }
    }
    
    function formatText(format, text) {
        if (text) {
            const selection = window.getSelection();
            if (selection.rangeCount > 0) {
                const range = selection.getRangeAt(0);
                const span = document.createElement('span');
                
                switch (format) {
                    case 'bold':
                        span.innerHTML = `<strong>${text}</strong>`;
                        break;
                    case 'italic':
                        span.innerHTML = `<em>${text}</em>`;
                        break;
                    case 'underline':
                        span.innerHTML = `<u>${text}</u>`;
                        break;
                }
                
                range.deleteContents();
                range.insertNode(span);
                selection.removeAllRanges();
            }
        } else {
            // Если нет выделенного текста, вставляем тег
            const tag = format === 'bold' ? 'strong' : 
                       format === 'italic' ? 'em' : 'u';
            const element = document.createElement(tag);
            element.textContent = `выделенный текст`;
            insertAtCursor(element);
        }
    }
    
    function insertLink(text) {
        const url = prompt('Введите URL:', 'https://');
        if (url) {
            const a = document.createElement('a');
            a.href = url;
            a.textContent = text || url;
            a.target = '_blank';
            
            if (window.getSelection().toString()) {
                replaceSelection(a);
            } else {
                insertAtCursor(a);
            }
        }
    }
    
    function insertHorizontalRule() {
        const hr = document.createElement('hr');
        insertAtCursor(hr);
    }
    
    function insertImage() {
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = function(e) {
            const file = e.target.files[0];
            if (file) {
                insertImageFromFile(file, editorContainer);
            }
        };
        input.click();
    }

    // Флаг для предотвращения множественного вызова insertImageContainer
    let isImageContainerBeingInserted = false;
    
    function insertImageContainer() {
        // Предотвращаем множественный вызов
        if (isImageContainerBeingInserted) {
            return;
        }
        
        isImageContainerBeingInserted = true;
        
        const container = document.createElement('figure');
        container.className = 'pm-block pm-image';
        container.innerHTML = `
            <div class="pm-image__holder" contenteditable="false">Загрузите изображение…</div>
            <figcaption class="pm-image__caption" contenteditable="true">Подпись к изображению</figcaption>
        `;
        insertAtCursor(container);
        // сразу открыть файловый диалог
        const input = document.createElement('input');
        input.type = 'file';
        input.accept = 'image/*';
        input.onchange = (e)=>{
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = (ev)=>{
                const img = new Image();
                img.src = ev.target.result;
                img.alt = 'image';
                container.querySelector('.pm-image__holder').innerHTML = '';
                container.querySelector('.pm-image__holder').appendChild(img);
            };
            reader.readAsDataURL(file);
        };
        input.click();
        
        // Разблокируем через задержку
        setTimeout(() => {
            isImageContainerBeingInserted = false;
        }, 1000);
    }

    function insertGallery() {
        const gallery = document.createElement('div');
        gallery.className = 'pm-block pm-gallery';
        gallery.innerHTML = `
            <div class="pm-gallery__item" contenteditable="false"></div>
            <div class="pm-gallery__item" contenteditable="false"></div>
            <div class="pm-gallery__hint">Добавьте две картинки</div>
        `;
        insertAtCursor(gallery);
    }

    function insertCallout(kind) {
        const callout = document.createElement('div');
        callout.className = `pm-block pm-callout pm-callout--${kind}`;
        callout.setAttribute('contenteditable','false');
        callout.innerHTML = `
            <div class="pm-callout__icon"></div>
            <div class="pm-callout__content" contenteditable="true">Текст врезки (${kind})</div>
        `;
        insertAtCursor(callout);
    }

    function insertTable() {
        const table = document.createElement('div');
        table.className = 'pm-block pm-table';
        table.innerHTML = `
            <table>
                <thead>
                    <tr><th>Колонка 1</th><th>Колонка 2</th></tr>
                </thead>
                <tbody>
                    <tr><td>Ячейка</td><td>Ячейка</td></tr>
                </tbody>
            </table>`;
        insertAtCursor(table);
    }

    function insertChecklist() {
        const list = document.createElement('ul');
        list.className = 'pm-block pm-checklist';
        list.innerHTML = `
            <li><label><input type="checkbox"> Задача 1</label></li>
            <li><label><input type="checkbox"> Задача 2</label></li>
        `;
        insertAtCursor(list);
    }
    
    function insertImageFromFile(file, container) {
        const reader = new FileReader();
        reader.onload = function(e) {
            const img = document.createElement('img');
            img.src = e.target.result;
            img.style.maxWidth = '100%';
            img.style.height = 'auto';
            img.style.display = 'block';
            img.style.margin = '1em auto';
            img.style.borderRadius = '8px';
            img.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
            
            insertAtCursor(img);
            updateTextarea(textarea, container);
        };
        reader.readAsDataURL(file);
    }
    
    function insertAtCursor(element) {
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            range.insertNode(element);
            range.setStartAfter(element);
            range.setEndAfter(element);
            selection.removeAllRanges();
            selection.addRange(range);
        } else {
            editorContainer.appendChild(element);
        }
    }
    
    function replaceSelection(element) {
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            range.deleteContents();
            range.insertNode(element);
            range.setStartAfter(element);
            range.setEndAfter(element);
            selection.removeAllRanges();
            selection.addRange(range);
        }
    }
    
    function hideCommandMenu() {
        if (commandMenu) {
            commandMenu.remove();
            commandMenu = null;
            isCommandMenuOpen = false; // Сбрасываем флаг при закрытии меню
            
            // Разблокируем обработку команд через дополнительную задержку
            setTimeout(() => {
                isProcessingCommand = false;
            }, 200);
        }
    }
    
    // Функция для показа подсказки о вызванной функции как текста в редакторе
    function showFunctionTooltip(functionName) {
        // Удаляем предыдущую подсказку, если она есть
        const existingTooltip = editorContainer.querySelector('.function-tooltip');
        if (existingTooltip) {
            existingTooltip.remove();
        }
        
        // Создаем подсказку как текст в редакторе
        const tooltip = document.createElement('span');
        tooltip.className = 'function-tooltip';
        tooltip.textContent = `// Вызвана функция: ${functionName}`;
        tooltip.style.color = '#6c757d';
        tooltip.style.fontStyle = 'italic';
        tooltip.style.fontSize = '0.9em';
        tooltip.style.opacity = '0.7';
        tooltip.contentEditable = 'false';
        
        // Вставляем подсказку в начало текущего элемента
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const currentNode = range.startContainer;
            let currentElement = currentNode;
            
            // Находим ближайший элемент p, div, h1-h6
            while (currentElement && currentElement !== editorContainer) {
                if (currentElement.nodeType === 1) {
                    const tagName = currentElement.tagName.toLowerCase();
                    if (tagName === 'p' || tagName === 'div' || tagName === 'li' || 
                        (tagName[0] === 'h' && tagName.length === 2 && !isNaN(tagName[1]))) {
                        break;
                    }
                }
                currentElement = currentElement.parentNode;
            }
            
            if (currentElement) {
                // Вставляем подсказку в начало элемента
                currentElement.insertBefore(tooltip, currentElement.firstChild);
                
                // Добавляем пробел после подсказки
                const space = document.createTextNode(' ');
                currentElement.insertBefore(space, tooltip.nextSibling);
                
                // Устанавливаем курсор после подсказки
                const newRange = document.createRange();
                newRange.setStartAfter(space);
                newRange.collapse(true);
                selection.removeAllRanges();
                selection.addRange(newRange);
            }
        }
        
        // Добавляем обработчик для удаления подсказки при начале набора
        const removeTooltip = () => {
            if (tooltip.parentNode) {
                tooltip.remove();
            }
        };
        
        // Удаляем подсказку при начале ввода
        editorContainer.addEventListener('input', removeTooltip, { once: true });
        editorContainer.addEventListener('keydown', removeTooltip, { once: true });
    }
    
    function updateTextarea(textarea, editor) {
        enhanceVisualFeedback(editor);
        textarea.value = editor.innerHTML;
        const event = new Event('change', { bubbles: true });
        textarea.dispatchEvent(event);
        const inputEvent = new Event('input', { bubbles: true });
        textarea.dispatchEvent(inputEvent);
    }
    
    function enhanceVisualFeedback(editor) {
        // Проверяем, находимся ли мы в темной теме
        const isDarkTheme = document.documentElement.getAttribute('data-bs-theme') === 'dark';
        
        // Применяем стили к жирному тексту
        const boldElements = editor.querySelectorAll('strong, b');
        boldElements.forEach(el => {
            el.style.fontWeight = '600';
            el.style.color = isDarkTheme ? '#f8f9fa' : 'inherit';
        });
        
        // Применяем стили к курсиву
        const italicElements = editor.querySelectorAll('em, i');
        italicElements.forEach(el => {
            el.style.fontStyle = 'italic';
            el.style.color = isDarkTheme ? '#f8f9fa' : 'inherit';
        });
        
        // Применяем стили к подчеркнутому тексту
        const underlineElements = editor.querySelectorAll('u');
        underlineElements.forEach(el => {
            el.style.textDecoration = 'underline';
            el.style.textDecorationColor = '#007bff';
            el.style.textDecorationThickness = '2px';
            el.style.textUnderlineOffset = '2px';
            el.style.color = isDarkTheme ? '#f8f9fa' : 'inherit';
        });
        
        // Применяем стили к коду
        const codeElements = editor.querySelectorAll('code');
        codeElements.forEach(el => {
            if (isDarkTheme) {
                el.style.background = '#343a40';
                el.style.color = '#ffc107';
                el.style.border = '1px solid #495057';
            } else {
                el.style.background = '#f1f3f4';
                el.style.color = '#e83e8c';
                el.style.border = '1px solid #e1e5e9';
            }
            el.style.padding = '0.2rem 0.4rem';
            el.style.borderRadius = '0.25rem';
            el.style.fontFamily = 'JetBrains Mono, monospace';
            el.style.fontSize = '0.9em';
            el.style.fontWeight = '500';
        });
        
        // Применяем стили к ссылкам
        const linkElements = editor.querySelectorAll('a');
        linkElements.forEach(el => {
            el.style.color = '#007bff';
            el.style.textDecoration = 'none';
            el.style.borderBottom = '1px solid transparent';
        });
        
        // Применяем общий цвет ко всем элементам в темной теме
        if (isDarkTheme) {
            const allElements = editor.querySelectorAll('*');
            allElements.forEach(el => {
                if (!el.style.color || el.style.color === 'inherit') {
                    el.style.color = '#f8f9fa';
                }
            });
        }
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Автоматическая инициализация всех редакторов на странице
    const editors = document.querySelectorAll('.prosemirror-editor');
    editors.forEach(editor => {
        const widgetId = editor.id.replace('editor-', '');
        if (typeof initProseMirror === 'function') {
            initProseMirror(widgetId);
            console.log('ProseMirror editor initialized');
        } else {
            console.error('initProseMirror function not found');
        }
    });
    
    // Предотвращение удаления кнопки +
    document.addEventListener('keydown', function(e) {
        const selection = window.getSelection();
        if (selection && selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const container = range.commonAncestorContainer;
            
            // Проверяем, не выделена ли кнопка +
            const plusButtons = document.querySelectorAll('.block-menu__plus.non-removable');
            plusButtons.forEach(button => {
                if (container.contains(button) || button.contains(container)) {
                    // Если кнопка + находится внутри выделения, отменяем действие
                    e.preventDefault();
                    range.collapse(true); // Сбрасываем выделение
                    return false;
                }
            });
        }
    });
    
    // Восстановление кнопки + если она была удалена
    setInterval(function() {
        const editors = document.querySelectorAll('.prosemirror-editor-container');
        editors.forEach(editorContainer => {
            const editorId = editorContainer.querySelector('.prosemirror-editor').id;
            const plusId = editorId.replace('editor-', 'plus-');
            
            if (!document.getElementById(plusId)) {
                // Кнопка была удалена, восстанавливаем её
                const plusButton = document.createElement('button');
                plusButton.id = plusId;
                plusButton.className = 'block-menu__plus non-removable';
                plusButton.title = 'Добавить элемент';
                plusButton.style = `position: absolute; left: -30px; transform: translateY(-50%); 
                                    width: 24px; height: 24px; display: flex; align-items: center; 
                                    justify-content: center; background: white; border: 1px solid #e1e5e9; 
                                    color: #929ca5; cursor: pointer; z-index: 1000; opacity: 0.8; 
                                    border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); 
                                    pointer-events: auto !important;`;
                
                plusButton.innerHTML = '<svg class="svg-icon" fill="currentColor" height="16" viewBox="0 0 24 24" width="16">' +
                                       '<path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/></svg>';
                
                editorContainer.appendChild(plusButton);
                
                // Переинициализируем обработчики
                const widgetId = editorId.replace('editor-', '');
                initProseMirror(widgetId);
            }
        });
    }, 1000); // Проверяем каждую секунду
});