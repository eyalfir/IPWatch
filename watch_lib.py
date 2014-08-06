from urwid import Text, WidgetWrap, Filler, Columns, Pile, LineBox, Overlay, SolidFill

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
        key_widget = Text('%s'%self.watch_name, wrap='clip', align='left')
        default = Columns([('pack', key_widget), (3, Text(' = ')), WatchText(factory, wrap='clip')])
        WidgetWrap.__init__(self, Filler(default))

class WatchList(WidgetWrap):
    def __init__(self, watches=None, title=None):
        """watches is a list of tuples - (name, factory)"""
        watches = watches or []
        self.pile = Pile([])
        for key, factory in watches:
            self.add_watch(key, factory)
        if title:
            overlay = Overlay(self.pile, SolidFill(' '), align='center', width=('relative', 100), valign='middle', height=('relative', 100), left=1, right=1)
            widget = LineBox(overlay, title=title)
        else:
            widget = self.pile
        WidgetWrap.__init__(self, widget)

    def add_watch(self, key, factory):
        self.pile.contents.append((Watch(key, factory), ('given', 1)))

    def remove_all_watches(self):
        for watch in list(self.pile.contents):
            self.pile.contents.remove(watch)

    def get_watches(self):
        return [x[0].watch_name for x in self.pile.contents]

    def remove_watch(self, key):
        if key in self.get_watches():
            self.pile.contents.remove([x for x in self.pile.contents if x[0].watch_name == key][0])
        else:
            raise KeyError('%s does not exist', key)

class WatchDict(WidgetWrap):
    def __init__(self, dict_factory, keys=None, title=None):
        keys = keys or []
        self.dict_factory = dict_factory
        self.default = WatchList(title=title)
        for key in keys:
            self.add_key(key)
        WidgetWrap.__init__(self, self.default)

    def remove_key(self, key):
        self.default.remove_watch(key)

    def add_key(self, key):
        factory = lambda: self.dict_factory().get(key, '%s does not exist'%key)
        self.default.add_watch(key, factory)

    def remove_all_keys(self):
        self.default.remove_all_watches()

    def set_keys(self, keys):
        self.remove_all_keys()
        for key in keys:
            self.add_key(key)

class WatchObject(WatchDict):

    def __init__(self, object_factory, title=True):
        self.object_factory = object_factory
        self.keys = []
        super(WatchObject, self).__init__(lambda: object_factory().__dict__, self.keys, title=title)

    def _get_object_keys(self):
        return [x for x in self.object_factory().__dict__.keys() if x[0] != '_']

    def render(self, size, focus=False):
        new_keys = self._get_object_keys()
        if new_keys != self.keys:
            self.remove_all_keys()
            self.keys = new_keys
            for key in new_keys:
                self.add_key(key)
        return super(WatchObject, self).render(size, focus)


class WatchTextList(WidgetWrap):
    def __init__(self, factory, align='left'):
        self.factory = factory
        self.text = Text('', align=align)
        WidgetWrap.__init__(self, self.text)

    def render(self, size, focus=False):
        lines = [str(x)[:size[0]] for x in self.factory()][-size[1]:]
        if len(lines) < size[1]:
            lines = ['']*(size[1]-len(lines)) + lines
        self.text.set_text('\n'.join(lines))
        return super(WatchTextList, self).render((size[0],), focus=focus)

