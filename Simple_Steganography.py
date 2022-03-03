import sys
import base64
from PIL import Image
from random import choice

text_to_bin = lambda text: ''.join([format(ord(x),"08b") for x in text])

def hide(msg:str,img)->str:
    img=Image.open(img)
    msg=text_to_bin(base64.b64encode(msg.encode('utf-8')).decode()+'stgENDflag0')
    
    pixels=[*((img.convert("RGB")).getdata())]
    start= choice([*range(0, 255)]) if pixels.__len__() >= 255 else choice([*range(0, 127)]) if pixels.__len__() >= 127 else choice([*range(0, 64)]) if pixels.__len__() >= 64 else 0
    hidden=[(start,0,0)]
    for pixel in enumerate(pixels[1:]):
        if(pixel[0]>=start and (pixel[0]-start) <= msg.__len__()-1):
            newcolor=[*pixel[1]]
            newcolor[1]=int((msg[(pixel[0]-start)]+(format(pixel[1][1],"b")[:-1][1:]))[::-1],2)
            hidden.append(tuple(newcolor))
        else:
            hidden.append(pixel[1])
    imNew=Image.new("RGB",img.size) 
    imNew.putdata(hidden)
    imNew.save(sys.path[0]+"\steganography."+img.format.lower(),format=img.format.lower())
    return sys.path[0]+"\steganography."+img.format.lower()

def view(img)->str:
    img=Image.open(img)
    message=''
    pixel_data=[*((img.convert("RGB")).getdata())]
    chars=''
    start=pixel_data[0][0]
    for pixel in enumerate(pixel_data[start+1:]):     
            if('stgENDflag0' in message):
                break
            if(pixel[0]%8==0 and pixel[0]!=0):
                message+=chr(int(chars,2))
                chars=''
            chars += format(pixel[1][1],'b')[::-1][:1]
    return base64.b64decode(message.replace('stgENDflag0','')).decode()
  
print(__file__)
path=hide("""You ve probably heard of Lorem Ipsum before – it’s the most-used dummy text excerpt out there. People use it because it has a fairly normal distribution of letters and words (making it look like normal English), but it’s also Latin, which means your average reader won’t get distracted by trying to read it. It’s perfect for showcasing design work as it should look when fleshed out with text, because it allows viewers to focus on the design work itself, instead of the text. It’s also a great way to showcase the functionality of programs like word processors, font types, and more.""",sys.path[0]+"\Simple_Steganography.jpg")
print(view(path))
