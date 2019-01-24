## Validation report
{% for name, desc in validation.items() %}
 - [{{name}}]({{desc['url']}}) ([ref]({{desc['ref_url']}}), [comparison]({{desc['comparison_url']}})): {% if desc['result'] -%} <span style="color:green">**OK**</span> {% else -%} <span style="color:red">**DIFFER**</span> {% endif -%}
{% endfor -%}
