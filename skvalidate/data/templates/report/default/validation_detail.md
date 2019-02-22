# {{ title }}
TODO: add table of contents
{% for name, values in summary['distributions'].items() -%}
# {{ name }} {{(KS statistic: {1:.3f}; p-value: {2:.3f}) | format(values['ks_statistic'], values['pvalue']) }}
[[!image]({{values['image']}})]({{values['image']}})
{% endfor -%}
