from libqtile.manager import Key, Click, Drag, Screen, Group
from libqtile.command import lazy
from libqtile import layout, bar, widget


mod = 'mod4'
liteblue = '0066FF'
litegreen = '009933'
keys = [
    Key([mod, "shift"], "Left", lazy.layout.decrease_ratio()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod, "shift"], "Right", lazy.layout.increase_ratio()),
    Key([mod, "shift"], "Tab", lazy.layout.previous()),
    Key([mod, "shift"], "j", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
    Key([mod, "shift"], "k", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod], "Left", lazy.group.prevgroup()),
    Key([mod], "Right", lazy.group.nextgroup()),
    Key([mod], "Tab", lazy.layout.next()),
    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod], "g", lazy.togroup()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "q", lazy.restart()),
    Key([mod], "space", lazy.nextlayout()),
    Key([mod], "Return", lazy.spawn('urxvt')),
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "BackSpace", lazy.spawn(
        "dmenu_run -i -b -fn 'monofur:pixelsize=16:antialias=true'"
        " -p 'Run' -nf '#ffffff' -nb '#202020'")),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

groups = []

for i in groups:
    keys.append(
        Key(["mod4"], i.name, lazy.group[i.name].toscreen())
    )
    keys.append(
        Key(["mod4", "shift"], i.name, lazy.window.togroup(i.name))
    )


layouts = [
    layout.Max(),
    layout.Stack(stacks=2),
    layout.Tile(ratio=0.25),
]

defaults = {'font': 'monofur', 'fontsize': 16}
screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    this_screen_border='0000FF',
                    borderwidth=2, padding=4, active=liteblue, **defaults),
                widget.Sep(),
                widget.Prompt(),
                widget.WindowName(
                    margin_x=6, foreground=liteblue, **defaults),
                widget.Mpd(host='entrecote', **defaults),
                widget.CPUGraph(
                    width=1000, graph_color=liteblue, fill_color='001188',
                    border_color='000000'),
                widget.Systray()
            ],
            28
        ),
    ),
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    this_screen_border='00FF00',
                    borderwidth=2, padding=4, active=litegreen, **defaults),
                widget.Sep(),
                widget.Prompt(),
                widget.WindowName(
                    margin_x=6, foreground=litegreen, **defaults),
                widget.MemoryGraph(
                    width=500, graph_color='22FF44', fill_color='118811',
                    border_color='000000'),
                widget.SwapGraph(
                    width=500, graph_color='FF2020', fill_color='881111',
                    border_color='000000'),
                widget.Clock(
                    '%H:%M %d/%m/%y', padding=6,
                    foreground=litegreen, **defaults),
            ],
        28
        )
    )
]

# change focus on mouse over
follow_mouse_focus = True


def main(qtile):
    from dgroups import DGroups, Match, simple_key_binder
    global mod

    groups = {
        'term': {'init': True,
                 'persist': True,
                 'spawn': 'urxvt',
                 'exclusive': True},
        'emacs': {'persist': True,
                  # 'spawn': 'emacs',
                  'exclusive': True},
        'www': {'init': True,
                'exclusive': True
                  # 'spawn': 'chromium'
            },
    }

    apps = [
        {'match': Match(
            wm_class=[
                'Guake.py', 'Xephyr',
                'MPlayer', 'Exe', 'Gnome-keyring-prompt'],
            wm_type=['dialog', 'utility', 'splash']), 'float': True},
        {'match': Match(wm_class=['Chromium-browser', 'Minefield'],
                        role=['browser']), 'group': 'www'},
        {'match': Match(wm_class=['URxvt']), 'group': 'term'},
        {'match': Match(wm_class=['Emacs']), 'group': 'emacs'}
    ]
    DGroups(qtile, groups, apps, simple_key_binder(mod))
