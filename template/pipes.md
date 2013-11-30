
pipes
=====

{%- for pipe in pipes %}
- [{{pipe["name"]}}](#{{pipe["name"]}})
{%- endfor %}

{%- for pipe in pipes %}

{{pipe["name"]}}
----
{{pipe["desc"]}}

### args
{%- if "args" not in pipe or pipe["args"] | length == 0 %}
None
{%- else %}
{%- for arg in pipe["args"] %}
{{loop.index}}. **{{arg}}**
{%- endfor %}
{%- endif %}

### kwds
{%- if "kwds" not in pipe or pipe["kwds"] | length == 0 %}
None
{%- else %}
{%- for kwd in pipe["kwds"] %}
- **{{kwd}}**
{%- endfor %}
{%- endif %}

### docstring
{{ pipe["func"].__doc__ }}

[top](#pipes)

---------------------

{%- endfor %}
