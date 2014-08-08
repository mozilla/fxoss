(function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
(i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
})(window,document,'script','//www.google-analytics.com/analytics.js','ga');

(function($, monster) {
    'use strict';

    var $doc = $(document.documentElement);
    var gaAccountCode = $doc.data('gaCode');
    if (gaAccountCode) {
        ga('create', gaAccountCode, 'auto');
        ga('send', 'pageview');
    }

    /*** Events ***************************************************************/
    var slug = $doc.data('pageSlug');

    // Site-wide events
    if (monster.get('just_logged_in') === 'true') {
        monster.remove('just_logged_in');
        ga('send', 'event', 'Login or Registration Interactions', 'User Logged In', 'Success');
    }

    // If there is no slug, we're done!
    if (!slug) {
        return;
    }

    // Index
    function homepageEvt(copy) {
        return function (e) {
            ga('send', 'event', 'Homepage Interactions', 'button click', copy, {
                'dimension1': copy
            });
        };
    }

    if (slug === 'index') {
        $doc.on('click', '#role-manufacturer', homepageEvt('I\'m a Manufacturer'));
        $doc.on('click', '#role-operator', homepageEvt('I\'m an Operator'));
    }

    // Learn & subpages
    if (slug.indexOf('learn') === 0) {
        $doc.on('click', 'a', function() {
            // Special-case for emails.
            var href = this.getAttribute('href');
            if (href === 'mailto:marketplace-inquiries@mozilla.com') {
                ga('send', 'event', '/learn interactions', 'email inquiry', 'marketplace-inquiries');
            } else if (href === 'mailto:marketplace-programs@mozilla.com') {
                ga('send', 'event', '/learn interactions', 'email inquiry', 'marketplace-programs');
            } else {
                ga('send', 'event', '/learn interactions', 'link click', href);
            }
        });
    }

    // Build & subpages
    if (slug.indexOf('build') === 0) {
        $doc.on('click', 'a', function() {
            ga('send', 'event', '/build interactions', 'link click', this.getAttribute('href'));
        });
    }

    // Market & subpages
    if (slug.indexOf('market') === 0) {
        $doc.on('click', 'a', function() {
            // Special-case for logged-out view.
            var href = this.getAttribute('href');
            if (href.indexOf('/accounts/signup') === 0) {
                ga('send', 'event', '/market interactions', 'partner with us link click', 'Register');
            } else if (href.indexOf('/accounts/login') === 0) {
                ga('send', 'event', '/market interactions', 'partner with us link click', 'Sign-in');
            } else {
                ga('send', 'event', '/market interactions', 'link click', href);
            }
        });

        // Contact form
        if (slug === 'market/contact-us') {
            $doc.on('submit', 'form', function() {
                ga('send', 'event', '/market interactions', 'Contact Us Form', 'Successfully Submitted', {
                    'dimension2': $('#id_field_6').val().join(','),
                    'dimension3': $('#id_field_7').val().join(',')
                });
            });
        }
    }

    // Maintain & subpages
    if (slug.indexOf('maintain') === 0) {
        $doc.on('click', 'a', function() {
            ga('send', 'event', '/maintain interactions', 'link click', this.getAttribute('href'));
        });
    }

    // Agreement page
    function agreementEvt(copy) {
        return function() {
            ga('send', 'event', '/market interactions', 'Prototype Agreement', copy);
        };
    }

    if (slug === 'download-agreement') {
        $doc.on('submit', '#agreement-form', agreementEvt('Agree'));
        $doc.on('click', '#cancel-agreement', agreementEvt('Cancel'));
        $doc.on('click', '#download-agreement-link', agreementEvt('Download'));
    }

    // Account signup
    if (slug === 'account-signup') {
        $doc.on('submit', 'form', function() {
            ga('send', 'event', 'Login or Registration Interactions', 'Register for Account',
               'Successfully Submitted', {
                'dimension2': $('#id_mobile_product_interest').val(),
                'dimension3': $('#id_type_of_device').val(),
                'dimension4': $('#id_industry').val()
            });
        });
    }
})(jQuery, monster);
