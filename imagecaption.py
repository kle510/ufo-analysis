from captionbot import CaptionBot

c = CaptionBot()
msg = c.url_caption("https://beebom-redkapmedia.netdna-ssl.com/wp-content/uploads/2016/01/Reverse-Image-Search-Engines-Apps-And-Its-Uses-2016.jpg")
#msg2 = c.file_caption("/Users/khanh/Desktop/bbb.jpg")
print(msg)