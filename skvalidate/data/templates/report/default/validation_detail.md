# Detailed validation report for {{job_name}}
{{table_of_contents}}

## Overview
<details>
<summary>Distributions in disagreement with reference</summary>


{% for subset in images | batch(overview_batch_size, '') -%}
{%for image in subset -%}{% if image -%}<a href="{{image}}"><img width="100" src="{{image}}" /></a>{% endif -%}{% endfor%}
{% if report_add_linebreaks -%}<br />{% endif -%}
{% endfor %}

</details>
