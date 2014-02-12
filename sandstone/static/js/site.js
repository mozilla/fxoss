(function() {
    var site = {
        platform: 'windows'
    };

    if(navigator.platform.indexOf("Win32") != -1 ||
       navigator.platform.indexOf("Win64") != -1) {
        site.platform = 'windows';
    }
    else if (navigator.platform.indexOf("armv7l") != -1) {
        site.platform = 'android';
    }
    else if(navigator.platform.indexOf("Linux") != -1) {
        site.platform = 'linux';
    }
    else if (navigator.userAgent.indexOf("Mac OS X") != -1) {
        site.platform = 'osx';
    }
    else if (navigator.userAgent.indexOf("MSIE 5.2") != -1) {
        site.platform = 'osx';
    }
    else if (navigator.platform.indexOf("Mac") != -1) {
        site.platform = 'mac';
    }
    else {
        site.platform = 'other';
    }

    function init() {
	// Add the platform as a classname on the html-element immediately to avoid lots
        // of flickering
	var h = document.documentElement;
	h.className = h.className.replace("windows", site.platform);

        // Add class to reflect javascript availability for CSS
        h.className = h.className.replace(/\bno-js\b/,'js');
    }

    init();
    window.site = site;
})();

/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

$(document).ready(function() {

    $('#sidebar')
        .focusin(function(e) { $('#sidebar').toggleClass('child-focus'); })
        .focusout(function(e) { $('#sidebar').toggleClass('child-focus'); });

    $('#sidebar nav ul li.has-children > a').click(function(e) {
        // e.preventDefault();

        var $li = $(this).parent('li');

        if ($li.hasClass('active')) {
            // close ul
            $(this).next()
                .slideUp('fast', function() {
                    $li.removeClass('active');
                });
        } else {
            $li.addClass('active');

            // open ul
            $(this).next('ul')
                .css('display', 'none')
                .slideDown('fast');

            // close siblings
            $li
                .siblings('li.has-children')
                .find('ul')
                .slideUp(
                    'fast',
                    function() {
                        $(this)
                            .parent('li')
                            .removeClass('active');
                    }
                );
        }

    });

});
