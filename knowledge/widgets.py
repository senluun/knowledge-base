from django.forms import widgets
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string


class ProseMirrorWidget(widgets.Textarea):
    """
    Кастомный виджет для ProseMirror редактора
    """
    template_name = 'widgets/prosemirror_widget.html'
    
    class Media:
        css = {
            'all': (
                '/static/css/prosemirror.css',
            )
        }
        js = (
            '/static/js/prosemirror-init.js',
        )
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'prosemirror-editor',
            'rows': 20,
            'cols': 80,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def render(self, name, value, attrs=None, renderer=None):
        if value is None:
            value = ''
        
        context = {
            'name': name,
            'value': value,
            'attrs': self.build_attrs(self.attrs, attrs),
            'widget_id': attrs.get('id', f'id_{name}') if attrs else f'id_{name}',
        }
        
        return mark_safe(render_to_string(self.template_name, context))


class ProseMirrorAdminWidget(ProseMirrorWidget):
    """
    Компактная версия ProseMirror виджета для админ панели
    """
    template_name = 'widgets/prosemirror_admin_widget.html'
    
    def __init__(self, attrs=None):
        default_attrs = {
            'class': 'prosemirror-editor prosemirror-admin',
            'rows': 15,
            'cols': 80,
        }
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)