# -*- coding:utf-8 -*-

image_styles = '''
<style type="text/css">

.imgfloat{
    float:left;
}
.imgfloat img{
    float:left;
}
.img_200_150{
    width: 200px;
    height: 150px;
}
.img_200_200{
    width: 200px;
    height: 200px;
}
.img_200_350{
    width: 200px;
    height: 350px;
}
.img_400_150{
    width: 400px;
    height: 150px;
}
.img_400_200{
    width: 400px;
    height: 200px;
}
.img_400_350{
    width: 400px;
    height: 350px;
}
.img_600_350{
    width: 600px;
    height: 350px;
}
.img_1000_350{
    width: 1000px;
    height: 350px;
}
</style>
'''
def get_scale(w,h):
    return '?imageView2/1/w/%s/h/%s/q/85' % (w,h)

image_boxs = {
# ' ____________________'
# '|                    |'
# '|                    |'
# '|____________________|'
    0:{
            'html':['<div class="img_1000 imgfloat"><img class="scrollLoading" class="img_1000_350" data-url="{0}" src="%s"></img></div>',],
            'width':1000,
            'scale':[get_scale(1000,350),],
        },
# ' ____________'
# '|            |'
# '|            |'
# '|____________|'
    1:{
            'html':['<div class="img_600 imgfloat"><img class="scrollLoading" class="img_600_350" data-url="{0}" src="%s"></img></div>',],
            'width':600,
            'scale':[get_scale(600,350),],
        },
# ' ________'
# '|        |'
# '|        |'
# '|________|'
    2:{
            'html':['<div class="img_400 imgfloat"><img class="scrollLoading" class="img_400_350" data-url="{0}" src="%s"></img></div>',],
            'width':400,
            'scale':[get_scale(400,350),],
        },
# ' ________'
# '|        |'
# '|________|'
# '|________|'
    3:{
            'html':['<div class="img_400 imgfloat"><img class="scrollLoading" class="img_400_200" data-url="{0}" src="%s"></img>',
                    '<img class="scrollLoading" class="img_400_150" data-url="{0}" src="%s"></img></div>',],
            'width':400,
            'scale':[get_scale(400,200), get_scale(400,150),],
        },
# ' ________'
# '|________|'
# '|        |'
# '|________|'
    4:{
            'html':['<div class="img_400 imgfloat"><img class="scrollLoading" class="img_400_150" data-url="{0}" src="%s"></img>',
                    '<img class="scrollLoading" class="img_400_200" data-url="{0}" src="%s"></img></div>',],
            'width':400,
            'scale':[get_scale(400,150), get_scale(400,200),],
        },
# ' ________'
# '|___|____|'
# '|        |'
# '|________|'
    5:{
            'html':['<div class="img_400 imgfloat"><img class="scrollLoading" class="img_200_150" data-url="{0}" src="%s"></img>',
                    '<img class="scrollLoading" class="img_200_150" data-url="{0}" src="%s"></img>',
                    '<img class="scrollLoading" class="img_400_200" data-url="{0}" src="%s"></img></div>',],
            'width':400,
            'scale':[get_scale(200,150), get_scale(200,150), get_scale(400,200),],
        },
# ' ________'
# '|        |'
# '|________|'
# '|___|____|'
    6:{
            'html':['<div class="img_400 imgfloat"><img class="scrollLoading" class="img_400_200" data-url="{0}" src="%s"></img>',
                    '<img class="scrollLoading" class="img_200_150" data-url="{0}" src="%s"></img>',
                    '<img class="scrollLoading" class="img_200_150" data-url="{0}" src="%s"></img></div>',],
            'width':400,
            'scale':[get_scale(400,200), get_scale(200,150), get_scale(200,150),],
        },
# ' ____'
# '|    |'
# '|    |'
# '|____|'
    7:{
            'html':['<div class="img_200 imgfloat"><img class="scrollLoading" class="img_200_350" data-url="{0}" src="%s"></img></div>',],
            'width':200,
            'scale':[get_scale(200,350),],
        },
# ' ____'
# '|____|'
# '|    |'
# '|____|'
    8:{
            'html':['<div class="img_200 imgfloat"><img class="scrollLoading" class="img_200_150" data-url="{0}" src="%s"></img>',
                    '<img class="scrollLoading" class="img_200_200" data-url="{0}" src="%s"></img></div>',],
            'width':200,
            'scale':[get_scale(200,150), get_scale(200,200),],
        },
# ' ____'
# '|    |'
# '|____|'
# '|____|'
    9:{
            'html':['<div class="img_200 imgfloat"><img class="scrollLoading" class="img_200_200" data-url="{0}" src="%s"></img>',
                    '<img class="scrollLoading" class="img_200_150" data-url="{0}" src="%s"></img></div>',],
            'width':200,
            'scale':[get_scale(200,200), get_scale(200,150),],
        },
}

RANDOM_IMAGE_BOX = {
    0:(1,9),
    200:(1,9),
    400:(1,9),
    600:(2,9),
    800:(7,9),
}
import random
def generate_row():
    imgBox = []
    t_width = 0
    while True:
        if t_width == 1000:
            break
        bindex = random.randint(*RANDOM_IMAGE_BOX[t_width])
        imgBox.append(image_boxs[bindex])
        t_width += image_boxs[bindex]['width']
    return imgBox

def generate_html(pagerow=8):
    imgBoxs = []
    for i in xrange(pagerow):
        imgBoxs += generate_row()
    return imgBoxs

RANDOM_IMAGE_BOX_M = {0:[1,2],400:[1],600:[2]}
def generate_row_mobile():
    imgBox = []
    t_width = 0
    while True:
        if t_width == 1000:
            break
        bindex = random.choice(RANDOM_IMAGE_BOX_M[t_width])
        imgBox.append(image_boxs[bindex])
        t_width += image_boxs[bindex]['width']
    return imgBox
def generate_html_mobile(pagerow=6):
    imgBoxs = []
    for i in xrange(pagerow):
        imgBoxs += generate_row_mobile()
    return imgBoxs

