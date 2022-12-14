__copyright__ = None
__version__ = None
__date__ = None


try:
    import bhamon_blog.__metadata__

    __copyright__ = bhamon_blog.__metadata__.__copyright__
    __version__ = bhamon_blog.__metadata__.__version__
    __date__ = bhamon_blog.__metadata__.__date__

except ImportError:
    pass
