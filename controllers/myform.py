def index():
    # not much to do here
    return dict()


def process():
    # process the form
    # Note request.vars.firstname matches the name of the input
    # field in the form.
    firstname = request.vars.firstname

    return dict(fname=firstname)
