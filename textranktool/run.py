import tkinter as tk
from tkinter import filedialog
import os
from TextRank import *
import json
import os
import tkinter.messagebox as Messagebox

def process():
    os.system('python split.py')
    os.system('python calwords.py')
    cal_textrank(window.get(),alpha.get())
    Messagebox.showinfo('提示', '计算完毕！')
def upload_files():
    absdir = os.getcwd()
    selectFile = tk.filedialog.askopenfilename(
        title='可选择1个或多个文件')
    filename = selectFile.split('/')[-1]
    cmd = f'copy {selectFile} {absdir}/original/corpus1.txt'.replace('/','\\')
    os.system(cmd)
    print(cmd)
    print(selectFile)
    print(filename)
    paths.insert(tk.END, selectFile + '\n')
    paths.update()
def cal_textrank(window, alpha):
    # with open('停用词表.txt', 'r', encoding='utf-8') as ban:
    #     banlist = ban.read().splitlines()
    win = int(window)
    alpha = float(alpha)
    with open('./original/corpus1.txt', 'r', encoding='utf-8') as f:
        s = f.read().replace('\n', '').strip()
        tr = TextRank(s, win, alpha, 700)
        tr.cutSentence()
        tr.createNodes()
        tr.createMatrix()
        tr.calPR()
        tr.output_matrix()
        res = tr.printResult()
    textrank = ''
    for item in res:
        # if item[0].strip() in banlist:
        #     continue
        s = str(tr.word_index[item[0]])+','+str(item).replace('(','').replace(')','').replace('\'','')+'\n'
        textrank+=s
    with open('./textrank.txt', 'w', encoding='utf-8') as w:
        w.write(textrank)
def get_textrank():
    with open('./textrank.txt', 'r', encoding='utf-8') as r:
        textrank = r.read()
    return textrank

def get_cal():
    with open('./cal/corpus1.txt', 'r', encoding='utf-8') as f:
        string = f.read()
        lis = json.loads(string)
    cal = ''
    for li in lis:
        s = str(li['x'])+','+str(li['value'])+'\n'
        cal+=s
    return cal
def print_selection():
    if (var1.get() == 1) & (var2.get() == 0):
        l.config(text='当前显示词频')
        wordfreq.insert(tk.END, get_cal() + '\n')
        wordfreq.update()
        TR.delete(1.0, 'end')
        TR.update()
    elif (var1.get() == 0) & (var2.get() == 1):
        l.config(text='当前显示TR值')
        wordfreq.delete(1.0, 'end')
        wordfreq.update()
        TR.insert(tk.END, get_textrank() + '\n')
        TR.update()
    elif (var1.get() == 0) & (var2.get() == 0):
        l.config(text='当前未勾选任何显示')
        wordfreq.delete(1.0, 'end')
        wordfreq.update()
        TR.delete(1.0, 'end')
        TR.update()
    else:
        l.config(text='当前显示词频与TR值')
        wordfreq.insert(tk.END, get_cal() + '\n')
        wordfreq.update()
        print(window)
        TR.insert(tk.END, get_textrank() + '\n')
        TR.update()

root = tk.Tk()
root.title('Textrank算法演示程序')
frm = tk.Frame(root)
frm.grid(padx='100', pady='150')
btn = tk.Button(frm, text='选择文件（txt）', command=upload_files)
btn.grid(row=0, column=0, ipadx='3', ipady='3', padx='10', pady='20')
paths = tk.Text(frm, width='50', height='2')
paths.grid(row=0, column=1)


tk.Label(frm, text='滑动窗口（整数）:', font=('Arial', 14)).grid(row=1, column=0)
tk.Label(frm, text='阻尼系数（0-1小数）:', font=('Arial', 14)).grid(row=2, column=0)


window = tk.StringVar()
window.set('3')
entry_usr_name = tk.Entry(frm, textvariable=window, font=('Arial', 14))
entry_usr_name.grid(row=1, column=1)

alpha = tk.StringVar()
alpha.set('0.85')
entry_usr_pwd = tk.Entry(frm, textvariable=alpha, font=('Arial', 14))
entry_usr_pwd.grid(row=2, column=1)

wordfreq = tk.Text(frm, width='45', height='20')
wordfreq.grid(row=4, column=0)
TR = tk.Text(frm, width='45', height='20')
TR.grid(row=4, column=1)

l = tk.Label(frm, bg='yellow', width=40, text='当前未勾选任何显示')

l.grid(row=5,column=0)

btn = tk.Button(frm, text='执行', command=process)
btn.grid(row=5, column=1, ipadx='3', ipady='3', padx='10', pady='20')
var1 = tk.IntVar()
var2 = tk.IntVar()

c1 = tk.Checkbutton(frm, text='WordFrequency',variable=var1, onvalue=1, offvalue=0, command=print_selection)    # 传值原理类似于radiobutton部件

c1.grid(row=3, column=0)
c2 = tk.Checkbutton(frm, text='TR',variable=var2, onvalue=1, offvalue=0, command=print_selection)

c2.grid(row=3, column=1)
root.mainloop()
