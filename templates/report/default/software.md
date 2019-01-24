## Software versions

| project | version | reference version |
|-----+--------+-------+-----------+------|
{% for name, version in versions.items() -%}
| {{name}}  | {{version}} | {{ref_versions[name]}} |
{% endfor -%}
