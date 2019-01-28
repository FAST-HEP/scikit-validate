## Tests (TODO - dummy content)
{% if tests -%}
| name | status | info |
|------|:------:|:----:|
{% endif -%}
{% for name, test in tests.items() -%}
| {{name}} | {{test['status']}} | [log]({{test['link']}}) ([raw]({{test['link_raw']}})) |
{% endfor %}
