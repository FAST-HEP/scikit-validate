# C++ Code formatting check
Following C++ files changed w.r.t. target branch (`{{ target_branch }}`):
{% for f in changed_files -%}
  - {{ f }}
{%endfor %}


Found divergences w.r.t. configure code style, please apply
```bash
{{ cmd }} {{ path }} | git am
git commit -m 'applied C++ code style'
git push origin {{ source_branch }}
```


In the future, please use
```bash
clang-format -i <file you changed>
```
or corresponding plugin for your editor of choice.
