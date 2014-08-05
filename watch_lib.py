from urwid import Text, WidgetWrap, Filler, Columns, Pile

class WatchText(WidgetWrap):
    def __init__(self, factory, align='left', wrap='space', layout=None):
        self.factory = factory
        self.text = Text('', align=align, wrap=wrap, layout=layout)
        WidgetWrap.__init__(self, self.text)

    def render(self, size, focus=False):
        self.text.set_text(str(self.factory()))
        return super(WatchText, self).render(size, focus=focus)

class Watch(WidgetWrap):
    def __init__(self, name, factory):
        self.watch_name = name
        default = Columns([Filler(Text('%s '%self.watch_name, wrap='clip', align='right')), Filler(WatchText(factory, wrap='clip'))])
        WidgetWrap.__init__(self, default)

class WatchList(WidgetWrap):
    def __init__(self, globals_factory, watches=['wlib']):
        self.globals_factory = globals_factory
        self.pile = Pile([])
        for key in watches:
            self.add_key(key)
        WidgetWrap.__init__(self, self.pile)

    def get_watched_keys(self):
        return [x[0].watch_name for x in self.pile.contents]

    def remove_key(self, key):
        if key in self.get_watched_keys():
            self.pile.contents.remove([x for x in self.pile.contents if x[0].watch_name==key][0])
        else:
            raise KeyError('%s does not exist', key)

    def add_key(self, key):
        self.pile.contents.append((Watch(key, lambda:self.globals_factory().get(key, '%s does not exist'%key)), ('weight', 1)))

    def remove_all_keys(self):
        for key in self.get_watched_keys():
            self.remove_key(key)

    def set_keys(self, keys):
        self.remove_all_keys()
        for key in keys:
            self.add_key(key)

class WatchTextList(WidgetWrap):
    def __init__(self, factory, align='left'):
        self.factory = factory
        self.text = Text('', align=align)
        WidgetWrap.__init__(self, self.text)

    def render(self, size, focus=False):
        lines = [str(x)[:size[0]] for x in self.factory()][-size[1]:]
        if len(lines)<size[1]:
            lines = ['']*(size[1]-len(lines)) + lines
        self.text.set_text('\n'.join(lines))
        return super(WatchTextList, self).render((size[0],), focus=focus)

