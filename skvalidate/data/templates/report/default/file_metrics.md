## Disk size report
{% if comparison -%}
| File | metric | value | ref value | diff |
|------|:-------|------:|----------:|-----:|
{% endif -%}
{% for cmd, metrics in comparison.items() -%}
{% for name, metric in metrics.items() -%}
| `{{ cmd }}` | {{ name | replace("_", "&#95;") }} {% if metric['unit'] -%} ({{ metric['unit'] }}) {%endif -%} | {{ '%.2f'| format(metric['value']) }} | {{ '%.2f'| format(metric['ref']) }} | {{ '%.2f'| format(metric['diff']) }} ({{ '%.2f'| format(metric['diff_pc']) }} %) {{metric['symbol']}} |
{% endfor -%}
{% endfor %}
