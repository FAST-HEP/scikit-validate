{% macro format_number(variable) -%}
{% if variable is number -%}{{ '%.2f'| format(variable) }} {% else -%} {{variable}} {% endif -%}
{%- endmacro -%}
## Performance report
{% if comparison -%}
| cmd | metric | value | ref value | diff | profile |
|-----|:-------|------:|----------:|-----:|--------:|
{% endif -%}
{% for cmd, metrics in comparison.items() -%}
{% for name, metric in metrics.items() -%}
| `{{ cmd }}` | {{ name | replace("_", "&#95;") }} {% if metric['unit'] -%} ({{ metric['unit'] }}) {%endif -%} | {{ format_number(metric['value']) }} | {{ format_number(metric['ref']) }} | {{ format_number(metric['diff']) }} ({{ format_number(metric['diff_pc']) }} %) {{metric['symbol']}} | {% if 'profile' in metric -%} [profile]({{metric['profile']}}) {% else -%} --- {% endif -%} |
{% endfor -%}
{% endfor %}
