
pipes
=====

{%- for pipe in pipes %}
- [{{pipe}}](#{{pipe}})
{%- endfor %}

{%- for pipe in pipes %}

{{pipe}}
----
{{pipes[pipe]["desc"]}}

### args
{%- if "args" not in pipes[pipe] or pipes[pipe]["args"] | length == 0 %}
None
{%- else %}
{%- for arg in pipes[pipe]["args"] %}
1. **{{arg}}**
{%- endfor %}
{%- endif %}

### kwds
{%- if "kwds" not in pipes[pipe] or pipes[pipe]["kwds"] | length == 0 %}
None
{%- else %}
{%- for kwd in pipes[pipe]["kwds"] %}
- **{{kwd}}**
{%- endfor %}
{%- endif %}

### docstring
{{ pipes[pipe]["func"].__doc__ }}

[top](#pipes)

<hr>
{%- endfor %}
