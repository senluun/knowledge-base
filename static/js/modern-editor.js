/**
 * Современный блочный редактор
 */
class ModernEditor {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            placeholder: 'Начните писать...',
            minHeight: 400,
            ...options
        };
        
        this.createEditor();
        this.setupEventListeners();
    }
    
    createEditor() {
        this.container.innerHTML = `
            <div class="modern-editor">
                <div class="modern-editor__content" 
                     data-placeholder="${this.options.placeholder}"
                     style="min-height: ${this.options.minHeight}px; padding-left: 50px;">
                    <div class="modern-editor__block" data-block-type="paragraph">
                        <div class="modern-editor__drag-handle" draggable="true">
                            <i class="fas fa-grip-vertical"></i>
                        </div>
                        <div class="modern-editor__add-block" data-action="add-block">
                            <i class="fas fa-plus"></i>
                        </div>
                        <p contenteditable="true" data-placeholder="Начните писать..."></p>
                    </div>
                </div>
            </div>
        `;
        
        this.editor = this.container.querySelector('.modern-editor__content');
        this.blocks = this.editor.querySelectorAll('.modern-editor__block');
    }
    
    setupEventListeners() {
        // Обработчики для области редактирования
        this.editor.addEventListener('input', () => {
            this.triggerChange();
        });
        
        this.editor.addEventListener('keydown', (e) => {
            this.handleKeydown(e);
        });
        
        this.editor.addEventListener('paste', (e) => {
            this.handlePaste(e);
        });
        
        // Обработчики для блочной системы
        this.setupBlockListeners();
    }
    
    setupBlockListeners() {
        // Обработчики для кнопки добавления блока
        this.editor.addEventListener('click', (e) => {
            if (e.target.closest('.modern-editor__add-block')) {
                e.preventDefault();
                e.stopPropagation();
                console.log('Кнопка + нажата!');
                const addButton = e.target.closest('.modern-editor__add-block');
                const block = addButton.closest('.modern-editor__block');
                this.showBlockMenu(block);
            }
        });
        
        // Обработчики для drag handle
        this.editor.addEventListener('click', (e) => {
            if (e.target.closest('.modern-editor__drag-handle')) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
        
        // Обработчики для drag & drop
        this.editor.addEventListener('dragstart', (e) => {
            if (e.target.closest('.modern-editor__drag-handle')) {
                console.log('Начато перетаскивание блока');
                const block = e.target.closest('.modern-editor__block');
                if (!block.dataset.blockId) {
                    block.dataset.blockId = Math.random().toString(36).substr(2, 9);
                }
                block.classList.add('dragging');
                e.dataTransfer.setData('text/plain', '');
                e.dataTransfer.effectAllowed = 'move';
                e.dataTransfer.setData('application/x-block-id', block.dataset.blockId);
            }
        });
        
        this.editor.addEventListener('dragend', (e) => {
            if (e.target.closest('.modern-editor__drag-handle')) {
                const block = e.target.closest('.modern-editor__block');
                block.classList.remove('dragging');
                document.querySelectorAll('.drag-over').forEach(el => {
                    el.classList.remove('drag-over');
                });
            }
        });
        
        this.editor.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.dataTransfer.dropEffect = 'move';
            
            const block = e.target.closest('.modern-editor__block');
            if (block && !block.classList.contains('dragging')) {
                // Убираем класс drag-over с других блоков
                document.querySelectorAll('.drag-over').forEach(el => {
                    if (el !== block) {
                        el.classList.remove('drag-over');
                    }
                });
                block.classList.add('drag-over');
            }
        });
        
        this.editor.addEventListener('dragleave', (e) => {
            // Убираем drag-over только если покидаем блок полностью
            const block = e.target.closest('.modern-editor__block');
            if (!block || !block.contains(e.relatedTarget)) {
                document.querySelectorAll('.drag-over').forEach(el => {
                    el.classList.remove('drag-over');
                });
            }
        });
        
        this.editor.addEventListener('drop', (e) => {
            e.preventDefault();
            document.querySelectorAll('.drag-over').forEach(el => {
                el.classList.remove('drag-over');
            });
            
            const draggedBlockId = e.dataTransfer.getData('application/x-block-id');
            const draggedBlock = this.editor.querySelector(`[data-block-id="${draggedBlockId}"]`);
            const targetBlock = e.target.closest('.modern-editor__block');
            
            if (draggedBlock && targetBlock && draggedBlock !== targetBlock) {
                const rect = targetBlock.getBoundingClientRect();
                const dropY = e.clientY;
                const blockCenter = rect.top + rect.height / 2;
                
                if (dropY < blockCenter) {
                    targetBlock.parentNode.insertBefore(draggedBlock, targetBlock);
                } else {
                    targetBlock.parentNode.insertBefore(draggedBlock, targetBlock.nextSibling);
                }
                
                this.triggerChange();
            }
        });
    }
    
    handleKeydown(e) {
        // Enter создает новый блок
        if (e.key === 'Enter') {
            e.preventDefault();
            this.createNewBlockAfterCurrent();
        }
    }
    
    createNewBlockAfterCurrent() {
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const currentBlock = range.startContainer.closest('.modern-editor__block');
            
            if (currentBlock) {
                // Получаем текст после курсора
                const afterCursor = range.extractContents();
                const textAfterCursor = afterCursor.textContent;
                
                // Создаем новый блок
                const newBlock = this.createBlockElement('paragraph');
                currentBlock.parentNode.insertBefore(newBlock, currentBlock.nextSibling);
                
                // Если есть текст после курсора, перемещаем его в новый блок
                if (textAfterCursor.trim()) {
                    const editableElement = newBlock.querySelector('[contenteditable="true"]');
                    if (editableElement) {
                        editableElement.textContent = textAfterCursor;
                    }
                }
                
                this.focusBlock(newBlock);
                this.triggerChange();
            }
        }
    }
    
    handlePaste(e) {
        // Обрабатываем вставку текста - создаем новые блоки для каждой строки
        e.preventDefault();
        const text = e.clipboardData.getData('text/plain');
        const lines = text.split('\n');
        
        if (lines.length > 1) {
            // Если несколько строк, создаем блоки для каждой
            const currentBlock = this.getCurrentBlock();
            if (currentBlock) {
                // Вставляем первую строку в текущий блок
                const firstLine = lines[0];
                if (firstLine.trim()) {
                    document.execCommand('insertText', false, firstLine);
                }
                
                // Создаем блоки для остальных строк
                for (let i = 1; i < lines.length; i++) {
                    const newBlock = this.createBlockElement('paragraph');
                    currentBlock.parentNode.insertBefore(newBlock, currentBlock.nextSibling);
                    
                    if (lines[i].trim()) {
                        const editableElement = newBlock.querySelector('[contenteditable="true"]');
                        if (editableElement) {
                            editableElement.textContent = lines[i];
                        }
                    }
                }
                
                this.triggerChange();
            }
        } else {
            // Одна строка - обычная вставка
            document.execCommand('insertText', false, text);
        }
    }
    
    getCurrentBlock() {
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            return range.startContainer.closest('.modern-editor__block');
        }
        return null;
    }
    
    showBlockMenu(block) {
        // Закрываем все открытые меню
        document.querySelectorAll('.modern-editor__block-menu').forEach(menu => menu.remove());
        
        const menu = document.createElement('div');
        menu.className = 'modern-editor__block-menu show';
        menu.style.position = 'absolute';
        menu.style.zIndex = '1000';
        
        // Позиционируем меню
        const rect = block.getBoundingClientRect();
        const editorRect = this.editor.getBoundingClientRect();
        
        menu.style.left = '50px';
        menu.style.top = `${rect.top - editorRect.top + 20}px`;
        
        const blockTypes = [
            { type: 'heading', title: 'Заголовок', icon: 'H' },
            { type: 'quote', title: 'Цитата', icon: '"' },
            { type: 'list', title: 'Список', icon: '•' },
            { type: 'numbered-list', title: 'Нумерованный список', icon: '1.' },
            { type: 'code', title: 'Блок кода', icon: '</>' },
            { type: 'image', title: 'Изображение', icon: '🖼️' }
        ];
        
        blockTypes.forEach(blockType => {
            const item = document.createElement('button');
            item.className = 'modern-editor__block-menu-item';
            item.innerHTML = `
                <div class="modern-editor__block-menu-item-icon">${blockType.icon}</div>
                <div class="modern-editor__block-menu-item-text">${blockType.title}</div>
            `;
            
            item.addEventListener('click', (e) => {
                e.stopPropagation();
                e.preventDefault();
                this.createBlock(block, blockType.type);
                menu.remove();
            });
            
            menu.appendChild(item);
        });
        
        this.editor.appendChild(menu);
        
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
    
    createBlock(afterBlock, blockType) {
        const newBlock = this.createBlockElement(blockType);
        
        // Вставляем новый блок после текущего
        afterBlock.parentNode.insertBefore(newBlock, afterBlock.nextSibling);
        
        // Фокусируемся на новом блоке
        this.focusBlock(newBlock);
        
        this.triggerChange();
    }
    
    createBlockElement(blockType) {
        const block = document.createElement('div');
        block.className = 'modern-editor__block';
        block.dataset.blockType = blockType;
        block.dataset.blockId = Math.random().toString(36).substr(2, 9);
        
        const dragHandle = document.createElement('div');
        dragHandle.className = 'modern-editor__drag-handle';
        dragHandle.draggable = true;
        dragHandle.innerHTML = '<i class="fas fa-grip-vertical"></i>';
        
        const addButton = document.createElement('div');
        addButton.className = 'modern-editor__add-block';
        addButton.dataset.action = 'add-block';
        addButton.innerHTML = '<i class="fas fa-plus"></i>';
        
        let content;
        switch (blockType) {
            case 'heading':
                content = '<h2 contenteditable="true" data-placeholder="Заголовок">Заголовок</h2>';
                break;
            case 'quote':
                content = '<blockquote contenteditable="true" data-placeholder="Цитата">Цитата</blockquote>';
                break;
            case 'list':
                content = '<ul><li contenteditable="true" data-placeholder="Элемент списка">Элемент списка</li></ul>';
                break;
            case 'numbered-list':
                content = '<ol><li contenteditable="true" data-placeholder="Элемент списка">Элемент списка</li></ol>';
                break;
            case 'code':
                content = '<pre><code contenteditable="true" data-placeholder="Введите код...">Введите код...</code></pre>';
                break;
            case 'image':
                content = '<div class="image-placeholder" contenteditable="false" style="min-height: 200px; border: 2px dashed #ccc; display: flex; align-items: center; justify-content: center; color: #666;">Нажмите для загрузки изображения</div>';
                break;
            default:
                content = '<p contenteditable="true" data-placeholder="Начните писать..."></p>';
        }
        
        // Создаем контент без лишних элементов
        const contentDiv = document.createElement('div');
        contentDiv.innerHTML = content;
        
        // Очищаем от лишних input элементов
        const inputs = contentDiv.querySelectorAll('input, textarea');
        inputs.forEach(input => input.remove());
        
        block.appendChild(dragHandle);
        block.appendChild(contentDiv);
        block.appendChild(addButton);
        
        return block;
    }
    
    focusBlock(block) {
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
    
    triggerChange() {
        const event = new CustomEvent('modern-editor-change', {
            detail: {
                content: this.getContent(),
                html: this.getHTML()
            }
        });
        this.container.dispatchEvent(event);
    }
    
    getContent() {
        return this.editor.textContent;
    }
    
    getHTML() {
        return this.editor.innerHTML;
    }
    
    setContent(content) {
        this.editor.innerHTML = content;
        this.triggerChange();
    }
}

// Инициализация редактора
document.addEventListener('DOMContentLoaded', function() {
    // Автоматическая инициализация всех редакторов на странице
    const editorContainers = document.querySelectorAll('[data-modern-editor]');
    editorContainers.forEach(container => {
        const editor = new ModernEditor(container.id);
        
        // Связываем с textarea если есть
        const textarea = document.getElementById(container.dataset.textarea);
        if (textarea) {
            // Устанавливаем начальное содержимое
            if (textarea.value) {
                editor.setContent(textarea.value);
            }
            
            // Синхронизируем изменения
            editor.container.addEventListener('modern-editor-change', () => {
                textarea.value = editor.getHTML();
                
                // Триггерим событие change для textarea
                const event = new Event('change', { bubbles: true });
                textarea.dispatchEvent(event);
            });
        }
    });
});