import falcon
import yaml

def get_version_from_request(req):
    """Attempt to extract the API version string."""
    for part in req.path.split('/'):
        if '.' in part and part.startswith('v'):
            return part
    return 'N/A'

def format_error_resp(req,
                      resp,
                      status_code=falcon.HTTP_500,
                      message="",
                      reason="",
                      error_type=None,
                      error_list=None,
                      info_list=None):
    """Generate a error message body and throw a Falcon exception to trigger
    an HTTP status.

    :param req: ``falcon`` request object.
    :param resp: ``falcon`` response object to update.
    :param status_code: ``falcon`` status_code constant.
    :param message: Optional error message to include in the body.
                    This should be the summary level of the error
                    message, encompassing an overall result. If
                    no other messages are passed in the error_list,
                    this message will be repeated in a generated
                    message for the output message_list.
    :param reason: Optional reason code to include in the body
    :param error_type: If specified, the error type will be used;
                       otherwise, this will be set to
                       'Unspecified Exception'.
    :param error_list: optional list of error dictionaries. Minimally,
                       the dictionary will contain the 'message' field,
                       but should also contain 'error': ``True``.
    :param info_list: optional list of info message dictionaries.
                      Minimally, the dictionary needs to contain a
                      'message' field, but should also have a
                      'error': ``False`` field.
    """

    if error_type is None:
        error_type = 'Unspecified Exception'

    # Since we're handling errors here, if error list is None, set up a default
    # error item. If we have info items, add them to the message list as well.
    # In both cases, if the error flag is not set, set it appropriately.
    if error_list is None:
        error_list = [{'message': 'An error occurred, but was not specified',
                       'error': True}]
    else:
        for error_item in error_list:
            if 'error' not in error_item:
                error_item['error'] = True

    if info_list is None:
        info_list = []
    else:
        for info_item in info_list:
            if 'error' not in info_item:
                info_item['error'] = False

    message_list = error_list + info_list

    error_response = {
        'kind': 'status',
        'apiVersion': get_version_from_request(req),
        'metadata': {},
        'status': 'Failure',
        'message': message,
        'reason': reason,
        'details': {
            'errorType': error_type,
            'errorCount': len(error_list),
            'messageList': message_list
        },
        'code': status_code,
        'retry': True if status_code is falcon.HTTP_500 else False
    }

    resp.body = yaml.safe_dump(error_response)
    resp.status = status_code


def default_exception_handler(ex, req, resp, params):
    """Catch-all execption handler for standardized output.

    If this is a standard falcon HTTPError
    """
    if isinstance(ex, falcon.HTTPError):
        # Allow the falcon http errors to bubble up and get handled.
        raise ex
    elif isinstance(ex, RetailStoreException):
        status_code = ex.code
        message = ex.message
    else:
        status_code = falcon.HTTP_500
        message = "Unhandled Exception raised: %s" % str(ex)

    format_error_resp(
        req,
        resp,
        status_code=status_code,
        error_type=ex.__class__.__name__,
        message=message
    )


class RetailStoreException(Exception):
    """Base RetailStore Exception."""

    msg_fmt = "An unknown exception occurred."
    code = falcon.HTTP_500

    def __init__(self, message=None, **kwargs):
        kwargs.setdefault('code', RetailStoreException.code)

        if not message:
            try:
                message = self.msg_fmt % kwargs
            except Exception:
                message = self.msg_fmt

        self.message = message
        super(RetailStoreException, self).__init__(message)

    def format_message(self):
        return self.args[0]


class LocationNotFound(RetailStoreException):
    """The Location cannot be found or doesn't exist."""

    msg_fmt = "The requested location=%(location_id)s was not found."
    code = falcon.HTTP_404
