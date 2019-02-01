## Pipeline summary
{% if pipeline -%}
Current pipeline: [{{pipeline}}]({{pipeline}})
{% endif %}

{% if jobs -%}
| name | status | log | software versions |
|------|:------:|:---:|:-----------------:|
{% endif -%}
{% for name, job in jobs.items() -%}
| {{name}} | {{job['status']}} | [log]({{job['web_url']}}) ([raw]({{job['web_url_raw']}})) | {{job['software_versions'] | join(', ')}} |
{% endfor %}
