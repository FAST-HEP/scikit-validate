# Detailed validation report for {{job_name}}
{{table_of_contents}}
{% for name, values in distributions.items() -%}
{% if 'ks_statistic' in values -%}
## {{ name }} ({{"KS statistic: %0.3f; p-value: %0.3f" | format(values['ks_statistic'], values['pvalue'])}} - {{values['status']}}
{% else -%}
{% for vname, value in values.items() -%}
 {{vname}} {{value}}
{% endfor -%}
{% endif -%}
{% if values['status'] != 'success' -%}
[![image]({{values['image']}})]({{values['image']}})
{% endif -%}
{% endfor -%}
