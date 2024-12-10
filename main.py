import pygame
import random
import copy
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image

pygame.init()


bg_color = "#202021"
size_x = 700
size_y = 700
pic_x = 50
pic_y = 50
num = 3
width = 10
width2 =1
difficulty = 1
screen=pygame.display.set_mode((1000,800),flags=pygame.RESIZABLE)
file_path = 'picture/picture1.png'
picture = pygame.image.load("picture/picture1.png")
picture = pygame.transform.scale(picture,size=(size_x,size_y))

f = pygame.font.Font('C:/Windows/Fonts/simhei.ttf',32)

screen.fill(bg_color)

rect2=pygame.Rect(pic_x,pic_y,size_x,size_y)


rect_ = {
    "picture" : rect2,
    "bk" : pygame.Rect(pic_x-width,pic_y-width,size_x+2*width,size_y+2*width),
    "start" : pygame.Rect(800,50,150,80),
    "choose" : pygame.Rect(800,150,150,80),
    "difficulty1" : pygame.Rect(800,250,150,80),
    "step" : pygame.Rect(800,550,150,80),
    "none" : pygame.Rect(800,650,150,80),
    "print" : pygame.Rect(800,350,150,80),
    "ticker" : pygame.Rect(800,450,150,80)
}

text_ = {
    "start" : "开始游戏",
    "choose" : "选择图片",
    "difficulty1" : "简单",
    "difficulty2" : "一般",
    'difficulty3' : "困难",
    "step" : "",
    "none" : "",
    "print" : "显示原图",
    "ticker0" : "一般模式",
    "ticker1" : "计时模式"
}

nums = []

surface_ = {

}

surface_num ={

}
rect_num = {

}

def create(num,face):
    global nums
    nums = []
    global rect_num,surface_num
    surface_num = {}
    rect_num = {}
    for x in range(1,num+1,1):
        for y in range(1,num+1,1):
            nums.append((x-1)*num+y)
            rect = pygame.Rect(rect_['picture'].x+(x-1)*(size_x/num),rect_['picture'].y+(y-1)*(size_x/num),size_x//num,size_x//num)
            rect_num[f"{(x-1)*num+y}"] = rect
            face = picture.subsurface(+(x-1)*size_x/num,+(y-1)*size_x/num,size_x/num,size_x/num)
            surface_num[f"{(x-1)*num+y}"] =face

def daluan():
    random.shuffle(nums)

def check(mode = 0 , time_left = 0.0):
    # print(mode)
    # print(time_left)
    flag = 1
    if mode == 0:
         for i in range(num * num - 1):
            if nums[i + 1] < nums[i]:
                flag = 0
         return flag
    else:
        if time_left<=0:
            return  1,0
        else:
            for i in range(num * num - 1):
                if nums[i + 1] < nums[i]:
                    return 0,0
        return 0,1

def draw1(surface, color, rect_x, rect_y, rect_width, rect_height, corner_radius = 5):
    # Rect 表示整个矩形区域
    rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
    # 确保圆角的半径不会大于矩形宽高的一半
    if corner_radius * 2 > rect.width or corner_radius * 2 > rect.height:
        corner_radius = min(rect.width // 2, rect.height // 2)

    # 绘制中间的矩形部分，去掉四个角
    pygame.draw.rect(surface, color, (rect_x + corner_radius, rect_y, rect_width - 2 * corner_radius, rect_height))
    pygame.draw.rect(surface, color, (rect_x, rect_y + corner_radius, rect_width, rect_height - 2 * corner_radius))

    # 绘制四个圆角
    pygame.draw.circle(surface, color, (rect_x + corner_radius, rect_y + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect_x + rect_width - corner_radius, rect_y + corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect_x + corner_radius, rect_y + rect_height - corner_radius), corner_radius)
    pygame.draw.circle(surface, color, (rect_x + rect_width - corner_radius, rect_y + rect_height - corner_radius), corner_radius)


def creat_button(button,difficulty = 0,text_all = None):
    surface = pygame.Surface((rect_[button].width,rect_[button].height),flags = 0)
    surface_[button] = surface
    surface.fill(bg_color)
    draw1(surface = surface , color = "#323232" , rect_x = width2 , rect_y = width2 , rect_height = rect_[button].height-2*(width2) ,rect_width = rect_[button].width-2*(width2) , corner_radius = 10)
    if button == "difficulty1":
        text = f.render(text_[f"difficulty{difficulty}"], True , (255 , 255 , 255))
    elif button == "none":
        f1 = pygame.font.Font('C:/Windows/Fonts/simhei.ttf' , 25)
        text = f1.render("时间："+text_all, True , (255 , 255 , 255))
    elif button == "step":
        f1 = pygame.font.Font('C:/Windows/Fonts/simhei.ttf' , 25)
        text = f1.render("步数："+text_all, True , (255 , 255 , 255))
    elif button == "ticker":
        text = f.render(text_all,True , (255 , 255 , 255))
    elif button == "start" and difficulty ==1:
        text = f.render(text_all , True , (255 , 255 , 255))
    else:
        text = f.render(text_[button] , True , (255 , 255 , 255))
    text_rect = text.get_rect()
    text_rect.center = (rect_[button].width/2,rect_[button].height/2)
    surface.blit(text,text_rect)



def choose_image():
    global picture,file_path
    file_path_raw = file_path
    file_path = filedialog.askopenfilename(title = "选择图片" ,
                                           filetypes = [("Image files" , "*.jpg *.png *.bmp *.jpeg")])

    if file_path:
        picture = pygame.image.load(file_path)
        picture = pygame.transform.scale(picture , size = (size_x , size_y))
        create(num , picture)
        return True
    file_path = file_path_raw
    return False

def show_game_over_popup(pass_time,step):
    """显示游戏结束的弹窗"""
    root = tk.Tk()  # 创建Tkinter窗口
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo("游戏结束", f"恭喜，你完成了游戏！\n用时{pass_time:.1f}s,走了{step}步")  # 弹出提示框
    root.destroy()  # 销毁窗口，关闭Tkinter
def show_game_over_popup1():
    """显示游戏结束的弹窗"""
    root = tk.Tk()  # 创建Tkinter窗口
    root.withdraw()  # 隐藏主窗口
    messagebox.showinfo("游戏结束", f"时间到啦，挑战失败")  # 弹出提示框
    root.destroy()  # 销毁窗口，关闭Tkinter


def xianshi():
    # 加载并显示图片
    image = Image.open(file_path)
    image.show()

limit_time = "0.0"

def time_put():
    global limit_time
    root = tk.Tk()
    root.title("倒计时")

    label = tk.Label(root , text = "请输入倒计时（s）:")
    label.pack()

    entry = tk.Entry(root)
    entry.pack(padx = 20 , pady = 20)

    def on_submit():
        global limit_time
        limit_time = entry.get()
        try:
            limit_time = float(limit_time)
        except ValueError as exceptions:
            messagebox.showinfo("输入失败" , f"请重新输入一个数字")
            root.destroy()
            time_put()
            return
        messagebox.showinfo("输入成功", f"倒计时时间设置为{limit_time}秒")
        root.destroy()

    button = tk.Button(root , text = "提交" , command = on_submit)
    button.pack()

    root.mainloop()

bk = pygame.Surface((rect_['bk'].width,rect_["bk"].height),flags = 0)
start = pygame.Surface((rect_['start'].width,rect_["start"].height),flags = 0)
bk.fill(bg_color)
draw1(surface = bk, color = "#323232",rect_x = 0,rect_y = 0,rect_height = rect_["bk"].height,rect_width = rect_["bk"].width,corner_radius=10)

screen.blit(picture,rect2)
screen.blit(bk,rect_['bk'])

dragging = False
drag_offset_x, drag_offset_y = 0, 0  
dragging_surface = ''

create(num,picture)

creat_button("start")
creat_button("choose")
creat_button("print")
creat_button("none",0,text_all = "0.0s")
creat_button("step",0,text_all = "0步")
creat_button("difficulty1",difficulty)
creat_button("ticker",0,"普通模式")
rect_raw = copy.deepcopy(rect_num)
screen.blit(surface_["start"],rect_["start"])
screen.blit(surface_["choose"],rect_["choose"])
screen.blit(surface_["difficulty1"],rect_["difficulty1"])
screen.blit(surface_["none"],rect_["none"])
screen.blit(surface_["step"],rect_["step"])
screen.blit(surface_["print"],rect_["print"])
screen.blit(surface_["ticker"],rect_["ticker"])

game_start = False
start_time = None
time_in =0
mode = 0
step = 0

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for key , value in surface_num.items():
                if rect_num[key].collidepoint(event.pos) and (int(key) in nums and game_start):
                    dragging = True
                    dragging_surface = key
                    drag_offset_x,drag_offset_y = event.pos
            for key,value in surface_.items():
                if rect_[key].collidepoint(event.pos):
                    if key == "choose" and not game_start:
                        choose_image()
                        game_start = False
                        creat_button("none",0,text_all = "0.0s")
                        step = 0
                    if key == "start":
                        if game_start:
                            game_start = 0
                            break
                        game_start =True
                        daluan()
                        step = 0
                        start_time = pygame.time.get_ticks()


                    if key == "difficulty1" and not game_start:
                        difficulty = difficulty+1
                        if difficulty == 4:
                            difficulty = 1
                        num = difficulty+2
                        create(num,picture)
                        rect_raw = copy.deepcopy(rect_num)
                        creat_button("difficulty1",difficulty)
                        game_start = False
                        step = 0
                        creat_button("step" , text_all = f"{step}步")
                        creat_button("none",0,text_all = "0.0s")
                    if key == "print":
                        xianshi()

                    if key == "ticker" and not game_start:
                        if mode == 0:
                            mode = 1
                            creat_button("ticker",0,"计时模式")
                        else:
                            mode = 0
                            creat_button("ticker",0,"普通模式")
                    if key == "none" and mode:
                        time_put()
                        limit_time = float(limit_time)
                        creat_button("none",0,text_all=f"{limit_time:.1f}s")


        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                flag = 0
                for key , value in surface_num.items():
                    if rect_raw[key].collidepoint(event.pos) and (not (key==dragging_surface)):
                        flag = 1
                        nums[int(key)-1] , nums[int(dragging_surface)-1] = nums[int(dragging_surface)-1],nums[int(key)-1]
                        step = step + 1
                rect_num = copy.deepcopy(rect_raw)
                dragging = False

                if check() and game_start:
                    screen.blit(picture,rect_['picture'])
                    creat_button("step",0,text_all = f"{step}步")
                    screen.blit(surface_["step"],rect_["step"])
                    screen.blit(surface_["none"],rect_["none"])
                    pygame.display.flip()
                    game_start = False
                    show_game_over_popup((pygame.time.get_ticks()-start_time)/1000,step)



        elif event.type == pygame.MOUSEMOTION and dragging:
            rect_num[dragging_surface].x = event.pos[0] - drag_offset_x + rect_raw[dragging_surface].x
            rect_num[dragging_surface].y = event.pos[1] - drag_offset_y + rect_raw[dragging_surface].y

    if game_start:
        creat_button("start",1,"结束游戏")
    else:
        creat_button("start",1,"开始游戏")
    screen.fill(bg_color)
    screen.blit(bk , rect_['bk'])
    screen.blit(surface_["start"] , rect_["start"])
    screen.blit(surface_["print"] , rect_["print"])
    screen.blit(surface_["choose"] , rect_["choose"])
    screen.blit(surface_[f"difficulty1"] , rect_[f"difficulty1"])
    screen.blit(surface_["ticker"] , rect_["ticker"])
    if(game_start):
        if mode == 0:
            creat_button("none",text_all = f"{(pygame.time.get_ticks()-start_time)/1000:.1f}s")
            creat_button("step" , text_all = f"{step}步")
            screen.blit(surface_["none"] , rect_["none"])
            screen.blit(surface_["step"] , rect_["step"])
        else:
            flag1,flag2 = check(1,(float(limit_time)-(pygame.time.get_ticks()-start_time)/1000))
            creat_button("none" ,text_all = f"{float(limit_time) - (pygame.time.get_ticks() - start_time) / 1000:.1f}s")
            creat_button("step" , text_all = f"{step}步")
            screen.blit(surface_["none"] , rect_["none"])
            screen.blit(surface_["step"] , rect_["step"])
            if flag1:
                show_game_over_popup1()
                game_start = False
                creat_button("start" , 0 , text_all = "开始游戏")
    else:
        if mode == 1:
            creat_button("none",0,f"{float(limit_time):.1f}s")
        screen.blit(surface_["none"] , rect_["none"])
        screen.blit(surface_["step"] , rect_["step"])


    k=0
    if dragging:
        for i in nums:
            k = k + 1
            screen.blit(surface_num[f"{i}"] , rect_num[f"{k}"])
    else:
        for i in nums:
            k = k + 1
            screen.blit(surface_num[f"{i}"] , rect_raw[f"{k}"])


    pygame.display.flip() #更新屏幕内容