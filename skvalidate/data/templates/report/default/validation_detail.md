# Detailed validation report for {{job_name}}
{{table_of_contents}}

## Overview

{% for subset in images | batch(overview_batch_size, '') -%}
{%for image in subset -%}{% if image -%}<a href="{{image}}"><img width="100" src="{{image}}" /></a>{% endif -%}{% endfor%}
{% if report_add_linebreaks -%}<br />{% endif -%}
{% endfor %}

<!---
{% for name, values in distributions.items() -%}
## {{ name }} ({{"KS statistic: %0.3f; p-value: %0.3f" | format(values['ks_statistic'], values['pvalue'])}} - {{values['status']}}

{% if values['status'] != 'success' -%}
[![image]({{values['image']}})]({{values['image']}})
{% endif -%}

{% endfor -%}
---!>
