__version__ = None
__date__ = None
__copyright__ = None


try:
    import benjaminhamon_blog.__metadata__

    __version__ = benjaminhamon_blog.__metadata__.__version__
    __date__ = benjaminhamon_blog.__metadata__.__date__
    __copyright__ = benjaminhamon_blog.__metadata__.__copyright__

except ImportError:
    pass
