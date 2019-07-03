# This page provides an endpoint for getting an oauth redirect after an oauth verification process
def index():
    full_url = URL(args=request.args, vars=request.get_vars, host=True)
    return {'url': full_url}