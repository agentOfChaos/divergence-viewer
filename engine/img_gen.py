from PIL import Image, ImageDraw, ImageFont

bgcolor = (48, 10, 36)
fgcolor = (216, 255, 213)

base1_size = (512, 512)

def string_to_png(mystr, filename, font="NotoSansMonoCJKjp-Regular.otf", fontsize=18):
    base1 = ImageDraw.Draw(Image.new("RGB", base1_size))
    fontobj = ImageFont.truetype(font, fontsize)
    text_width, text_height = base1.textsize(mystr, font=fontobj)
    trueimg = Image.new("RGB", (text_width, text_height), bgcolor)
    drawer = ImageDraw.Draw(trueimg)
    drawer.text((0,0), mystr, fill=fgcolor, font=fontobj)
    with open(filename, "wb") as fp:
        trueimg.save(fp)
