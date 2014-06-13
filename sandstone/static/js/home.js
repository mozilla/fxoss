;(function($) {
    'use strict';

    // Operator / Manufacturer Buttons
    var $mainContent = $('#main-content');
    var $options = $('input[name="role"]');
    var $buttons = $options.parents('.role-button');
    $options.prop('checked', false); // Ensure nothing is checked on launch.

    // Show different guide section when options change.
    $options.change(function() {
        $buttons.removeClass('selected');

        var $checkedOption = $options.filter(':checked');
        $checkedOption.parents('.role-button').addClass('selected');

        $mainContent.slideUp(400, function() {
            $('.home-guide').hide();
            $('#' + $checkedOption.attr('value') + '-guide').show();
            $mainContent.slideDown(400);
        });
    });

    // Hide guide when the close button is clicked.
    $('.guide-close').click(function(e) {
        e.preventDefault();
        $mainContent.slideUp(400);
        $options.prop('checked', false);
        $buttons.removeClass('selected');
    });
})(jQuery);
