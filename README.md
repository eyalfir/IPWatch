# IPWatch 

A watches panel for IPython.

tested with IPython versions 1.2.1

* author: Eyal Firstenberg

This is a curses termnial utility to watch an active ipython kernel.

## Simple Setup

Start and ipython kernel with ``ipython kernel`` or ``ipython console``:

    $> ipython console
    Python 2.7.6 (default, Mar 22 2014, 22:59:56) 
    Type "yright", "credits" or "license" for more information.
    
    IPython 1.2.1 -- An enhanced Interactive Python.
    ?         -> Introduction and overview of IPython's features.
    %quickref -> Quick reference.
    help      -> Python's own help system.
    object?   -> Details about 'object', use 'object??' for extra details.
    
    In [1]: 

Then, using a different terminal start IPWatch:

    $> IPWatch

In your first terminal, you now have new global [urwid](http://urwid.org) widget called ``___top_widget``. Simply set ``___top_widget`` to any [box urwid](http://urwid.org/manual/widgets.html#box-flow-and-fixed-widgets) widget to have it displayed in the watch terminal.

That's it, you are done
