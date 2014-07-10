(function ($, englishVersion) {
    var popup = null;

    function openPopup() {
        if (popup === null || popup.closed) {
            popup = window.open(
                englishVersion.link,
                englishVersion.label,
                'height=800,width=800,resizable=yes,scrollbars=yes'
            );
        }
        popup.focus();
    }

    function buildLink() {
        return $('<a>')
            .attr('href', englishVersion.link)
            .text(englishVersion.label)
            .click(function (e) {
                e.preventDefault();
                openPopup();
            });
    }

    function buildToolsLink() {
        var link = buildLink(),
            li = $('<li>').append(link);
        $('ul.object-tools', '#content-main').prepend(li);
    }

    function buildFieldLink(name) {
        var id = 'id_' + name; 
            label = $('label[for="' + id + '"]'),
            link = link = buildLink();
        label.append('<br />').append(link);
    }
    
    $(document).ready(function () {
        if (englishVersion.link && englishVersion.label) {
            buildToolsLink();
            $.each(englishVersion.fields, function (i, name) {
                buildFieldLink(name);
            });
        }
    });

})(jQuery, englishVersion);
