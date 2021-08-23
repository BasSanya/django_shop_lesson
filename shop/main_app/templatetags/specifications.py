from django import template
from django.utils.safestring import mark_safe

from main_app.models import Smartphone

register = template.Library()

TABLE_HEAD = """
        <table class="table">
    <tbody>
"""

TABLE_TAIL = """
        </tbody>
    </table>
"""

TABLE_CONTENT = """
    <tr>
        <td>{name}</td>
        <td>{value}</td>
    </tr>
"""

PRODUCT_SPEC = {
    'notebook': {
        'Діагональ': 'diagonal',
        'Тип дисплею': 'display_type',
        'Частота процесора': 'processor_freq',
        'Оперативна пам\'ять': 'ram',
        'Відеокарта': 'video',
        'Час роботи від акамулятора': 'time_without_charge'
    },
    'smartphone': {
        'Діагональ': 'diagonal',
        'Тип дисплею': 'display_type',
        'Розрішення екрану': 'resolution',
        'Об\'єм акамулятора': 'accum_volume',
        'Оперативна пам\'ять': 'ram',
        'Наявність роз\'єму для SD карти памяті': 'sd',
        'Максимальний об\'єм карти пам\'яті': 'sd_volume_max',
        'Основна камера': 'main_cam_mp',
        'Фронтальна камера': 'frontal_cam_mp'
    },
}


def get_product_spec(product, model_name):
    table_content = ''
    for name, value in PRODUCT_SPEC[model_name].items():
        if name == 'Максимальний об\'єм карти пам\'яті' \
                and not getattr(product, PRODUCT_SPEC[model_name].get('Наявність роз\'єму для SD карти памяті')):
            continue
        table_content += TABLE_CONTENT.format(name=name, value=getattr(product, value))
    return table_content

@register.filter
def product_spec(product):
    model_name = product.__class__._meta.model_name

    return mark_safe(TABLE_HEAD + get_product_spec(product, model_name) + TABLE_TAIL)
