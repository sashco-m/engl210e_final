from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from engl210e_final.auth import login_required

bp = Blueprint('tutorial', __name__)

# pages for
# - ethics statement
# - main text / login screen

# probably just return a page with a big blob of text that can be cycled through
# successfully performing the injection can lead to another page idk
# be sure to wrap the hell out of the input with try-except
