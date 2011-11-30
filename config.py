from libqtile.manager import Key, Click, Drag, Screen, Group
from libqtile.command import lazy
from libqtile import layout, bar, widget
from socket import gethostname

hostname = gethostname()
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

groups = []

fonts = {'font': 'monofur', 'fontsize': 12}
fontcolors = fonts.copy()
green_fontcolors = fonts.copy()
fontcolors['foreground'] = liteblue
green_fontcolors['foreground'] = litegreen

layouts = [
    layout.Max(),
    layout.Stack(stacks=2),
    layout.Tile(ratio=0.25, border_normal='#000066', border_focus='#0000FF')
#    layout.TreeTab(**fontcolors),
#    layout.MonadTall(),
#    layout.Zoomy()
]

top_bar_heigth = 26
bottom_bar_heigth = 18
if hostname == 'ark':
    screens = [Screen(
        top=bar.Bar([
            widget.GroupBox(
                borderwidth=2, padding=4, active="0066FF",
                this_screen_border='0066FF.8', **fonts),
            widget.Prompt(**fontcolors),
            widget.WindowName(margin_x=6, **fontcolors),
            # widget.Mpd(host='arkr', **fontcolors),
            widget.CPUGraph(
                width=150, graph_color='0066FF', fill_color='0066FF.3',
                border_color='000000'),
            widget.MemoryGraph(
                width=150, graph_color='22FF44', fill_color='22FF44.3',
                border_color='000000'),
            widget.NetGraph(
                width=150, interface='wlan0',
                graph_color='FF2020', fill_color='FF2020.3',
                border_color='000000'),
            widget.Systray(),
            widget.CurrentLayout(**fontcolors),
            widget.Clock(
                '%H:%M %d/%m/%y', padding=6, **fontcolors
            )], 28),)]
else:
    screens = [
        Screen(
            top=bar.Bar([
                widget.GroupBox(
                    this_current_screen_border='0000ff',
                    this_screen_border='0000bb',
                    borderwidth=2, padding=4, active=liteblue, **fonts),
                widget.Prompt(**fontcolors),
                widget.WindowName(
                    margin_x=6, **fontcolors),
                widget.Systray(),
                widget.Mpd(host='entrecote', **fontcolors),
                widget.CurrentLayout(**fontcolors)
            ], top_bar_heigth, background="000000.1"),
            bottom=bar.Bar([
                widget.CPUGraph(
                    width=1920, graph_color=liteblue, fill_color='0000FF',
                    samples=1000, frequency=0.1, border_color='000000'
                )
            ], bottom_bar_heigth, background="000000.1")
        ),
        Screen(
            top=bar.Bar([
                widget.GroupBox(
                    this_current_screen_border='00ff00',
                    this_screen_border='00bb00',
                    borderwidth=2,
                    padding=4, active=litegreen, **fonts),
                widget.Prompt(),
                widget.WindowName(
                    margin_x=6, **green_fontcolors),
                widget.Clock(
                    '%H:%M %d/%m/%y', padding=6, **green_fontcolors),
                widget.CurrentLayout(**fontcolors)
            ], top_bar_heigth),
            bottom=bar.Bar([
                widget.MemoryGraph(
                    width=1920 / 2, graph_color='22FF44', fill_color='118811',
                    samples=1000, frequency=1, border_color='000000'),
                widget.NetGraph(
                    width=1920 / 2, graph_color='22FF99', fill_color='118855',
                    samples=1000, frequency=1, border_color='000000',
                    interface='eth0'),
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
                 'layout': 'tile',
                 # 'spawn': 'urxvt',
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
            wm_type=['dialog', 'utility', 'splash']),
         'float': True},
        {'match': Match(
            wm_class=['Chromium', 'Chromium-browser', 'Chrome', 'Minefield'],
            role=['browser']),
         'group': 'www'},
        {'match': Match(title=['Developer Tools']),
         'group': 'www-inspector'},
        {'match': Match(wm_class=['URxvt']),
         'group': 'term'},
        {'match': Match(wm_class=['Emacs']),
         'group': 'emacs'}
    ]
    DGroups(qtile, groups, apps, simple_key_binder(mod))
