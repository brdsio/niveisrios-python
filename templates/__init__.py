from web.template import CompiledTemplate, ForLoop


def index():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__ (cidades):
        for x in loop.setup(var):
            yield '', join_(escape_(x, True), '\n')
        yield '', join_('\n')
    return __template__

index = CompiledTemplate(index(), 'templates/index.html')


def status():
    loop = ForLoop()
    _dummy  = CompiledTemplate(lambda: None, "dummy")
    join_ = _dummy._join
    escape_ = _dummy._escape

    def __template__ (rios):
        yield '', join_(' \n')
        yield '', join_('<h3>Hist\xc3\xb3rico dos rios</h3>\n')
        yield '', join_('<ul>\n')
        for rio in loop.setup(rios):
            yield '', join_('<li>', escape_(rio.ds_estacao, True), '</li>\n')
        yield '', join_('</ul>\n')
        yield '', join_('\n')
    return __template__

status = CompiledTemplate(status(), 'templates/status.html')

