"Error views for IxStates."
import flask
from ixstates import util

blueprint = flask.Blueprint('ui.errors',  # pylint: disable=invalid-name
                            __name__)


@blueprint.app_errorhandler(403)
def handle_403(err):  # pylint: disable=unused-argument
    "Admin control panel page."
    return util.render_template_noredir("error_403.html"), 403
