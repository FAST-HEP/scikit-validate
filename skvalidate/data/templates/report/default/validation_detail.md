# Detailed validation report for {{job_name}}
{{table_of_contents}}

{% for name, values in distributions.items() -%}
## {{ name }} ({{"KS statistic: %0.3f; p-value: %0.3f" | format(values['ks_statistic'], values['pvalue'])}} - {{values['status']}}

{% if values['status'] != 'success' -%}
[![image]({{values['image']}})]({{values['image']}})
{% endif -%}

{% endfor -%}
