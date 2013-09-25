__version__ = '1.0.0'

def version():
    return __version__

def version_context_processor():
    return dict(version=__version__)
