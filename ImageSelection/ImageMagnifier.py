from ttkbootstrap import Toplevel, Canvas, NW, BOTH

from PIL import Image, ImageTk

class ImageMagnifier(object):

    WIDTH = 750
    HEIGHT = 750

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.photo = None
        self.x = self.y = 0

    def showtip(self, path):
        self.path = path
        if self.tipwindow or not self.path:
            return

        image = self.widget.find_withtag("image")
        x, y, cx, cy = self.widget.bbox(image)
        x = x + self.widget.winfo_rootx()
        y = y + self.widget.winfo_rooty() + cy

        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)

        canvas = Canvas(tw)
        canvas.pack(expand=True, fill=BOTH)

        img = Image.open(self.path)

        img.thumbnail(size=(self.WIDTH, self.HEIGHT))

        width, height = img.size

        if y + height > 1080:
            y = y - height - cy
        
        if y < 0:
            y = y + height + cy

        if y + height > 1080:
            y = y - height / 2 - cy
            if x - width > 0:
                x -= width
            else:
                x += cx 
        
        if y < 0:
            y = y + height / 2

        if x + width > 1920:
            x -= width - cx

        tw.wm_geometry("+%d+%d" % (x, y))

        canvas.config(width=img.size[0], height=img.size[1])
        self.photo = ImageTk.PhotoImage(img)

        canvas.create_image(0, 0, image=self.photo, anchor=NW)


    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def newImageMagnifier(widget, path):
    toolTip = ImageMagnifier(widget)
    def enter(event):
        toolTip.showtip(path)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)