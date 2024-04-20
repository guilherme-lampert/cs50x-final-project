from flask import redirect, g, url_for
import re
import functools

def check_password(password):
    """Check if user password is valid"""

    regex = "^(?=.*?[0-9])(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^a-zA-Z0-9_]).{8,}$"

    if re.search(regex, password):
        return True

    return False


def login_required(view):
    """Decorator used in views that need a session"""

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        
        if not g.user:
            return redirect(url_for('auth.login'))

        return view(*args, **kwargs)

    return wrapped_view


def logoff_required(view):
    """Decorator used in views that can't have a session"""

    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        
        if g.user:
            return redirect(url_for('base.index'))

        return view(*args, **kwargs)

    return wrapped_view