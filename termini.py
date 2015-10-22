
import tkinter as tk
from os import system as cmd

import uinput as ui


class Application(tk.Tk):

    def __init__(self, master):
        super(Application, self).__init__(master)
        self.fullscreen = False
        self.term = Terminal(self, 320, 96)
        self.term.pack()
        self.kb = Keyboard(self, 320, 144, [(1, 3), (4, 6)], 1)
        self.kb.set_key_coords()
        row1 = [
            ('q', ui.KEY_Q),
            ('w', ui.KEY_W),
            ('e', ui.KEY_E),
            ('r', ui.KEY_R),
            ('t', ui.KEY_T),
            ('y', ui.KEY_Y),
            ('u', ui.KEY_U),
            ('i', ui.KEY_I),
            ('o', ui.KEY_O),
            ('p', ui.KEY_P),
        ]
        row2 = [
            ('a', ui.KEY_A),
            ('s', ui.KEY_S),
            ('d', ui.KEY_D),
            ('f', ui.KEY_F),
            ('g', ui.KEY_G),
            ('h', ui.KEY_H),
            ('j', ui.KEY_J),
            ('k', ui.KEY_K),
            ('l', ui.KEY_L),
        ]
        row3 = [
            ('123', 1),
            ('z', ui.KEY_Z),
            ('x', ui.KEY_X),
            ('c', ui.KEY_C),
            ('v', ui.KEY_V),
            ('b', ui.KEY_B),
            ('n', ui.KEY_N),
            ('m', ui.KEY_M),
            ('Ret', ui.KEY_ENTER),
        ]
        row4 = [
            ('1', ui.KEY_1),
            ('2', ui.KEY_2),
            ('3', ui.KEY_3),
            ('4', ui.KEY_4),
            ('5', ui.KEY_5),
            ('6', ui.KEY_6),
            ('7', ui.KEY_7),
            ('8', ui.KEY_8),
            ('9', ui.KEY_9),
            ('0', ui.KEY_0),
        ]
        row5 = [
            ('-', ui.KEY_MINUS),
            ('/', ui.KEY_SLASH),
            (':', None),
            (';', ui.KEY_SEMICOLON),
            ('(', ui.KEY_LEFTBRACE),
            (')', ui.KEY_RIGHTBRACE),
            ('$', ui.KEY_DOLLAR),
            ('&', None),
            ('@', ui.KEY_EMAIL),
            ('"', None),
        ]
        row6 = [
            ('ABC', 0),
            ('.', ui.KEY_DOT),
            (',', ui.KEY_COMMA),
            ('?', ui.KEY_QUESTION),
            ('!', None),
            ("'", ui.KEY_APOSTROPHE),
        ]
        self.kb.add_row(row1)
        self.kb.add_row(row2)
        self.kb.add_row(row3)
        self.kb.add_row(row4)
        self.kb.add_row(row5)
        self.kb.add_row(row6)
        self.device = Device(self)
        self.kb.pack()
        self.kb.render()
        self.bind("<F11>", self.toggle_fullscreen)
        #self.toggle_fullscreen()

    def toggle_fullscreen(self, event=None):
        self.fullscreen = not self.fullscreen
        self.attributes("-fullscreen", self.fullscreen)
        return

    def end_fullscreen(self, event):
        self.fullscreen = False
        self.attributes("-fullscreen", False)
        return


class Terminal(tk.Frame):

    def __init__(self, master, width, height):
        super(Terminal, self).__init__(master, width=width, height=height)
        self.width = width
        self.height = height
        wid = self.winfo_id()
        cmd('xterm -into %d -geometry -sb &' % wid)


class Keyboard(tk.Canvas):
    
    def __init__(self, master, width, height, row_ranges, curr_range):
        super(Keyboard, self).__init__(master, width=width, height=height)
        self.config(background='#ecf0f1')
        self.width = width
        self.height = height
        self.key_width = 32
        self.key_height = 48
        self.rows = []
        self.row_ranges = row_ranges
        self.curr_range = curr_range

        self.bind('<Button-1>', self.on_left_click)
        self.bind('<ButtonRelease-1>', self.on_left_release)
    
    def on_left_click(self, event):
        for key in self.get_keys():
            if key.is_around(event.x, event.y):
                key.pressed = True
                self.render()
                return
            else:
                key.pressed = False
        self.render()
        return

    def on_left_release(self, event):
        for key in self.get_keys():
            key.pressed = False
        self.render()
        return

    def add_row(self, couples):
        first_x = (self.width - len(couples) * self.key_width) / 2
        lower_range = (self.row_ranges[self.curr_range][0] - 1)
        upper_range = self.row_ranges[self.curr_range][1]
        first_y = len(self.rows[lower_range:upper_range]) * self.key_height
        new_row = []
        for i, couple in enumerate(couples):
            x = first_x + self.key_width * i
            y = first_y
            text = couple[0]
            event = couple[1]
            key = Key(self, text, event, x, y, self.key_width, self.key_height)
            new_row.append(key)
        self.rows.append(new_row)
        return

    def render(self):
        self.delete('all')
        for key in self.get_keys():
            key.render()
        return

    def get_keys(self):
        keys = []
        lower_range = (self.row_ranges[self.curr_range][0] - 1)
        upper_range = self.row_ranges[self.curr_range][1]
        for row in self.rows[lower_range:upper_range]:
            for key in row:
                keys.append(key)
        return keys

    def get_events(self):
        events = []
        for row in self.rows:
            for key in row:
                if key.event and not isinstance(key.event, int):
                    events.append(key.event)
        return events

    def set_key_coords(self):
        lower_range = (self.row_ranges[self.curr_range][0] - 1)
        upper_range = self.row_ranges[self.curr_range][1]
        for i, row in enumerate(self.rows):
            if lower_range <= i < upper_range:
                for key in row:
                    key.y = (i - lower_range) * self.key_height
            else:
                for key in row:
                    key.y = self.height
        return

    def set_keyboard(self, number):
        self.curr_range = number
        self.set_key_coords()
        self.render()
        return


class Key:

    def __init__(self, master, text, event, x, y, width, height):
        self.master = master
        self.text = text
        self.event = event
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.pressed = False
    
    def render(self):
        x2 = self.x + self.width
        y2 = self.y + self.height
        x_ave = self.x + self.width / 2
        y_ave = self.y + self.height / 2
        if not self.pressed:
            fill = '#ecf0f1'
        else:
            fill = '#95a5a6'
        self.master.create_rectangle(self.x, self.y, x2, y2, fill=fill)
        self.master.create_text(x_ave, y_ave, text='%s' % self.text)
        return

    def is_around(self, x, y):
        left_side = self.x
        right_side = self.x + self.width
        bottom_side = self.y + self.height
        top_side = self.y
        if x < left_side:
            return False
        elif x > right_side:
            return False
        elif y > bottom_side:
            return False
        elif y < top_side:
            return False
        else:
            if not isinstance(self.event, int):
                curr_x = self.master.winfo_pointerx()
                curr_y = self.master.winfo_pointery()
                term_x = self.master.winfo_rootx() + int(self.master.master.term.width / 2)
                term_y = self.master.winfo_rooty() - int(self.master.master.term.height / 2)
                self.master.master.device.emit(ui.ABS_X, term_x)
                self.master.master.device.emit(ui.ABS_Y, term_y)
                self.master.master.device.emit_click(self.event)
                self.master.master.device.emit(ui.ABS_X, curr_x)
                self.master.master.device.emit(ui.ABS_Y, curr_y)
            else:
                self.master.set_keyboard(self.event)
            return True


class Device(ui.Device):

    def __init__(self, parent):
        self.parent = parent
        events = self.parent.kb.get_events()
        events += [ui.ABS_X, ui.ABS_Y, ui.KEY_ENTER]
        super(Device, self).__init__(events)


if __name__ == '__main__':
    app = Application(None)
    app.mainloop()
