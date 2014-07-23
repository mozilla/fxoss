class SetJustLoggedInCookieMiddleware(object):
    def process_response(self, request, response):
        """
        If the user just logged in, set a cookie for the JavaScript to
        read that signals this fact.

        The JavaScript will in turn send an event to GA to show that the
        user just logged in.
        """
        if getattr(request, 'just_logged_in', False):
            response.set_cookie('just_logged_in', 'true', httponly=False)
        return response
