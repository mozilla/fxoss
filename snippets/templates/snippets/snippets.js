var tinyMCETemplateList = [
    // Name, URL, Description
    {% for snippet in snippets %}
        ["{{ snippet.title }}", "{% url 'snippet-content' snippet.pk %}", "{{ snippet.description }}"]{% if not forloop.last %},{% endif %}
    {% endfor %}
];