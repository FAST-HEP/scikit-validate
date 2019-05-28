## Validation report
{% if validation -%}
| job | status | summary | details | mismatch |
|-----|:-------|:--------|--------:|----------|
{% for job, desc in validation.items() -%}
| {{ job }} | {{ desc['status'] }} | {{ desc['differ']|length }}/{{ desc['distributions']|length }} distributions differ {% if desc['unknown']-%}({{desc['unknown']|length}} unknown){% endif -%} {% if desc['error']-%}({{desc['error']|length}} errors){% endif -%}| [details]({{ desc['web_url_to_details'] }}) | <details><summary>Display the names of the {{ desc['differ']|length }} differing distributions</summary> {{ desc['differ'] | join(', ') }} {% if desc['unknown']-%} ({{ desc['unknown'] | join(', ') }}) {% endif -%} {% if desc['error']-%} (**{{ desc['error'] | join(', ') }}**) {% endif -%}</details>|
{% endfor -%}
{% endif -%}
