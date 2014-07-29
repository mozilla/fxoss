from django import template
register = template.Library()

@register.filter(name='is_correct_notes')
def is_correct_notes(value, language_code):
    '''
        This filter is used to help determine the correct notes field to display
        Inputs:
            value --  the name of the notes field
            language_code -- the languauge code the template detects as defined
                             with {% get_current_language as LANGUAGE_CODE %} in
                             in template file located in inline/stacked.html
    '''
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
    '''
        This filter is used to determine if the parameter (value) passsed to it is
        a notes field
    '''
    if value.strip().lower().startswith('notes'):
        return True
    else:
        return False
