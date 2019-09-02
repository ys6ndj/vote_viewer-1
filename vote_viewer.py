import tkinter as tk
from tkinter import messagebox as msg
import os
from PIL import Image,ImageTk
import numpy as np
import cv2
import json
import shutil
import datetime

def get_img_path(img_path_lst,index):
    img_path = "image/origin/%s" % img_path_lst[index]
    return img_path

def get_img_wh(img):
    img_h,img_w = img.shape[:2]
    return img_w,img_h

def plus_or_minus(p_or_m,value):
    if p_or_m == "plus":
        value += 1
    elif p_or_m == "minus":
        value -= 1
    return value

def img_resize(img,canvas_size,img_w,img_h):
    img_size = img_w * img_h
    canvas_w,canvas_h = canvas_size
    while img_w > canvas_w or img_h > canvas_h:
        img_w *= 0.9
        img_h *= 0.9
        img_size = img_w * img_h
    img_w,img_h = int(img_w),int(img_h)
    resized_img = cv2.resize(img,(img_w,img_h))
    return resized_img

def get_image(img_lst,img_num,canvas_size,dummy=False):

    img_path = get_img_path(img_lst,img_num)

    if dummy:
        img_path = "config/dummy.jpg"
    img_imread = cv2.imread(img_path)
    img_bgr_to_rgb = cv2.cvtColor(img_imread,cv2.COLOR_BGR2RGB)
    img_w,img_h = get_img_wh(img_bgr_to_rgb)
    resized_img = img_resize(img_bgr_to_rgb,canvas_size,img_w,img_h)
    img_pil = Image.fromarray(resized_img)
    img = ImageTk.PhotoImage(img_pil)
    return img

def quit(root):
    root.destroy()


"""defines sub window for export file"""
class WindowForExport():
    def __init__(self,sub):
        #create title label
        self.sub = sub
        self.top_name = tk.Label(
            sub,
            text="画像を絞り込む",
            font=24
        )
        self.top_name.pack(pady=5)
        #create input file name text
        self.text_whats_filename = tk.Label(
            sub,
            text="作成するファイル名を入力してください。"
        )
        self.text_whats_filename.pack(pady=5)
        #create input file name area
        self.create_file_name = tk.Entry(
            sub
        )
        self.create_file_name.pack(fill="both",padx=15)
        #create input vote number text
        self.text_whats_vote_number = tk.Label(
            sub,
            text="任意の数字を入力してください。\n\
入力された数字以上の vote 数を持つ画像が絞り込まれます。"
        )
        self.text_whats_vote_number.pack(pady=5)
        #create input vote number area
        self.whats_vote_number = tk.Entry(
            sub
        )
        self.whats_vote_number.pack(fill="both",padx=80,pady=5)
        #create bool value for checkbox
        self.bln_check = tk.BooleanVar()
        self.bln_check.set(False)
        #create checkbox what del or not del original image
        self.check_img_del = tk.Checkbutton(
            sub,
            text="元ファイルに格納されている画像を削除する。",
            variable=self.bln_check,
            command=self.checkbutton_is_click
        )
        self.check_img_del.pack(pady=5)
        #create export button
        self.end_button = tk.Button(
            sub,
            text="エクスポート",
            command=self.export_file,
            width=10,
            height=1
        )
        self.end_button.pack(side="bottom",fill="both",padx=15,pady=10)
    """defines export file"""
    def export_file(self):
        #get input file name
        self.file_name = self.create_file_name.get()
        #create dir
        try:
            os.mkdir("image/%s" % self.file_name)
        except:
            #if already existing file_name or invalid file name,
            #raise popup alert.
            self.failed_mkdir_info_box = msg.showwarning("failed mkdir",
            "ファイルの作成に失敗しました。\n\
既に存在しているファイル名か、不正なファイル名です。\n\
ファイル名を入れ直して再度実行してください。")
        #get input vote number
        try:
            self.vote_number_for_squize = int(self.whats_vote_number.get())
        except:
            self.failed_convart_str_to_int = msg.showwarning("failed convart",
            "半角の数字を入力してください。"
            )
        with open("config/vote.json") as f:
            self.dict_img_lst = json.load(f)
        self.img_lst_limited = [
            k for k,v in self.dict_img_lst.items() \
            if int(v) >= self.vote_number_for_squize
        ]

        #if checked checkbox for del or not del original image,
        #original image delete.else,not delete.
        #if delte
        if self.bln_check.get():
            for img_name in self.img_lst_limited:
                src = "image/origin/%s" % img_name
                dst = "image/%s" % self.file_name
                shutil.move(src,dst)
        #if not delete
        else:
            for img_name in self.img_lst_limited:
                src = "image/origin/%s" % img_name
                dst = "image/%s" % self.file_name
                shutil.copy2(src,dst)
        #end exporting
        quit(self.sub)
        self.end_export_info = msg.showinfo("end export",
            "作業が終了しました。\nフォルダを確認してください。"
        )

    def checkbutton_is_click(self):
        if self.bln_check.get():
            self.bln_check.set(False)
        else:
            self.bln_check.set(True)
"""defines category mode config"""
class CategoryModeConfig():
    def __init__(self,sub):
        #create title label
        self.sub = sub
        self.top_name = tk.Label(
            sub,
            text="カテゴリ名を設定する",
            font=24
        )
        self.top_name.pack(pady=10)
        #create input file name text
        self.text_whats_category_name = tk.Label(
            sub,
            text="カテゴリ名を入力してください。"
        )
        self.text_whats_category_name.pack(pady=20)
        #create input file name area
        self.create_category_name = tk.Entry(
            sub
        )
        self.create_category_name.pack(fill="both",padx=20)
        #create send button
        self.send_button = tk.Button(
            sub,
            text="決定",
            command=self.send_category_name
        )
        self.send_button.pack(padx=30,pady=10)
    def send_category_name(self):
        self.category_name = self.create_category_name.get()

        if not self.category_name:
            self.alert_non_cat_name = msg.showwarning("not category name",
            "カテゴリ名を入力してください。")
        else:
            try:
                quit(self.sub)
                os.mkdir("image/%s" % self.category_name)
                self.cat_mode_window = tk.Tk()
                self.cat_mode_window.title("create_mode")
                self.cat_mode_window.minsize(1000,600)
                self.cat_mode = CategoryMode(
                    self.cat_mode_window,
                    self.category_name
                )
                self.cat_mode_window.mainloop()


            except FileExistsError:
                #if already existing file_name or invalid file name,
                #raise popup alert.
                self.failed_mkdir_info_box = msg.showwarning("failed mkdir",
                "既に存在しているカテゴリ名です。\n\
はいを押すとこのまま操作を続けます。\n\
カテゴリ名を再設定するにはいいえを押してください。")
            except OSError:
                self.failed_mkdir_info_box = msg.showwarning("failed mkdir",
                "カテゴリファイルの作成に失敗しました。\n\
ファイル名を確認して再実行してください。")
"""defines category mode"""
class CategoryMode():
    def __init__(self,main,cat_name):

        self.main_window = main
        self.cat_name = cat_name
        self.top_label = tk.Label(
            main,
            text="カテゴリー名：%s" % self.cat_name
        )
        self.top_label.grid(row=0,column=0,columnspan=2)
        #create first to eight img
        with open("config/vote.json") as f:
            self.dict_img_lst = json.load(f)

        self.img_lst = list(self.dict_img_lst.keys())
        self.img_num_s = 0
        self.img_num_e = self.img_num_s + 4
        self.img_on_canvas_lst_top = []

        self.img_lst_top = []
        self.button_lst_top = []
        #get first to four img
        self.top_lst = self.img_set(
            self.img_num_s,self.img_num_e,main,self.img_lst_top,self.button_lst_top,1
                )
        self.img_num_s += 4
        self.img_num_e += 4
        self.img_lst_bottom,self.button_lst_bottom = [],[]
        self.bottom_lst = self.img_set(
            self.img_num_s,self.img_num_e,main,self.img_lst_bottom,self.button_lst_bottom,2
        )

        self.next_button = tk.Button(
            main,
            width=5,
            height=10,
            text="next",
            command=self.button_next
        )
        self.next_button.grid(row=1,column=5,sticky="ns",rowspan=2)
        self.back_button = tk.Button(
            main,
            width=5,
            height=10,
            text="back",
            command=self.button_back
        )
        self.back_button.grid(row=1,column=0,sticky="ns",rowspan=2)

    def img_set(self,start_val,end_val,main,img_lst,button_lst,row_):

        for i in range(start_val,end_val):
            img = get_image(self.img_lst,i,[240,270])
            img_lst.append(img)
        for j in range(4):
            button = tk.Button(
                main,width=240,height=270,image=img_lst[j]
            )
            button_lst.append(button)
        for button,val in zip(button_lst,range(1,5)):
            button.grid(row=row_,column=val,sticky="wens")

        return button_lst
    """defines next button"""
    def button_next(self):
        self.img_num_s += 4
        if self.img_num_s >= len(self.img_lst):
            self.img_num_s = 0
        self.img_num_e += 4
        self.img_lst_top = []
        for img in range(self.img_num_s,self.img_num_e):
            try:
                self.img_lst_top.append(get_image(self.img_lst,img,[240,270]))

            except IndexError:
                self.img_lst_top.append(get_image("dummy",0,[240,270],True))
        self.img_num_s += 4
        self.img_num_e += 4
        self.img_lst_bottom = []
        for img in range(self.img_num_s,self.img_num_e):
            try:
                self.img_lst_bottom.append(get_image(self.img_lst,img,[240,270]))

            except IndexError:
                self.img_lst_bottom.append(get_image("dummy",0,[240,270],True))

        for top,img in zip(self.top_lst,self.img_lst_top):
            top.config(image=img)
        for bottom,img in zip(self.bottom_lst,self.img_lst_bottom):
            bottom.config(image=img)

    """defines bavk button"""
    def button_back(self):
        self.img_num_s -= 8
        self.img_num_e -= 8
        self.img_lst_bottom = [
            get_image(self.img_lst,i,[240,270]) for i in range(self.img_num_s,self.img_num_e)
            ]

        self.img_num_s -= 4
        self.img_num_e -= 4
        self.img_lst_top = [
            get_image(self.img_lst,i,[240,270]) for i in range(self.img_num_s,self.img_num_e)
            ]

        for top,img in zip(self.top_lst,self.img_lst_top):
            top.config(image=img)
        for bottom,img in zip(self.bottom_lst,self.img_lst_bottom):
            bottom.config(image=img)
"""defines initializing mode"""
class InitializingWindow():
    def __init__(self,configs):
        self.configs = configs
        self.main = tk.Tk()
        self.main.title("initializing")
        self.main.minsize(300,200)
        self.initializing_label = tk.Label(
            self.main
            )
        self.initializing_label.pack(ipady=10)
        self.initializing_label_text()
        self.initializing_button = tk.Button(
            self.main,
            text="初期化作業を行う",
            width=16,
            height=1,
            command=self.initializing
        )
        self.initializing_button.pack(pady=10)
        self.main.mainloop()

    def initializing_label_text(self):
        self.initializing_bool = self.configs["initializing"]
        if self.initializing_bool:
            self.initializing_label.config(text="初期化は完了しています。")
        else:
            self.initializing_label.config(text="初期化が完了していません。\n初期化を行ってください。")
    """defines initializing"""
    def initializing(self):
        if not self.initializing_bool:
            self.img_path_lst = os.listdir("image/origin")
            self.img_dic = {}
            for img in self.img_path_lst:
                self.img_dic[img] = "0"
            with open("config/vote.json", mode="w") as f:
                json.dump(self.img_dic,f)
            with open("config/time.json", mode="w") as f:
                json.dump(self.img_dic,f)
            self.configs["initializing"] = 1
            with open("config/config.json", mode="w") as f:
                json.dump(self.configs,f)
            self.initializing_label_text()
        else:
            self.askbox = msg.askyesno("initializing","初期化は完了しています。\nはいを押すとvote数が初期化されます。")
            if self.askbox:
                self.configs["initializing"] = 0
                self.initializing_bool = self.configs["initializing"]
                self.initializing()
                self.initializing_label.config(text="再初期化が完了しました。")
                quit(self.main)
            else:
                quit(self.main)


"""defines main window"""
class MainWindow():
    def __init__(self,main,configs):
        self.configs = configs
        self.main = main
        self.sort_type = self.configs["sort_type"]
        """create img list"""
        #get img keys and vote values
        with open("config/%s.json" % self.sort_type) as f:
            self.dict_img_lst = json.load(f)
            self.dict_img_lst = dict(sorted(
                                            self.dict_img_lst.items(),
                                            key=lambda x:int(x[1]),
                                            reverse=True
                                            )
                                    )

        #get img path list
        self.img_lst = list(self.dict_img_lst.keys())
        self.img_num = 0
        #get img vote list
        self.img_votes = list(self.dict_img_lst.values())
        #set first img
        self.img = get_image(self.img_lst,self.img_num,[960,540])
        #create canvas
        self.canvas = tk.Canvas(main,width=960,height=540)
        """
        self.canvas = tk.Label(
            main,
            image=self.img,
            width=960,
            height=540
        )
        """
        #self.canvas.place(x=20,y=30)

        self.canvas.grid(row=30,column=20,columnspan=960,rowspan=540,sticky="news")

        self.image_on_canvas = self.canvas.create_image(
            960/2,
            540/2,
            image=self.img
            )

        """create buttons"""
        #create next button
        self.next_button = tk.Button(
            main,
            text="next",
            command=self.button_next,
            #width=5,
            #height=10
        )
        #self.next_button.pack(side="right",fill="both")
        self.next_button.grid(row=30,column=980,columnspan=20,rowspan=540,sticky="ns")
        #create back button
        self.back_button = tk.Button(
            main,
            text="back",
            command=self.button_back,
            #width=5,
            #height=10
        )
        #self.back_button.pack(side="left",fill="both")
        self.back_button.grid(row=30,column=0,columnspan=20,rowspan=540,sticky="ns")

        #create update vote file button

        self.vote_update_button = tk.Button(
            main,
            text="update",
            command=self.update_vote_file,
            width=10,
            height=1
        )
        #self.vote_update_button.pack(anchor="nw")
        self.vote_update_button.grid(row=0,column=20,columnspan=20,rowspan=30)
        #create export button
        self.export_button = tk.Button(
            main,
            text="export",
            command=self.create_export_window,
            width=10,
            height=1
        )
        #self.export_button.pack(anchor="nw")
        self.export_button.grid(row=0,column=40,columnspan=20,rowspan=30)
        #create initializing button
        self.initializing_button = tk.Button(
            main,
            text="initializing",
            width=10,
            height=1,
            command=self.initializing
        )
        self.initializing_button.grid(row=0,column=60,columnspan=20,rowspan=30)
        #create change category mode button
        """
        self.change_cat_mode_button = tk.Button(
            main,
            text="category",
            command=self.change_cat_mode,
            width=10,
            height=3
        )
        self.change_cat_mode_button.pack(anchor="nw")
        """
        #create plus 100 vote button
        self.up_vote_100_button = tk.Button(
            main,
            text="plus100",
            command=self.plus_vote_number_100,
            width=20,
            height=1
        )
        #self.up_vote_100_button.pack(side="right",anchor="se",ipadx=50)
        self.up_vote_100_button.grid(row=570,column=850,rowspan=30,columnspan=130,ipadx=70)
        #create plus vote button
        self.up_vote_button = tk.Button(
            main,
            text="plus",
            command=self.plus_vote_number,
            width=15,
            #height=1
        )
        #self.up_vote_button.pack(side="right",anchor="se",ipadx=80)
        self.up_vote_button.grid(row=570,column=650,rowspan=30,columnspan=200,ipadx=10)
        #create minus vote 100 button
        self.minus_vote_100_button = tk.Button(
            main,
            text="minus100",
            command=self.minus_vote_number_100,
            width=20,
            #height=1
        )
        #self.minus_vote_100_button.pack(side="left",anchor="sw",ipadx=50)
        self.minus_vote_100_button.grid(row=570,column=20,rowspan=30,columnspan=130,ipadx=70)
        #create minus vote button
        self.minus_vote_button = tk.Button(
            main,
            text="minus",
            command=self.minus_vote_number,
            width=15,
            height=1
        )
        #self.minus_vote_button.pack(side="left",anchor="sw",ipadx=80)
        self.minus_vote_button.grid(row=570,column=150,rowspan=30,columnspan=200,ipadx=10)
        #create vote number
        self.vote = str(self.img_votes[self.img_num])
        self.vote_number = tk.Label(
            main,
            text=self.vote,
            font=("",16),
            width=8,
            height=1
            )
        self.vote_number.grid(row=570,column=350,rowspan=30,columnspan=300,sticky="wens")
        #self.vote_number.pack(side="bottom")
        #print(self.main.grid_size())
    """defines common pagenation button"""
    def pagenation_button(self):
        #if abs(img_num) equals length of img_lst,img_num back to zero.
        if abs(self.img_num) == len(self.img_lst):
            self.img_num = 0
        """update canvas"""

        #get image
        self.img = get_image(self.img_lst,self.img_num,[960,540])

        #draw image on main canvas

        self.image_on_canvas = self.canvas.create_image(
            960/2,
            540/2,
            image=self.img
            )

        #canvas update
        #self.canvas.itemconfig(self.image_on_canvas,image=self.img)
    """defines next button"""
    def button_next(self):
        #update vote
        self.dict_img_lst[self.img_lst[self.img_num]] = str(self.vote)
        #img_nums index plus 1
        self.img_num = plus_or_minus("plus",self.img_num)
        #execution pagenation_button
        self.pagenation_button()
        #
        self.img_votes = list(self.dict_img_lst.values())
        self.vote = str(self.img_votes[self.img_num])
        self.vote_number["text"] = self.vote
    """defines back button"""
    def button_back(self):
        #update vote
        self.dict_img_lst[self.img_lst[self.img_num]] = str(self.vote)
        #img_nums index minus 1
        self.img_num = plus_or_minus("minus",self.img_num)
        #execution pagenation_button
        self.pagenation_button()
        #
        self.img_votes = list(self.dict_img_lst.values())
        self.vote = str(self.img_votes[self.img_num])
        self.vote_number["text"] = self.vote
    """defines change vote numver"""
    def change_vote_number(self):
        #self.img_votes[self.img_num] = self.vote
        self.vote = str(self.vote)
        self.vote_number["text"] = self.vote
    """defines plus vote number"""
    def plus_vote_number(self):
        self.vote = int(self.vote)
        self.vote = plus_or_minus("plus",self.vote)
        self.change_vote_number()
    """defines plus vote 100"""
    def plus_vote_number_100(self):
        self.vote = int(self.vote)
        self.vote += 100
        self.change_vote_number()
    """defines minus vote number"""
    def minus_vote_number(self):
        self.vote = int(self.vote)
        self.vote = plus_or_minus("minus",self.vote)
        self.change_vote_number()
    """defines minus vote 100"""
    def minus_vote_number_100(self):
        self.vote = int(self.vote)
        self.vote -= 100
        self.change_vote_number()
    """defines update vote value"""
    def update_vote_file(self):
        #last update vote
        self.dict_img_lst[self.img_lst[self.img_num]] = str(self.vote)
        with open("config/vote.json", mode="w") as f:
            json.dump(self.dict_img_lst,f)
    """defines export button"""
    def create_export_window(self):
        self.sub_window_for_export = tk.Tk()
        self.sub_window_for_export.title("export_window")
        self.sub_window_for_export.minsize(100,100)
        self.window = WindowForExport(self.sub_window_for_export)
        self.sub_window_for_export.mainloop()
    """defines initializing"""
    def initializing(self):
        self.initializing_window = InitializingWindow(self.configs)
    """defines category mode button"""
    """
    def change_cat_mode(self):
        self.sub_window_for_cat_mode = tk.Tk()
        self.sub_window_for_cat_mode.title("whats_cat_name")
        self.sub_window_for_cat_mode.minsize(200,200)
        self.window = CategoryModeConfig(self.sub_window_for_cat_mode)
        self.sub_window_for_cat_mode.mainloop()
    """


if __name__ == "__main__":
    with open("config/config.json", mode="r") as f:
        configs = json.load(f)
    initializing = configs["initializing"]
    if initializing:
        root = tk.Tk()
        root.title("vote_viewer")
        root.minsize(1034,600)
        window = MainWindow(root,configs)
        root.mainloop()
    else:
        window = InitializingWindow(configs)
