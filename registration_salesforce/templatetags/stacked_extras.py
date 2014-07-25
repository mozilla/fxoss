from django import template
register = template.Library()

@register.filter(name='is_correct_notes')
def is_correct_notes(value, language_code):
    if language_code.lower() in ('en', 'en-us'):
        notes_field = 'notes'
    else:
        notes_field = 'notes_%s' % language_code.replace('-', '_').strip().lower()
    if value == notes_field:
        return True
    else:
        return False

@register.filter(name='is_notes_field')
def is_notes_field(value):
    if value.strip().lower().startswith('notes'):
        return True
    else:
        return False

