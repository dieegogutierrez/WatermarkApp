from tkinter import *
from tkinter import colorchooser
from PIL import Image, ImageOps, ImageTk, ImageDraw, ImageFont
from tkinter.filedialog import askopenfilename, asksaveasfilename
from matplotlib import font_manager

FILETYPES = [('Jpg Files', '*.jpg'), ('PNG Files', '*.png')]
BG_COLOR = 'black'
TITLE_FONT = ("Arial Bold", 20)
ITEMS_FONT = ("Arial", 15)


class WatermarkApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermark App")
        self.config(pady=50, padx=50, bg=BG_COLOR)
        self.canvas = Canvas(width=500, height=700, bg=BG_COLOR, highlightbackground='white')
        self.canvas.grid(column=0, row=0, rowspan=10, padx=40)
        self.filepath = None
        self.img = None
        self.image_container = None
        self.watermarked_image = None
        self.watermark_color = (255, 255, 255)
        self.color_button = None
        self.radio_state = IntVar()
        self.font_style = StringVar()
        self.font_size_spinbox = Spinbox()
        self.opacity_scale = Scale()
        self.watermark_entry = Entry()
        self.create_widgets()

    def create_widgets(self):
        self.upload_btn()
        self.save_btn()
        self.position_btn()
        self.fontstyle_btn()
        self.fontsize_btn()
        self.fontcolor_btn()
        self.fontopacity_btn()
        self.watermark_btn()

    def upload_btn(self):
        upload = Button(text='Upload Image', command=self.search_file, font=ITEMS_FONT)
        upload.grid(column=0, row=10)

    def search_file(self):
        self.filepath = askopenfilename(initialdir="/", title="Select an Image", filetypes=FILETYPES)
        self.show_image_canvas()

    def show_image_canvas(self):
        pic = Image.open(self.filepath)
        img = ImageOps.exif_transpose(pic)  # Cancel auto-rotation
        r_img = self.resize(img)
        self.canvas.configure(width=r_img.width(), height=r_img.height())
        self.image_container = self.canvas.create_image(0, 0, anchor='nw', image=r_img)

    def resize(self, image):
        resized_img = ImageOps.contain(image, (500, 700))
        resized_img = ImageTk.PhotoImage(resized_img)
        self.canvas.image = resized_img  # Keep reference to the image
        return resized_img

    def save_btn(self):
        save_button = Button(text='Save', command=lambda: self.save_image(), font=ITEMS_FONT)
        save_button.grid(column=6, row=10, sticky=W)

    def save_image(self):
        try:
            file = asksaveasfilename(defaultextension='.jpeg', filetypes=FILETYPES)
            if file:
                self.watermarked_image.save(file)
        except AttributeError:
            pass

    def position_btn(self):
        watermark_position_label = Label(text='Watermark Position', bg=BG_COLOR, font=TITLE_FONT)
        watermark_position_label.grid(column=3, columnspan=4, row=0)

        radiobutton1 = Radiobutton(text="Top Left", value=1, variable=self.radio_state, bg=BG_COLOR, font=ITEMS_FONT)
        radiobutton1.grid(column=3, row=1, sticky=W)
        radiobutton2 = Radiobutton(text="Top Right", value=2, variable=self.radio_state, bg=BG_COLOR, font=ITEMS_FONT)
        radiobutton2.grid(column=6, row=1, sticky=W)
        radiobutton3 = Radiobutton(text="Center", value=3, variable=self.radio_state, bg=BG_COLOR, font=ITEMS_FONT)
        radiobutton3.grid(column=3, columnspan=4, row=2)
        radiobutton4 = Radiobutton(text="Bottom Left", value=4, variable=self.radio_state, bg=BG_COLOR, font=ITEMS_FONT)
        radiobutton4.grid(column=3, row=3, sticky=W)
        radiobutton5 = Radiobutton(text="Bottom Right", value=5, variable=self.radio_state, bg=BG_COLOR, font=ITEMS_FONT)
        radiobutton5.grid(column=6, row=3, sticky=W)

    def watermark_position(self, pic_size, text_size):
        text_width = text_size[2] - text_size[0]
        text_height = text_size[3] - text_size[1]
        pad = 50
        if self.radio_state.get() == 1:
            x = pad + text_width // 2
            y = pad + text_height // 2
        elif self.radio_state.get() == 2:
            x = pic_size[0] - pad - text_width // 2
            y = pad + text_height // 2
        elif self.radio_state.get() == 3:
            x = pic_size[0] // 2
            y = pic_size[1] // 2
        elif self.radio_state.get() == 4:
            x = pad + text_width // 2
            y = pic_size[1] - pad - text_height // 2
        else:
            x = pic_size[0] - pad - text_width // 2
            y = pic_size[1] - pad - text_height // 2

        return x, y

    def fontstyle_btn(self):
        font_options_label = Label(text='Font Options', bg=BG_COLOR, font=TITLE_FONT)
        font_options_label.grid(column=3, columnspan=4, row=4)

        font_style_label = Label(text='Style', bg=BG_COLOR, font=ITEMS_FONT)
        font_style_label.grid(column=3, row=5, sticky=E)

        system_fonts_paths = font_manager.findSystemFonts(fontpaths=None, fontext='ttf')
        font_name = [path.split('.')[0].split('/')[-1] for path in system_fonts_paths if not path.endswith('.otf')]
        font_name.sort()
        self.font_style.set('Arial')
        font_style_menu = OptionMenu(self, self.font_style, *font_name)
        font_style_menu.grid(column=4, columnspan=3, row=5, sticky=W)

    def fontsize_btn(self):
        font_size_label = Label(text='Size', bg=BG_COLOR, font=ITEMS_FONT)
        font_size_label.grid(column=3, row=6, sticky=E)
        self.font_size_spinbox = Spinbox(from_=1, to=1000, increment=50, width=4)
        self.font_size_spinbox.grid(column=4, row=6, sticky=W)

    def fontcolor_btn(self):
        color_label = Label(text='Color', bg=BG_COLOR, font=ITEMS_FONT)
        color_label.grid(column=3, row=7, sticky=E)
        self.color_button = Button(text="Set", command=self.color)
        self.color_button.grid(column=4, row=7, sticky=W)

    def color(self):
        color_code = colorchooser.askcolor()
        self.watermark_color = color_code[0]
        self.color_button['fg'] = color_code[1]
        self.color_button['highlightbackground'] = color_code[1]
        self.color_button['text'] = '✔'

    def fontopacity_btn(self):
        opacity_label = Label(text='Opacity', bg=BG_COLOR, font=ITEMS_FONT)
        opacity_label.grid(column=3, row=8, sticky=E)
        self.opacity_scale = Scale(from_=0, to=255, orient='horizontal', sliderlength=20, length=150, bg=BG_COLOR, font=ITEMS_FONT)
        self.opacity_scale.set(255)
        self.opacity_scale.grid(column=4, columnspan=2, row=8, sticky=W, ipady=10)

    def watermark_btn(self):
        watermark_text_label = Label(text='Watermark Text', bg=BG_COLOR, font=TITLE_FONT)
        watermark_text_label.grid(column=3, columnspan=4, row=9)

        self.watermark_entry.insert(0, "@Watermark")
        self.watermark_entry.grid(column=3, columnspan=2, row=10, sticky=E)

        watermark_button = Button(text='Add', command=self.watermark, font=ITEMS_FONT)
        watermark_button.grid(column=5, row=10, sticky=E)

    def watermark(self):
        # get an image
        try:
            with Image.open(self.filepath).convert("RGBA") as base:

                # Cancel auto-rotation
                base = ImageOps.exif_transpose(base)

                # make a blank image for the text, initialized to transparent text color
                txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
                # get a font
                fnt = ImageFont.truetype(self.font_style.get(), int(self.font_size_spinbox.get()))
                # get a drawing context
                d = ImageDraw.Draw(txt)
                # get a color and opacity
                fill_rgba = tuple(self.watermark_color) + (int(self.opacity_scale.get()),)
                # draw watermark
                d.text((self.watermark_position(base.size, fnt.getbbox(text=self.watermark_entry.get()))), self.watermark_entry.get(),
                       anchor='mm', font=fnt, fill=fill_rgba)

                out = Image.alpha_composite(base, txt).convert("RGB")
                self.watermarked_image = out

                out = self.resize(out)

                self.canvas.itemconfig(self.image_container, image=out)
        except AttributeError:
            pass