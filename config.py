from libqtile.manager import Key, Click, Drag, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget

mod = 'mod4'
keys = [
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod], "q", lazy.restart()),
    Key([mod], "space", lazy.nextlayout()),
    Key([mod], "Tab", lazy.layout.next()),
    Key([mod, "shift"], "Tab", lazy.layout.previous()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod, "shift"], "Return", lazy.layout.toggle_split()),
    Key([mod, "shift"], "Right", lazy.layout.increase_ratio()),
    Key([mod, "shift"], "Left", lazy.layout.decrease_ratio()),
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "F2", lazy.spawn(
        "dmenu_run -i -fn 'monofur:pixelsize=16:antialias=true'"
        " -p 'Run' -nf '#ffffff' -nb '#202020'")),
    Key([mod, "shift"], "k", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([mod, "shift"], "j", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
    Key([mod], "g", lazy.togroup()),
    Key([mod], "Left", lazy.group.prevgroup()),
    Key([mod], "Right", lazy.group.nextgroup()),
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


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.GroupBox(
                    borderwidth=2, font='monofur', fontsize=14, padding=4,
                    active="0066FF"),
                widget.Sep(),
                widget.Prompt(),
                widget.WindowName(
                    font='monofur', fontsize=16, margin_x=6,
                    foreground="0066FF"),
                #widget.Mpd(fontsize=16),
                widget.CPUGraph(
                    width=150, graph_color='0066FF', fill_color='001188',
                    border_color='000000'),
                widget.MemoryGraph(
                    width=150, graph_color='22FF44', fill_color='118811',
                    border_color='000000'),
                widget.SwapGraph(
                    width=150, graph_color='FF2020', fill_color='881111',
                    border_color='000000'),
                widget.Systray(),
                widget.Clock(
                    '%H:%M %d/%m/%y', font='monofur', fontsize=18, padding=6,
                    foreground="0066FF"),
            ],
            28
        ),
    ),
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
        'www': {'exclusive': True
                  # 'spawn': 'chromium'
            },
    }

    apps = [
        {'match': Match(
            wm_class=[
                'Guake.py',
                'MPlayer', 'Exe', 'Gnome-keyring-prompt'],
            wm_type=['dialog', 'utility', 'splash']), 'float': True},
        {'match': Match(wm_class=['Chromium-browser', 'Minefield'],
                        role=['browser']), 'group': 'www'},
        {'match': Match(wm_class=['URxvt']), 'group': 'term'},
        {'match': Match(wm_class=['Emacs']), 'group': 'emacs'}
    ]
    DGroups(qtile, groups, apps, simple_key_binder(mod))
