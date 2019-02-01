## Validation report
{% if validation -%}
| job | status | summary | details | mismatch |
|-----|:-------|:--------|--------:|----------|
{% for job, desc in validation.items() -%}
| {{ job }} | {{ desc['status'] }} | {{ desc['differ']|length }}/{{ desc['distributions']|length }} distributions differ {% if desc['unknown']-%}({{desc['unknown']|length}} unknown) {% endif -%}| [details]({{ desc['link_to_details'] }}) | {{ desc['differ'] | join(', ') }} {% if desc['unknown']-%} ({{ desc['unknown'] | join(', ') }}) {% endif -%} |
{% endfor -%}
{% endif -%}
