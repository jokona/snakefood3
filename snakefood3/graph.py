"""
Read snakefood dependencies and output a visual graph.
"""
# This file is part of the Snakefood open source package.
# See http://furius.ca/snakefood/ for licensing details.

from typing import Mapping, Set
import jinja2

template = jinja2.Template(
    """
strict digraph "dependencies" {
    graph [
        {%- for key, value in graph_config.items() %}
            {{key}}="{{value}}"{% if not loop.last %},{% endif %}
        {%- endfor %}
        ]
    
       node [
        {%- for key, value in node_config.items() %}
            {{key}}={{value}},
        {%- endfor %}
       ];
    
{%- for edge in edges %}
    "{{edge.source}}" -> "{{edge.dist}}"
{%- endfor %}
}

"""
)

graph_config = {
    "rankdir": "LR",
    "overlap": "scale",
    "ratio": "fill",
    "fontsize": "16",
    "clusterrank": "local",
}
node_config = {
    "fontsize": 14,
    "shape": "ellipse",
    "fontname": "Consolas",
}


def graph(pairs: Mapping[str, Set[str]]) -> str:
    """Use predefined graphviz template to generate the dependency graph in dot language

    :param pairs: mapping of dependencies
    :return: string in dot language which defines the class dependencies
    """
    edges = []
    for key, value in pairs.items():
        if value:
            for v in value:
                edges.append({"source": v, "dist": key})
    return template.render(
        graph_config=graph_config,
        node_config=node_config,
        edges=edges,
    )
