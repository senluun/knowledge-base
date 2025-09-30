import re
import unicodedata
from django.utils.text import slugify as django_slugify


def slugify_cyrillic(text):
    """
    Создает slug с улучшенной поддержкой кириллицы
    """
    if not text:
        return ''
    
    # Расширенный словарь для транслитерации кириллицы в латиницу
    cyrillic_to_latin = {
        # Строчные буквы
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        # Заглавные буквы
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
        # Дополнительные символы
        '№': 'no', '—': '-', '–': '-', '«': '"', '»': '"', '"': '"', '"': '"',
        ''': "'", ''': "'", '…': '...', '•': '*', '→': '->', '←': '<-',
        '↑': 'up', '↓': 'down', '∞': 'infinity', '±': 'plus-minus',
        '×': 'x', '÷': '/', '≈': 'approx', '≠': 'not-equal', '≤': 'less-equal',
        '≥': 'greater-equal', '√': 'sqrt', '∑': 'sum', '∏': 'product',
        '∆': 'delta', 'π': 'pi', 'α': 'alpha', 'β': 'beta', 'γ': 'gamma',
        'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta', 'θ': 'theta',
        'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron',
        'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon', 'φ': 'phi',
        'χ': 'chi', 'ψ': 'psi', 'ω': 'omega'
    }
    
    # Транслитерация кириллицы и специальных символов
    result = ''
    for char in text:
        if char in cyrillic_to_latin:
            result += cyrillic_to_latin[char]
        else:
            result += char
    
    # Нормализация Unicode
    result = unicodedata.normalize('NFKD', result)
    
    # Удаление диакритических знаков и конвертация в ASCII
    result = result.encode('ascii', 'ignore').decode('ascii')
    
    # Замена пробелов и специальных символов на дефисы
    result = re.sub(r'[^\w\s-]', '', result)
    result = re.sub(r'[-\s]+', '-', result)
    
    # Удаление дефисов в начале и конце
    result = result.strip('-')
    
    # Приведение к нижнему регистру
    result = result.lower()
    
    # Ограничение длины (максимум 50 символов)
    if len(result) > 50:
        result = result[:50].rstrip('-')
    
    return result


def create_unique_slug(model, slug, instance=None):
    """
    Создает уникальный slug для модели
    """
    original_slug = slug
    counter = 1
    
    while model.objects.filter(slug=slug).exclude(pk=instance.pk if instance else None).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    return slug





from django.utils.text import slugify as django_slugify


def slugify_cyrillic(text):
    """
    Создает slug с улучшенной поддержкой кириллицы
    """
    if not text:
        return ''
    
    # Расширенный словарь для транслитерации кириллицы в латиницу
    cyrillic_to_latin = {
        # Строчные буквы
        'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo',
        'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm',
        'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u',
        'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
        # Заглавные буквы
        'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'Yo',
        'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M',
        'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U',
        'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Sch',
        'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya',
        # Дополнительные символы
        '№': 'no', '—': '-', '–': '-', '«': '"', '»': '"', '"': '"', '"': '"',
        ''': "'", ''': "'", '…': '...', '•': '*', '→': '->', '←': '<-',
        '↑': 'up', '↓': 'down', '∞': 'infinity', '±': 'plus-minus',
        '×': 'x', '÷': '/', '≈': 'approx', '≠': 'not-equal', '≤': 'less-equal',
        '≥': 'greater-equal', '√': 'sqrt', '∑': 'sum', '∏': 'product',
        '∆': 'delta', 'π': 'pi', 'α': 'alpha', 'β': 'beta', 'γ': 'gamma',
        'δ': 'delta', 'ε': 'epsilon', 'ζ': 'zeta', 'η': 'eta', 'θ': 'theta',
        'λ': 'lambda', 'μ': 'mu', 'ν': 'nu', 'ξ': 'xi', 'ο': 'omicron',
        'ρ': 'rho', 'σ': 'sigma', 'τ': 'tau', 'υ': 'upsilon', 'φ': 'phi',
        'χ': 'chi', 'ψ': 'psi', 'ω': 'omega'
    }
    
    # Транслитерация кириллицы и специальных символов
    result = ''
    for char in text:
        if char in cyrillic_to_latin:
            result += cyrillic_to_latin[char]
        else:
            result += char
    
    # Нормализация Unicode
    result = unicodedata.normalize('NFKD', result)
    
    # Удаление диакритических знаков и конвертация в ASCII
    result = result.encode('ascii', 'ignore').decode('ascii')
    
    # Замена пробелов и специальных символов на дефисы
    result = re.sub(r'[^\w\s-]', '', result)
    result = re.sub(r'[-\s]+', '-', result)
    
    # Удаление дефисов в начале и конце
    result = result.strip('-')
    
    # Приведение к нижнему регистру
    result = result.lower()
    
    # Ограничение длины (максимум 50 символов)
    if len(result) > 50:
        result = result[:50].rstrip('-')
    
    return result


def create_unique_slug(model, slug, instance=None):
    """
    Создает уникальный slug для модели
    """
    original_slug = slug
    counter = 1
    
    while model.objects.filter(slug=slug).exclude(pk=instance.pk if instance else None).exists():
        slug = f"{original_slug}-{counter}"
        counter += 1
    
    return slug


















