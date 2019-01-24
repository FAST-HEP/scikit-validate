## Disk size report

| File | metric | value | ref value | diff |
|-----+--------+-------+-----------+------|
{% for metric in metrics -%}
| {{ metric['cmd']}} | {{ metric['name'] }} {% if metric['unit'] is not none -%} ({{ metric['unit'] }}) {%endif -%} | {{ '%.2f'| format(metric['value']) }} | {{ '%.2f'| format(metric['ref_value']) }} | {{ '%.2f'| format(metric['diff']) }} ({{ '%.2f'| format(metric['diff_pc']) }} %) |
{% endfor %}
