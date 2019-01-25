## Builds
{% if builds -%}
| name | status | info |
|------|:------:|:----:|
{% endif -%}
{% for name, build in builds.items() -%}
| {{name}} | {{build['status']}} | [log]({{build['link']}}) ([raw]({{build['link_raw']}})) |
{% endfor %}
