import urwid
import random
import time

def exit_on_q(key):
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()

progress = urwid.ProgressBar('pg normal', 'pg complete', 0, 100)
text = urwid.Text('Presiona "q" para salir.')
pile = urwid.Pile([text, progress])
fill = urwid.Filler(pile, 'top')

def update_progress(loop, user_data):
    current = progress.current
    increment = random.randint(1, 10)
    if current + increment > 100:
        progress.set_completion(100)
        text.set_text('Descarga completa! Presiona "q" para salir.')
        return
    progress.set_completion(current + increment)
    loop.set_alarm_in(0.5, update_progress)

loop = urwid.MainLoop(fill, unhandled_input=exit_on_q)
loop.set_alarm_in(0.5, update_progress)
loop.run()
