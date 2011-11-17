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
    Key([mod, "shift"], "q", lazy.shutdown()),
    Key([mod, "shift"], "space", lazy.layout.rotate()),
    Key([mod], "Left", lazy.group.prevgroup()),
    Key([mod], "Right", lazy.group.nextgroup()),
    Key([mod], "Up", lazy.to_next_screen()),
    Key([mod], "Down", lazy.to_prev_screen()),
    Key([mod], "Tab", lazy.layout.next()),
    Key([mod], "f", lazy.window.toggle_floating()),
    Key([mod], "g", lazy.togroup()),
    Key([mod], "r", lazy.spawncmd()),
    Key([mod], "j", lazy.layout.up()),
    Key([mod], "k", lazy.layout.down()),
    Key([mod], "q", lazy.restart()),
    Key([mod], "l", lazy.spawn('alock -auth pam -bg blank')),
    Key([mod], "space", lazy.nextlayout()),
    Key([mod], "Return", lazy.spawn('urxvt')),
    Key([mod], "w", lazy.window.kill()),
    Key([mod], "BackSpace", lazy.spawn(
        "dmenu_run -i -b -fn 'monofur:pixelsize=16:antialias=true'"
        " -p 'Run' -nf '#ffffff' -nb '#202020'")),
    Key([mod], "XF86AudioPlay", lazy.spawn('mpc -h entrecote toggle')),
    Key([mod], "XF86AudioLowerVolume", lazy.spawn(
        'mpc -h entrecote volume -2')),
    Key([mod], "XF86AudioRaiseVolume", lazy.spawn(
        'mpc -h entrecote volume +2')),
]

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

layouts = [
    layout.Max(),
    layout.Stack(stacks=2),
    layout.Tile(ratio=0.25),
]

groups = []

defaults = {'font': 'monofur', 'fontsize': 12}
top_bar_heigth = 26
bottom_bar_heigth = 18
screens = [
    Screen(
        top=bar.Bar([
            widget.GroupBox(
                this_screen_border='0000FF',
                borderwidth=2, padding=4, active=liteblue, **defaults),
            widget.Prompt(foreground=liteblue, **defaults),
            widget.WindowName(
                margin_x=6, foreground=liteblue, **defaults),
            widget.Systray(),
            widget.Mpd(host='entrecote', **defaults)
        ], top_bar_heigth),
        bottom=bar.Bar([
            widget.CPUGraph(
                width=1920, graph_color=liteblue, fill_color='0000FF',
                samples=1000, frequency=0.1, border_color='000000'),
        ], bottom_bar_heigth)
    ),
    Screen(
        top=bar.Bar([
            widget.GroupBox(
                this_screen_border='00FF00',
                borderwidth=2, padding=4, active=litegreen, **defaults),
            widget.Prompt(),
            widget.WindowName(
                margin_x=6, foreground=litegreen, **defaults),
            widget.Clock(
                '%H:%M %d/%m/%y', padding=6,
                foreground=litegreen, **defaults),
        ], top_bar_heigth),
        bottom=bar.Bar([
            widget.MemoryGraph(
                width=1920, graph_color='22FF44', fill_color='118811',
                samples=1000, frequency=1, border_color='000000'),
        ], bottom_bar_heigth)
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
        'www': {'init': True,
                'exclusive': True
                # 'spawn': 'chromium'
            },
        'emacs': {'persist': True,
                  # 'spawn': 'emacs',
                  'exclusive': True},
    }

    apps = [
        {'match': Match(
            wm_class=['Xephyr'],
            wm_type=['dialog', 'utility', 'splash']), 'float': True},
        {'match': Match(wm_class=['Chromium-browser', 'Minefield'],
                        role=['browser']), 'group': 'www'},
        {'match': Match(wm_class=['URxvt']), 'group': 'term'},
        {'match': Match(wm_class=['Emacs']), 'group': 'emacs'}
    ]
    DGroups(qtile, groups, apps, simple_key_binder(mod))
