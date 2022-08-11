from django import template

register = template.Library()


@register.filter(name='accordition_id')
def get_accordition_id(counter):
    digits = {
        1: 'One', 2: 'Two', 3: 'Three', 4: 'Four', 5: 'Five', 6: 'Six', 7: 'Seven', 8: 'Eight', 9: 'Nine', 0: 'Ten'
    }

    return digits.get(counter)
