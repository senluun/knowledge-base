// Современный редактор в стиле Хабра
class HabrEditor {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        this.options = {
            placeholder: 'Начните писать...',
            minHeight: 400,
            ...options
        };
        
        this.init();
    }
    
    init() {
        this.createEditor();
        this.setupEventListeners();
        this.setupToolbar();
    }
    
    createEditor() {
        this.container.innerHTML = `
            <div class="habr-editor">
                <div class="habr-editor__header">
                    <div class="habr-editor__toolbar">
                        <button type="button" class="habr-editor__button" data-command="bold" title="Жирный">
                            <i class="fas fa-bold"></i>
                        </button>
                        <button type="button" class="habr-editor__button" data-command="italic" title="Курсив">
                            <i class="fas fa-italic"></i>
                        </button>
                        <button type="button" class="habr-editor__button" data-command="underline" title="Подчеркнутый">
                            <i class="fas fa-underline"></i>
                        </button>
                        <button type="button" class="habr-editor__button" data-command="strikeThrough" title="Зачеркнутый">
                            <i class="fas fa-strikethrough"></i>
                        </button>
                        
                        <div class="habr-editor__separator"></div>
                        
                        <button type="button" class="habr-editor__button" data-command="heading1" title="Заголовок 1">
                            <i class="fas fa-heading"></i>
                        </button>
                        <button type="button" class="habr-editor__button" data-command="heading2" title="Заголовок 2">
                            <i class="fas fa-heading" style="font-size: 0.8em;"></i>
                        </button>
                        <button type="button" class="habr-editor__button" data-command="heading3" title="Заголовок 3">
                            <i class="fas fa-heading" style="font-size: 0.6em;"></i>
                        </button>
                        
                        <div class="habr-editor__separator"></div>
                        
                        <button type="button" class="habr-editor__button" data-command="insertUnorderedList" title="Маркированный список">
                            <i class="fas fa-list-ul"></i>
                        </button>
                        <button type="button" class="habr-editor__button" data-command="insertOrderedList" title="Нумерованный список">
                            <i class="fas fa-list-ol"></i>
                        </button>
                        
                        <div class="habr-editor__separator"></div>
                        
                        <button type="button" class="habr-editor__button" data-command="createLink" title="Ссылка">
                            <i class="fas fa-link"></i>
                        </button>
                        <button type="button" class="habr-editor__button" data-command="insertImage" title="Изображение">
                            <i class="fas fa-image"></i>
                        </button>
                        <button type="button" class="habr-editor__button" data-command="insertCode" title="Код">
                            <i class="fas fa-code"></i>
                        </button>
                        <button type="button" class="habr-editor__button" data-command="insertQuote" title="Цитата">
                            <i class="fas fa-quote-left"></i>
                        </button>
                        
                        <div class="habr-editor__separator"></div>
                        
                        <button type="button" class="habr-editor__button" data-command="insertTable" title="Таблица">
                            <i class="fas fa-table"></i>
                        </button>
                        <button type="button" class="habr-editor__button" data-command="insertHorizontalRule" title="Разделитель">
                            <i class="fas fa-minus"></i>
                        </button>
                    </div>
                </div>
                <div class="habr-editor__content" 
                     contenteditable="true" 
                     data-placeholder="${this.options.placeholder}"
                     style="min-height: ${this.options.minHeight}px;">
                </div>
            </div>
        `;
        
        this.editor = this.container.querySelector('.habr-editor__content');
        this.toolbar = this.container.querySelector('.habr-editor__toolbar');
    }
    
    setupEventListeners() {
        // Обработчики для кнопок панели инструментов
        this.toolbar.addEventListener('click', (e) => {
            if (e.target.closest('.habr-editor__button')) {
                e.preventDefault();
                const button = e.target.closest('.habr-editor__button');
                const command = button.dataset.command;
                this.executeCommand(command);
            }
        });
        
        // Обработчики для области редактирования
        this.editor.addEventListener('input', () => {
            this.updateToolbar();
            this.triggerChange();
        });
        
        this.editor.addEventListener('keydown', (e) => {
            this.handleKeydown(e);
        });
        
        this.editor.addEventListener('paste', (e) => {
            this.handlePaste(e);
        });
        
        this.editor.addEventListener('focus', () => {
            this.updateToolbar();
        });
        
        this.editor.addEventListener('blur', () => {
            this.updateToolbar();
        });
    }
    
    setupToolbar() {
        this.updateToolbar();
    }
    
    executeCommand(command, value = null) {
        this.editor.focus();
        
        switch (command) {
            case 'bold':
            case 'italic':
            case 'underline':
            case 'strikeThrough':
                document.execCommand(command, false, null);
                break;
                
            case 'heading1':
                this.insertHeading(1);
                break;
            case 'heading2':
                this.insertHeading(2);
                break;
            case 'heading3':
                this.insertHeading(3);
                break;
                
            case 'insertUnorderedList':
            case 'insertOrderedList':
                document.execCommand(command, false, null);
                break;
                
            case 'createLink':
                this.createLink();
                break;
                
            case 'insertImage':
                this.insertImage();
                break;
                
            case 'insertCode':
                this.insertCode();
                break;
                
            case 'insertQuote':
                this.insertQuote();
                break;
                
            case 'insertTable':
                this.insertTable();
                break;
                
            case 'insertHorizontalRule':
                this.insertHorizontalRule();
                break;
        }
        
        this.updateToolbar();
        this.triggerChange();
    }
    
    insertHeading(level) {
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const heading = document.createElement(`h${level}`);
            
            if (range.collapsed) {
                heading.innerHTML = '<br>';
            } else {
                heading.innerHTML = range.toString();
                range.deleteContents();
            }
            
            range.insertNode(heading);
            
            // Устанавливаем курсор в заголовок
            const newRange = document.createRange();
            newRange.setStartAfter(heading);
            newRange.collapse(true);
            selection.removeAllRanges();
            selection.addRange(newRange);
        }
    }
    
    createLink() {
        const url = prompt('Введите URL ссылки:');
        if (url) {
            document.execCommand('createLink', false, url);
        }
    }
    
    insertImage() {
        const url = prompt('Введите URL изображения:');
        if (url) {
            const img = document.createElement('img');
            img.src = url;
            img.alt = 'Изображение';
            img.style.maxWidth = '100%';
            img.style.height = 'auto';
            
            const selection = window.getSelection();
            if (selection.rangeCount > 0) {
                const range = selection.getRangeAt(0);
                range.insertNode(img);
            }
        }
    }
    
    insertCode() {
        const code = prompt('Введите код:');
        if (code) {
            const pre = document.createElement('pre');
            const codeElement = document.createElement('code');
            codeElement.textContent = code;
            pre.appendChild(codeElement);
            
            const selection = window.getSelection();
            if (selection.rangeCount > 0) {
                const range = selection.getRangeAt(0);
                range.insertNode(pre);
            }
        }
    }
    
    insertQuote() {
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const blockquote = document.createElement('blockquote');
            
            if (range.collapsed) {
                blockquote.innerHTML = '<br>';
            } else {
                blockquote.innerHTML = range.toString();
                range.deleteContents();
            }
            
            range.insertNode(blockquote);
        }
    }
    
    insertTable() {
        const table = document.createElement('table');
        table.style.width = '100%';
        table.style.borderCollapse = 'collapse';
        table.style.border = '1px solid #e1e5e9';
        table.style.borderRadius = '6px';
        table.style.overflow = 'hidden';
        
        // Создаем заголовок таблицы
        const thead = document.createElement('thead');
        const headerRow = document.createElement('tr');
        for (let i = 0; i < 3; i++) {
            const th = document.createElement('th');
            th.textContent = `Заголовок ${i + 1}`;
            th.style.padding = '12px 16px';
            th.style.borderBottom = '1px solid #e1e5e9';
            th.style.background = '#f8f9fa';
            th.style.fontWeight = '600';
            headerRow.appendChild(th);
        }
        thead.appendChild(headerRow);
        table.appendChild(thead);
        
        // Создаем тело таблицы
        const tbody = document.createElement('tbody');
        for (let i = 0; i < 2; i++) {
            const row = document.createElement('tr');
            for (let j = 0; j < 3; j++) {
                const td = document.createElement('td');
                td.textContent = `Ячейка ${i + 1}-${j + 1}`;
                td.style.padding = '12px 16px';
                td.style.borderBottom = '1px solid #e1e5e9';
                row.appendChild(td);
            }
            tbody.appendChild(row);
        }
        table.appendChild(tbody);
        
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            range.insertNode(table);
        }
    }
    
    insertHorizontalRule() {
        const hr = document.createElement('hr');
        hr.style.border = 'none';
        hr.style.borderTop = '1px solid #e1e5e9';
        hr.style.margin = '1rem 0';
        
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            range.insertNode(hr);
        }
    }
    
    handleKeydown(e) {
        // Ctrl+B для жирного
        if (e.ctrlKey && e.key === 'b') {
            e.preventDefault();
            this.executeCommand('bold');
        }
        
        // Ctrl+I для курсива
        if (e.ctrlKey && e.key === 'i') {
            e.preventDefault();
            this.executeCommand('italic');
        }
        
        // Ctrl+K для ссылки
        if (e.ctrlKey && e.key === 'k') {
            e.preventDefault();
            this.executeCommand('createLink');
        }
    }
    
    handlePaste(e) {
        // Очищаем форматирование при вставке
        e.preventDefault();
        const text = e.clipboardData.getData('text/plain');
        document.execCommand('insertText', false, text);
    }
    
    updateToolbar() {
        const buttons = this.toolbar.querySelectorAll('.habr-editor__button');
        buttons.forEach(button => {
            const command = button.dataset.command;
            let isActive = false;
            
            switch (command) {
                case 'bold':
                case 'italic':
                case 'underline':
                case 'strikeThrough':
                    isActive = document.queryCommandState(command);
                    break;
                case 'insertUnorderedList':
                case 'insertOrderedList':
                    isActive = document.queryCommandState(command);
                    break;
            }
            
            button.classList.toggle('is-active', isActive);
        });
    }
    
    triggerChange() {
        const event = new CustomEvent('habr-editor-change', {
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
    
    setContent(html) {
        this.editor.innerHTML = html;
        this.updateToolbar();
    }
    
    setPlaceholder(placeholder) {
        this.editor.dataset.placeholder = placeholder;
    }
    
    focus() {
        this.editor.focus();
    }
    
    blur() {
        this.editor.blur();
    }
    
    destroy() {
        this.container.innerHTML = '';
    }
}

// Инициализация редактора
document.addEventListener('DOMContentLoaded', function() {
    // Автоматическая инициализация всех редакторов на странице
    const editorContainers = document.querySelectorAll('[data-habr-editor]');
    editorContainers.forEach(container => {
        const editor = new HabrEditor(container.id);
        
        // Связываем с textarea если есть
        const textarea = document.getElementById(container.dataset.textarea);
        if (textarea) {
            // Устанавливаем начальное содержимое
            if (textarea.value) {
                editor.setContent(textarea.value);
            }
            
            // Синхронизируем изменения
            editor.container.addEventListener('habr-editor-change', () => {
                textarea.value = editor.getHTML();
                
                // Триггерим событие change для textarea
                const event = new Event('change', { bubbles: true });
                textarea.dispatchEvent(event);
            });
        }
    });
});

