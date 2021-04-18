
# source: https://stackoverflow.com/a/54514410
def raise_if_outside_context(method):
    def decorator(self, *args, **kwargs):
        if not self.inside_context:
            raise Exception("This method should be called from inside context.")
        return method(self, *args, **kwargs)
    return decorator