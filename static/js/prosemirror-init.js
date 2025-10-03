// Блочный редактор с drag & drop и контекстными меню
// Исправленная версия без багов

function initProseMirror(widgetId) {
    const textarea = document.getElementById(widgetId);
    const editorContainer = document.getElementById(`editor-${widgetId}`);
    
    if (!textarea || !editorContainer) {
        console.error('Editor: Required elements not found');
        return;
    }
    
    // Очищаем предыдущие обработчики
    editorContainer.innerHTML = '';
    
    // Инициализация редактора
    editorContainer.innerHTML = textarea.value || '<div class="node node_paragraph is-empty" data-placeholder="Начните писать..."><p contenteditable="true" data-placeholder="Введите текст"></p></div>';
    editorContainer.setAttribute('data-placeholder', 'Начните писать...');
    editorContainer.setAttribute('contenteditable', 'true');
    
    // Инициализация блочной системы
    initializeBlockSystem(editorContainer, textarea);
    
    // Обработчики событий
    setupEventHandlers(editorContainer, textarea);
}

function initializeBlockSystem(editor, textarea) {
    // Добавляем классы для блочной системы
    editor.classList.add('prosemirror-editor-container');
    
    // Инициализируем существующие блоки
    initializeExistingBlocks(editor);
}

function initializeExistingBlocks(editor) {
    const blocks = editor.querySelectorAll('.node');
    blocks.forEach(block => {
        setupBlockControls(block);
    });
}

function setupBlockControls(block) {
    // Очищаем предыдущие контролы
    const existingControls = block.querySelectorAll('.node__drag-control, .right-menu__container, .block-menu__plus');
    existingControls.forEach(control => control.remove());
    
    // Проверяем, есть ли текст в блоке
    const hasText = block.textContent.trim().length > 0;
    
    // Добавляем/убираем класс is-empty
    if (hasText) {
        block.classList.remove('is-empty');
        // Если есть текст, добавляем drag handle и правое меню
        const dragControl = createDragControl();
        block.appendChild(dragControl);
        
        const rightMenu = createRightMenu(block);
        block.appendChild(rightMenu);
    } else {
        block.classList.add('is-empty');
        // Если нет текста, показываем только кнопку +
        const plusButton = createPlusButton(block);
        block.appendChild(plusButton);
    }
    
    // Настраиваем drag & drop
    setupDragAndDrop(block);
}

function createDragControl() {
    const dragControl = document.createElement('div');
    dragControl.className = 'node__drag-control';
    dragControl.setAttribute('contenteditable', 'false');
    dragControl.setAttribute('data-drag-handle', '');
    dragControl.setAttribute('draggable', 'true');
    
    dragControl.innerHTML = `
        <svg class="svg-icon" fill="currentColor" height="24" viewBox="0 0 20 20" width="24">
            <circle cx="8.5" cy="6.5" r="1.5"></circle>
            <circle cx="8.5" cy="12.5" r="1.5"></circle>
            <circle cx="8.5" cy="18.5" r="1.5"></circle>
            <circle cx="14.5" cy="6.5" r="1.5"></circle>
            <circle cx="14.5" cy="12.5" r="1.5"></circle>
            <circle cx="14.5" cy="18.5" r="1.5"></circle>
        </svg>
    `;
    
    return dragControl;
}

function createRightMenu(block) {
    const rightMenuContainer = document.createElement('div');
    rightMenuContainer.className = 'right-menu__container';
    rightMenuContainer.setAttribute('contenteditable', 'false');
    
    const dotsButton = document.createElement('button');
    dotsButton.className = 'node__dots button-icon';
    dotsButton.type = 'button';
    
    dotsButton.innerHTML = `
        <svg class="svg-icon" fill="currentColor" height="20" viewBox="0 0 20 20" width="20">
            <path fill-rule="evenodd" clip-rule="evenodd" d="M5 10C5 11.1046 4.10457 12 3 12C1.89543 12 1 11.1046 1 10C1 8.89543 1.89543 8 3 8C4.10457 8 5 8.89543 5 10ZM12 10C12 11.1046 11.1046 12 10 12C8.89543 12 8 11.1046 8 10C8 8.89543 8.89543 8 10 8C11.1046 8 12 8.89543 12 10ZM17 12C18.1046 12 19 11.1046 19 10C19 8.89543 18.1046 8 17 8C15.8954 8 15 8.89543 15 10C15 11.1046 15.8954 12 17 12Z"></path>
        </svg>
    `;
    
    const contextMenu = createContextMenu(block);
    rightMenuContainer.appendChild(dotsButton);
    rightMenuContainer.appendChild(contextMenu);
    
    // Обработчик клика на кнопку точек
    dotsButton.addEventListener('click', (e) => {
        e.stopPropagation();
        e.preventDefault();
        toggleContextMenu(contextMenu);
    });
    
    return rightMenuContainer;
}

function createContextMenu(block) {
    const contextMenu = document.createElement('div');
    contextMenu.className = 'context-menu right-menu';
    contextMenu.setAttribute('contenteditable', 'false');
    contextMenu.style.display = 'none';
    
    const blockType = getBlockType(block);
    const menuItems = getContextMenuItems(blockType);
    
    menuItems.forEach(item => {
        const wrapper = document.createElement('div');
        wrapper.className = 'context-menu__wrapper';
        
        if (item.type === 'separator') {
            const separator = document.createElement('hr');
            separator.className = 'context-menu__separator';
            wrapper.appendChild(separator);
        } else {
            const button = document.createElement('button');
            button.className = `context-menu__item right-menu__item ${item.active ? 'right-menu__item_active' : ''}`;
            button.type = 'button';
            button.setAttribute('data-item-type', item.type);
            
            button.innerHTML = `
                <svg class="svg-icon" fill="currentColor" height="20" viewBox="0 0 20 20" width="20">
                    ${item.icon}
                </svg>
                <span>${item.text}</span>
            `;
            
            button.addEventListener('click', (e) => {
                e.stopPropagation();
        e.preventDefault();
                handleContextMenuAction(block, item);
                hideContextMenu(contextMenu);
            });
            
            wrapper.appendChild(button);
        }
        
        contextMenu.appendChild(wrapper);
    });
    
    return contextMenu;
}

function getBlockType(block) {
    if (block.classList.contains('node_heading')) return 'heading';
    if (block.classList.contains('node_paragraph')) return 'paragraph';
    if (block.classList.contains('node_ul')) return 'ul';
    if (block.classList.contains('node_ol')) return 'ol';
    if (block.classList.contains('node_code')) return 'code';
    if (block.classList.contains('node_image')) return 'image';
    if (block.classList.contains('node_gallery')) return 'gallery';
    if (block.classList.contains('node_callout')) return 'callout';
    if (block.classList.contains('node_table')) return 'table';
    if (block.classList.contains('node_checklist')) return 'checklist';
    if (block.classList.contains('node_separator')) return 'separator';
    if (block.classList.contains('node_persona')) return 'persona';
    return 'paragraph';
}

function getContextMenuItems(blockType) {
    const baseItems = [
        {
            type: 'paragraph',
            text: 'Параграф',
            icon: '<path d="M19 5H5v2h14V5Zm0 4H5v2h14V9ZM5 13h14v2H5v-2Zm8 4H5v2h8v-2Z"></path>',
            active: blockType === 'paragraph'
        },
        {
            type: 'quote',
            text: 'Цитата',
            icon: '<path fill-rule="evenodd" clip-rule="evenodd" d="M14.024 4.00149C14.796 3.97849 15.561 4.22148 16.144 4.78045C16.715 5.32743 17 6.0104 17 6.83136C17 7.25434 16.926 7.70232 16.777 8.1743C16.628 8.64628 16.38 9.25525 16.033 10.0012L13.613 15H12.072L13.527 9.10326C13.5616 8.96326 12.7741 8.54925 12.4153 8.3606C12.3384 8.32019 12.2812 8.29012 12.256 8.2753C11.81 8.01331 11.389 7.58333 11.197 7.09635C10.992 6.57837 11.151 5.8944 11.417 5.43142C11.715 4.91145 12.207 4.51546 12.758 4.28247C13.162 4.11148 13.594 4.01549 14.024 4.00149ZM5.65494 4.2819C6.05894 4.11091 6.49095 4.01491 6.92095 4.00191C7.69295 3.97791 8.45796 4.2219 9.04096 4.78088C9.61197 5.32785 9.89697 6.01082 9.89697 6.83179C9.89697 7.25477 9.82297 7.70175 9.67397 8.17473C9.52497 8.64671 9.27596 9.25568 8.92996 10.0016L6.50995 14.9994H4.96794L6.42395 9.10369C6.45857 8.96355 5.66953 8.54819 5.31119 8.35956C5.23485 8.31937 5.17805 8.28948 5.15294 8.27472C4.70694 8.01273 4.28593 7.58375 4.09293 7.09678C3.88893 6.5778 4.04693 5.89483 4.31393 5.43085C4.61194 4.91087 5.10394 4.51489 5.65494 4.2819Z"></path>',
            active: blockType === 'quote'
        },
        { type: 'separator' },
        {
            type: 'delete',
            text: 'Удалить',
            icon: '<path fill-rule="evenodd" clip-rule="evenodd" d="M10 6H14V7H10V6ZM8 7V6C8 4.89543 8.89543 4 10 4H14C15.1046 4 16 4.89543 16 6V7H18H19C19.5523 7 20 7.44772 20 8C20 8.55228 19.5523 9 19 9H18V17C18 18.6569 16.6569 20 15 20H9C7.34315 20 6 18.6569 6 17V9H5C4.44772 9 4 8.55228 4 8C4 7.44772 4.44772 7 5 7H6H8ZM16 9H14H10H8V17C8 17.5523 8.44772 18 9 18H15C15.5523 18 16 17.5523 16 17V9ZM10 11.5C10 11.2239 10.2239 11 10.5 11C10.7761 11 11 11.2239 11 11.5V15.5C11 15.7761 10.7761 16 10.5 16C10.2239 16 10 15.7761 10 15.5V11.5ZM13.5 11C13.2239 11 13 11.2239 13 11.5V15.5C13 15.7761 13.7761 16 13.5 16C13.7761 16 14 15.7761 14 15.5V11.5C14 11.2239 13.7761 11 13.5 11Z"></path>'
        }
    ];
    
    return baseItems;
}

function createPlusButton(block) {
    const plusButton = document.createElement('button');
    plusButton.className = 'block-menu__plus';
    plusButton.type = 'button';
    plusButton.title = 'Добавить блок';
    
    plusButton.innerHTML = `
        <svg class="svg-icon" fill="currentColor" height="16" viewBox="0 0 24 24" width="16">
            <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z"/>
        </svg>
    `;
    
    plusButton.addEventListener('click', (e) => {
        e.stopPropagation();
        e.preventDefault();
        
        // Если блок пустой, создаем новый блок
        if (block.classList.contains('is-empty')) {
            createNewBlockAfter(block);
        } else {
            // Если блок не пустой, показываем меню
            showBlockMenu(block);
        }
    });
    
    // Добавляем обработчик для начала редактирования
    plusButton.addEventListener('mousedown', (e) => {
        // НЕ предотвращаем событие по умолчанию, чтобы можно было кликнуть в поле
        e.stopPropagation();
        
        // Находим редактируемый элемент в блоке
        const editableElement = block.querySelector('[contenteditable="true"]');
        if (editableElement) {
            // Фокусируемся на редактируемом элементе
            setTimeout(() => {
                editableElement.focus();
                
                // Устанавливаем курсор в начало
                const range = document.createRange();
                const sel = window.getSelection();
                range.setStart(editableElement, 0);
                range.collapse(true);
                sel.removeAllRanges();
                sel.addRange(range);
            }, 10);
        }
    });
    
    return plusButton;
}

function showBlockMenu(block) {
    // Закрываем все открытые меню
    document.querySelectorAll('.command-menu').forEach(menu => menu.remove());
    
    // Создаем меню выбора типа блока
    const menu = document.createElement('div');
    menu.className = 'command-menu';
    menu.style.position = 'absolute';
    menu.style.zIndex = '1001';
    
    // Позиционируем меню рядом с кнопкой +
    const rect = block.getBoundingClientRect();
    const editorRect = block.closest('.prosemirror-editor').getBoundingClientRect();
    
    menu.style.left = '50px';
    menu.style.top = `${rect.top - editorRect.top + 20}px`;
    
    const blockTypes = [
        { type: 'heading', title: 'Заголовок', description: 'Большой заголовок', icon: 'H' },
        { type: 'paragraph', title: 'Параграф', description: 'Обычный текст', icon: 'P' },
        { type: 'quote', title: 'Цитата', description: 'Блок цитаты', icon: '"' },
        { type: 'ul', title: 'Список', description: 'Маркированный список', icon: '•' },
        { type: 'ol', title: 'Нумерованный список', description: 'Пронумерованный список', icon: '1.' },
        { type: 'code', title: 'Код', description: 'Блок кода', icon: '</>' },
        { type: 'image', title: 'Изображение', description: 'Вставить изображение', icon: '🖼️' },
        { type: 'separator', title: 'Разделитель', description: 'Горизонтальная линия', icon: '—' }
    ];
    
    blockTypes.forEach(blockType => {
        const item = document.createElement('button');
        item.className = 'command-menu-item';
        item.innerHTML = `
            <div class="command-menu-item-icon">${blockType.icon}</div>
            <div class="command-menu-item-content">
                <div class="command-menu-item-title">${blockType.title}</div>
                <div class="command-menu-item-description">${blockType.description}</div>
            </div>
        `;
        
        item.addEventListener('click', (e) => {
            e.stopPropagation();
            e.preventDefault();
            createNewBlock(block, blockType.type);
            menu.remove();
        });
        
        menu.appendChild(item);
    });
    
    block.closest('.prosemirror-editor').appendChild(menu);
    
    // Закрываем меню при клике вне его
    setTimeout(() => {
        const closeMenu = (e) => {
            if (!menu.contains(e.target)) {
                menu.remove();
                document.removeEventListener('click', closeMenu);
            }
        };
        document.addEventListener('click', closeMenu);
    }, 100);
}

function createNewBlock(afterBlock, blockType) {
    const newBlock = createBlockElement(blockType);
    
    // Вставляем новый блок после текущего
    afterBlock.parentNode.insertBefore(newBlock, afterBlock.nextSibling);
    
    // Настраиваем контролы для нового блока
    setupBlockControls(newBlock);
    
    // Фокусируемся на новом блоке
    focusBlock(newBlock);
    
    // Обновляем textarea
    updateTextarea(afterBlock.closest('.prosemirror-editor'));
}

function createNewBlockAfter(block) {
    // Создаем новый параграф после текущего блока
    const newBlock = createBlockElement('paragraph');
    
    // Вставляем новый блок после текущего
    block.parentNode.insertBefore(newBlock, block.nextSibling);
    
    // Настраиваем контролы для нового блока
    setupBlockControls(newBlock);
    
    // Фокусируемся на новом блоке
    focusBlock(newBlock);
    
    // Обновляем textarea
    updateTextarea(block.closest('.prosemirror-editor'));
}

function createBlockElement(blockType) {
    const block = document.createElement('div');
    block.className = `node node_${blockType}`;
    block.dataset.blockId = Math.random().toString(36).substr(2, 9);
    
    switch (blockType) {
        case 'heading':
            block.innerHTML = `
                <div class="heading heading-1" data-empty-heading="Заголовок" contenteditable="true" style="outline: none; border: none; background: transparent;"></div>
            `;
                break;
        case 'paragraph':
            block.innerHTML = `
                <p contenteditable="true" data-placeholder="Введите текст" style="outline: none; border: none; background: transparent;"></p>
            `;
            break;
        case 'quote':
            block.innerHTML = `
                <blockquote contenteditable="true" data-placeholder="Введите цитату"></blockquote>
            `;
                break;
        case 'ul':
            block.innerHTML = `
                <ul>
                    <li contenteditable="true" data-placeholder="Элемент списка"></li>
                </ul>
            `;
                break;
        case 'ol':
            block.innerHTML = `
                <ol>
                    <li contenteditable="true" data-placeholder="Элемент списка"></li>
                </ol>
            `;
                break;
        case 'code':
            block.innerHTML = `
                <div class="node_code__header">
                    <span class="node_code__lang">text</span>
                    <button type="button" class="node_code__copy">Копировать</button>
                </div>
                <pre class="node_code__body" contenteditable="true"><code>/* Ваш код */</code></pre>
            `;
                break;
        case 'image':
            block.innerHTML = `
                <div class="node_image__holder" contenteditable="false">Загрузите изображение…</div>
                <div class="node_image__caption" contenteditable="true">Подпись к изображению</div>
            `;
                break;
        case 'separator':
            block.innerHTML = `
                <div class="separator"></div>
            `;
                break;
        }
        
    return block;
}

function setupDragAndDrop(block) {
    const dragHandle = block.querySelector('.node__drag-control');
    
    if (dragHandle) {
        dragHandle.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', '');
            e.dataTransfer.effectAllowed = 'move';
            block.classList.add('dragging');
            
            // Сохраняем данные о перетаскиваемом блоке
            e.dataTransfer.setData('text/html', block.outerHTML);
            e.dataTransfer.setData('application/x-block-id', block.dataset.blockId || Math.random().toString(36));
        });
        
        dragHandle.addEventListener('dragend', (e) => {
            block.classList.remove('dragging');
            
            // Убираем все классы drag-over
            document.querySelectorAll('.drag-over').forEach(el => {
                el.classList.remove('drag-over');
            });
        });
    }
    
    block.addEventListener('dragover', (e) => {
        e.preventDefault();
        e.dataTransfer.dropEffect = 'move';
        block.classList.add('drag-over');
    });
    
    block.addEventListener('dragleave', (e) => {
        // Проверяем, что мы действительно покидаем блок
        if (!block.contains(e.relatedTarget)) {
            block.classList.remove('drag-over');
        }
    });
    
    block.addEventListener('drop', (e) => {
        e.preventDefault();
        block.classList.remove('drag-over');
        
        const draggedBlockId = e.dataTransfer.getData('application/x-block-id');
        const draggedBlock = document.querySelector(`[data-block-id="${draggedBlockId}"]`);
        
        if (draggedBlock && draggedBlock !== block) {
            // Перемещаем блок
            const rect = block.getBoundingClientRect();
            const dropY = e.clientY;
            const blockCenter = rect.top + rect.height / 2;
            
            if (dropY < blockCenter) {
                // Вставляем перед текущим блоком
                block.parentNode.insertBefore(draggedBlock, block);
            } else {
                // Вставляем после текущего блока
                block.parentNode.insertBefore(draggedBlock, block.nextSibling);
            }
            
            // Обновляем textarea
            updateTextarea(block.closest('.prosemirror-editor'));
        }
    });
    
    // Добавляем обработчик для редактирования текста
    const editableElements = block.querySelectorAll('[contenteditable="true"]');
    editableElements.forEach(element => {
        element.addEventListener('focus', () => {
            // При фокусе на редактируемом элементе обновляем контролы
            setTimeout(() => {
                updateSingleBlockControls(block);
            }, 100);
        });
        
        element.addEventListener('blur', () => {
            // При потере фокуса обновляем контролы
            setTimeout(() => {
                updateSingleBlockControls(block);
            }, 100);
        });
        
        // Обработчик нажатия клавиш
        element.addEventListener('keydown', (e) => {
            // Enter в конце блока создает новый блок
            if (e.key === 'Enter') {
                const selection = window.getSelection();
                const range = selection.getRangeAt(0);
                const textNode = range.startContainer;
                
                // Проверяем, находимся ли мы в конце текста
                if (textNode.nodeType === Node.TEXT_NODE) {
                    const textLength = textNode.textContent.length;
                    const cursorPosition = range.startOffset;
                    
                    // Если курсор в конце текста, создаем новый блок
                    if (cursorPosition === textLength) {
                        e.preventDefault();
                        createNewBlockAfter(block);
                    }
                } else {
                    // Если это не текстовый узел, создаем новый блок
                    e.preventDefault();
                    createNewBlockAfter(block);
                }
            }
            
            // Escape для выхода из блока
            if (e.key === 'Escape') {
                element.blur();
            }
        });
    });
    
    // Добавляем обработчик для клика по блоку
    block.addEventListener('click', (e) => {
        // Если клик не по кнопке, фокусируемся на редактируемом элементе
        if (!e.target.closest('.block-menu__plus') && !e.target.closest('.node__drag-control') && !e.target.closest('.node__dots')) {
            const editableElement = block.querySelector('[contenteditable="true"]');
            if (editableElement) {
                editableElement.focus();
            }
        }
    });
    
    // Добавляем обработчик для двойного клика по блоку
    block.addEventListener('dblclick', (e) => {
        e.preventDefault();
        e.stopPropagation();
        
        // Находим редактируемый элемент в блоке
        const editableElement = block.querySelector('[contenteditable="true"]');
        if (editableElement) {
            // Фокусируемся на редактируемом элементе
            editableElement.focus();
            
            // Устанавливаем курсор в начало
            const range = document.createRange();
            const sel = window.getSelection();
            range.setStart(editableElement, 0);
            range.collapse(true);
            sel.removeAllRanges();
            sel.addRange(range);
        }
    });
}

function setupEventHandlers(editor, textarea) {
    // Обработчик изменений в редакторе
    editor.addEventListener('input', () => {
        updateTextarea(editor);
        updateBlockControls(editor);
    });
    
    // Обработчик фокуса
    editor.addEventListener('focus', function() {
        this.classList.add('focused');
    });
    
    editor.addEventListener('blur', function() {
        this.classList.remove('focused');
    });
    
    // Обработчик вставки изображений
    editor.addEventListener('paste', function(e) {
        const items = e.clipboardData.items;
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                e.preventDefault();
                const file = items[i].getAsFile();
                insertImageFromFile(file, editor);
            }
        }
    });
    
    // Обработчик перетаскивания изображений
    editor.addEventListener('dragover', function(e) {
        e.preventDefault();
    });
    
    editor.addEventListener('drop', function(e) {
        e.preventDefault();
        const files = e.dataTransfer.files;
        for (let i = 0; i < files.length; i++) {
            if (files[i].type.startsWith('image/')) {
                insertImageFromFile(files[i], editor);
            }
        }
    });
}

function updateBlockControls(editor) {
    const blocks = editor.querySelectorAll('.node');
    blocks.forEach(block => {
        updateSingleBlockControls(block);
    });
}

function updateSingleBlockControls(block) {
    const hasText = block.textContent.trim().length > 0;
    const hasDragControl = block.querySelector('.node__drag-control');
    const hasRightMenu = block.querySelector('.right-menu__container');
    const hasPlusButton = block.querySelector('.block-menu__plus');
    
    if (hasText) {
        // Если есть текст, убираем кнопку + и добавляем drag handle и меню
        block.classList.remove('is-empty');
        if (hasPlusButton) {
            hasPlusButton.remove();
        }
        if (!hasDragControl) {
            const dragControl = createDragControl();
            block.appendChild(dragControl);
        }
        if (!hasRightMenu) {
            const rightMenu = createRightMenu(block);
            block.appendChild(rightMenu);
        }
    } else {
        // Если нет текста, убираем drag handle и меню, добавляем кнопку +
        block.classList.add('is-empty');
        if (hasDragControl) {
            hasDragControl.remove();
        }
        if (hasRightMenu) {
            hasRightMenu.remove();
        }
        if (!hasPlusButton) {
            const plusButton = createPlusButton(block);
            block.appendChild(plusButton);
        }
    }
}

function handleContextMenuAction(block, action) {
    switch (action.type) {
        case 'delete':
            block.remove();
            updateTextarea(block.closest('.prosemirror-editor'));
            break;
        case 'paragraph':
            convertBlock(block, 'paragraph');
            break;
        case 'quote':
            convertBlock(block, 'quote');
            break;
        case 'heading':
            convertBlock(block, 'heading');
            break;
        case 'ul':
            convertBlock(block, 'ul');
            break;
        case 'ol':
            convertBlock(block, 'ol');
            break;
        case 'code':
            convertBlock(block, 'code');
            break;
        case 'image':
            convertBlock(block, 'image');
            break;
        case 'separator':
            convertBlock(block, 'separator');
            break;
    }
}

function convertBlock(block, newType) {
    const content = block.textContent;
    const newBlock = createBlockElement(newType);
    
    // Копируем содержимое
    const editableElement = newBlock.querySelector('[contenteditable="true"]');
    if (editableElement) {
        editableElement.textContent = content;
    }
    
    // Заменяем блок
    block.parentNode.replaceChild(newBlock, block);
    setupBlockControls(newBlock);
    focusBlock(newBlock);
    updateTextarea(newBlock.closest('.prosemirror-editor'));
}

function focusBlock(block) {
    const editableElement = block.querySelector('[contenteditable="true"]');
    if (editableElement) {
        editableElement.focus();
        
        // Устанавливаем курсор в начало
        const range = document.createRange();
        const selection = window.getSelection();
        range.selectNodeContents(editableElement);
        range.collapse(true);
            selection.removeAllRanges();
            selection.addRange(range);
    }
}

function toggleContextMenu(menu) {
    const isVisible = menu.style.display === 'block';
    
    // Закрываем все другие меню
    document.querySelectorAll('.context-menu').forEach(m => {
        m.style.display = 'none';
    });
    
    if (!isVisible) {
        menu.style.display = 'block';
    }
}

function hideContextMenu(menu) {
    menu.style.display = 'none';
}

function updateTextarea(editor) {
    const textarea = editor.parentNode.querySelector('textarea');
    if (textarea) {
        textarea.value = editor.innerHTML;
        
        const event = new Event('change', { bubbles: true });
        textarea.dispatchEvent(event);
    }
}

function insertImageFromFile(file, editor) {
    const reader = new FileReader();
    reader.onload = function(e) {
        // Создаем новый блок изображения
        const imageBlock = createBlockElement('image');
        const holder = imageBlock.querySelector('.node_image__holder');
        
        const img = document.createElement('img');
        img.src = e.target.result;
        img.style.maxWidth = '100%';
        img.style.height = 'auto';
        
        holder.innerHTML = '';
        holder.appendChild(img);
        
        // Вставляем блок в редактор
        editor.appendChild(imageBlock);
        setupBlockControls(imageBlock);
        updateTextarea(editor);
    };
    reader.readAsDataURL(file);
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Автоматическая инициализация всех редакторов на странице
    const editors = document.querySelectorAll('.prosemirror-editor');
    editors.forEach(editor => {
        const widgetId = editor.id.replace('editor-', '');
        if (typeof initProseMirror === 'function') {
            initProseMirror(widgetId);
            console.log('Block editor initialized');
        } else {
            console.error('initProseMirror function not found');
        }
    });
    
    // Закрытие контекстных меню при клике вне их
    document.addEventListener('click', function(e) {
        if (!e.target.closest('.context-menu') && !e.target.closest('.node__dots')) {
            document.querySelectorAll('.context-menu').forEach(menu => {
                menu.style.display = 'none';
            });
        }
    });
});
