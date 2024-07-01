import configparser
import argparse
import ast
from tkinter import Tk, Label, Menu
from tkinter.font import Font
from random import SystemRandom

class RandomNumberGeneratorApp:
    def __init__(self, root, cfg):
        self.root = root
        self.root.title('RNGclick')
        self.interval = None
        self.click_funcid = None

        self.rng_limit = (1, 100)
        self.default_width = int(cfg['default_width'])
        self.default_height = int(cfg['default_height'])
        self.default_x = int(cfg['default_x'])
        self.default_y = int(cfg['default_y'])
        self.fontsize_incr = int(cfg['fontsize_incr'])
        self.menu_isvisible = cfg.getboolean('menu_isvisible')
        self.color_mode = cfg.getboolean('color_mode')
        self.rng_istimed = cfg.getboolean('rng_istimed')
        self.refresh_interval = int(cfg['refresh_interval'])

        self.create_widgets()

    def create_widgets(self):
        self.fontStyle = Font(family='Consolas', size=30)
        self.label = Label(self.root, text="0", font=self.fontStyle, bg='black')
        self.label.pack(expand='True', fill="both")
        
        self.emptyMenu = Menu(self.root)
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Switch Color Order", command=self.color_switch)
        self.filemenu.add_separator()
        self.filemenu.add_radiobutton(label="RNG from 0-99", command=lambda: self.rng_limit_switch((0,99)))
        self.filemenu.add_radiobutton(label="RNG from 1-100", command=lambda: self.rng_limit_switch((1,100)))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Increase Font Size", 
            command=lambda: self.fontStyle.config(
                size = self.fontStyle['size'] + self.fontsize_incr)
        )
        self.filemenu.add_command(label="Decrease Font Size", 
            command=lambda: self.fontStyle.config(
                size = self.fontStyle['size'] - self.fontsize_incr)
        )
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Timed Mode Toggle", command=self.timed_switch)
        self.menubar.add_cascade(label="Options", menu=self.filemenu)
        self.root.config(menu=self.menubar)

        self.root.configure(background='black')
        self.click_funcid = self.root.bind('<Button-1>', lambda event: self.gen_rand())
        self.root.bind('<Button-3>', lambda event: self.clear_rand())
        self.root.bind('<Double-Button-3>', lambda event: self.menu_switch())

        self.root.geometry(f"{self.default_width}x{self.default_height}+{self.default_x}+{self.default_y}") #260x200+200+200
        self.root.wm_attributes("-topmost", 1)

    def gen_rand(self):
        COLORS = ('#FF3333','#FFAC33','#FFFF33','#33FF39','#33FF39','#FFFF33','#FFAC33','#FF3333')

        self.label['text'] = SystemRandom().randint(self.rng_limit[0], self.rng_limit[1])
        self.label.config(fg=COLORS[(self.label['text'] + 100*int(self.color_mode) - self.rng_limit[0]) // 25])

    def auto_refresh(self):
        COLORS = ('#FF3333','#FFAC33','#FFFF33','#33FF39','#33FF39','#FFFF33','#FFAC33','#FF3333')

        self.label['text'] = SystemRandom().randint(self.rng_limit[0], self.rng_limit[1])
        self.label.config(fg=COLORS[(self.label['text'] + 100*int(self.color_mode) - self.rng_limit[0]) // 25])

        if self.interval:
            self.interval = self.root.after(self.refresh_interval, self.auto_refresh)
        

    def clear_rand(self):
        self.label['text'] = ""

    def color_switch(self):
        self.color_mode = not(self.color_mode)

    def timed_switch(self):
        self.rng_istimed = not(self.rng_istimed)
        if self.rng_istimed == True:
            self.interval = self.root.after(self.refresh_interval, self.auto_refresh)
            self.root.unbind('<Button-1>', self.click_funcid)
        else:
            if self.interval:
                self.root.after_cancel(self.interval)
                self.interval = None
            self.click_funcid = self.root.bind('<Button-1>', lambda event: self.gen_rand())

    def rng_limit_switch(self, new_limit):
        self.rng_limit = new_limit

    def menu_switch(self):
        if self.menu_isvisible:
            self.root.config(menu=self.emptyMenu)
            self.menu_isvisible = not self.menu_isvisible
            winx = self.root.winfo_rootx() - 1
            winy = self.root.winfo_rooty() + 19
            winw = self.root.winfo_width()
            winh = self.root.winfo_height() - 38
            self.root.geometry(f'{winw}x{winh}')
            self.root.geometry(f'+{winx}+{winy}')
            self.root.overrideredirect(1)
        else:
            self.root.config(menu=self.menubar)
            self.menu_isvisible = not self.menu_isvisible
            winx = self.root.winfo_rootx() - 7
            winy = self.root.winfo_rooty() - 50
            winw = self.root.winfo_width()
            winh = self.root.winfo_height() - 2
            self.root.geometry(f'{winw}x{winh}')
            self.root.geometry(f'+{winx}+{winy}')
            self.root.overrideredirect(0)

def main():
    config = configparser.ConfigParser()
    config.read('RNGclick.ini')

    default_config = config['DEFAULT']

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--position", help="position of the random number", type=int)
    args = parser.parse_args()

    positions_list = ast.literal_eval(default_config['positions_list'])

    if args.position is not None:
        p = args.position
        default_config['default_x'] = str(positions_list[p][0])
        default_config['default_y'] = str(positions_list[p][1])

    root = Tk()
    app = RandomNumberGeneratorApp(root, default_config)

    app.gen_rand()
    root.mainloop()


if __name__ == '__main__':
    main()
