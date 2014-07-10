(function ($, englishVersion) {
    function buildToolsLink() {
        var li, link;
        if (englishVersion.link && englishVersion.label) {
            link = $('<a>')
                .attr('href', englishVersion.link)
                .text(englishVersion.label);
            li = $('<li>').append(link);
            $('ul.object-tools', '#content-main').prepend(li);
        }
    }
    
    $(document).ready(function () {
        buildToolsLink();
    });
})(jQuery, englishVersion);
