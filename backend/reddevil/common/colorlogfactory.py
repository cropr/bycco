import colorlog

def c_factory(**kwargs):
    return colorlog.ColoredFormatter(
        fmt=kwargs['format'],
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red,bg_blue',
        },
        reset=True,
        style='%'        
    )