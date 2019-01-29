## Pipeline summary
{% if pipeline -%}
Current pipeline: [{{pipeline}}]({{pipeline}})
{% endif %}

{% if jobs -%}
| name | status | log | software versions |
|------|:------:|:---:|:-----------------:|
{% endif -%}
{% for name, job in jobs.items() -%}
| {{name}} | {{job['status']}} | [log]({{job['link']}}) ([raw]({{job['link_raw']}})) | {{job['software_versions'] | join(', ')}} |
{% endfor %}
