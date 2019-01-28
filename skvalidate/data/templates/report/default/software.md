## Software versions
{% if versions -%}
| project | version | reference version |
|---------+---------+-------------------|
{% endif -%}
{% for name, version in versions.items() -%}
| {{name}}  | {{version}} | {{ref_versions[name]}} |
{% endfor -%}
