import sys
import base64
from PIL import Image
from random import choice,randint
from string import ascii_lowercase,ascii_uppercase

text_to_bin = lambda text: ''.join([format(ord(x),"08b") for x in text])
random_word = lambda n: ''.join([choice(ascii_lowercase+ascii_uppercase+'_') for x in range(n+1)])

def hide(msg:str,img)->str:
    img=Image.open(img)
    magic_char = randint(32,127)
    msg=text_to_bin(base64.b64encode(msg.encode("utf-8")).decode()+('stgENDflag0_'+chr(magic_char)))  
    pixels=[*((img.convert("RGB")).getdata())]
    start= choice([*range(0, 255)]) if pixels.__len__() >= 255 else choice([*range(0, 127)]) if pixels.__len__() >= 127 else choice([*range(0, 64)]) if pixels.__len__() >= 64 else 0
    hidden=[(start,magic_char,255)]
    for pixel in enumerate(pixels[1:]):
        if(pixel[0]>start and (pixel[0]-start) <= (msg.__len__()-1)):
            newcolor=[*pixel[1]]
            newcolor[1]=int((msg[(pixel[0]-start)]+(format(pixel[1][1],"b")[:-1][1:]))[::-1],2) 
            hidden.append(tuple(newcolor))
        else:
            hidden.append(pixel[1])
    imNew=Image.new("RGB",img.size) 
    imNew.putdata(hidden)
    f_name=f"\steganography_{random_word(randint(8,16))}.png"
    imNew.save(sys.path[0]+f_name)
    return sys.path[0]+f_name

def view(img)->str:
    img=Image.open(img)
    message,chars=[*('','')]
    pixel_data=[*((img.convert("RGB")).getdata())]
    start=pixel_data[0][0]+1
    flag='stgENDflag0_'+chr(pixel_data[0][1])
    for pixel in enumerate(pixel_data[start:]):   
            if(flag in message):
                break
            if(((pixel[0]%8==0) & (pixel[0]!=0))^1 == 0):
                message+=chr(int(chars,2))
                chars=''
            chars += format(pixel[1][1],'b')[::-1][:1]
    return base64.b64decode(message.replace(flag,'')).decode()

path=hide("""You ve probably heard of Lorem Ipsum before – it’s the most-used dummy text excerpt out there. People use it because it has a fairly normal distribution of letters and words (making it look like normal English), but it’s also Latin, which means your average reader won’t get distracted by trying to read it. It’s perfect for showcasing design work as it should look when fleshed out with text, because it allows viewers to focus on the design work itself, instead of the text. It’s also a great way to showcase the functionality of programs like word processors, font types, and more.""",sys.path[0]+"\steganography.jpeg")
print(view(path))
exit(0)
