from tkinter import Tk, Frame, Label, Button, scrolledtext, StringVar, Entry, Radiobutton, IntVar, mainloop, BOTTOM, END
from tkinter.messagebox import askyesno,showinfo
from tkinter.simpledialog import askstring
from tkinter.filedialog import askopenfilename
from pypinyin import lazy_pinyin
from webbrowser import open as webopen

pktime=0#回合数
findtime=0#帮助次数

def wordinit():
    global word_list,word_list1,word_list2,word_list3,word_list4,word_before,word_len
    with open(r"模块文档\szcy1.txt",mode='r',encoding='ansi') as word_file1:
        word_list1 = word_file1.readlines()
    with open(r"模块文档\szcy2.txt",mode='r',encoding='ansi') as word_file2:
        word_list2 = word_file2.readlines()
    with open(r"模块文档\私有词库.txt",mode='r',encoding='ansi') as word_file3:
        word_list3 = word_file3.readlines()
    with open(r"模块文档\new_ciku.txt",mode='r',encoding='utf-8') as word_file4:
        word_list4 = word_file4.readlines()

    word_list = word_list1+word_list2+word_list3+word_list4
    word_before=list(word_list)
    word_len = len(word_list)

    check_a='<head>key=ansi_gb2321<!-python-!><mode>list'+'\n'
    check_f=word_before.count(check_a)
    che_a=3-check_f
    if che_a!=0:
        entry=showinfo('错误','缺少%d个转换项！建议重现安装词库!' %che_a)
        root.destroy()

def re_main_ciku():#恢复词库
    global word_list,word_before,word_len
    chengyu_web.configure(state='active')#恢复查询按钮
    try_help.configure(state='active')#恢复帮助按钮
    if word_list1+word_list2+word_list3+word_list4==word_list:
        return
    word_list=word_list1+word_list2+word_list#主词库始终放在最前
    word_before=list(word_list)
    word_len=len(word_list)

def no_main_ciku():
    global word_list,word_before,word_len
    chengyu_web.configure(state='disable')#禁用查询按钮
    try_help.configure(state='disable')#禁用帮助按钮

    main_ciku=len(word_list1+word_list2)
    word_list=word_list[main_ciku:]#去掉主词库的内容
    word_before=list(word_list)
    word_len=len(word_list)

def loser():
    global first_word,pktime,chengyu,findtime
    root.attributes('-alpha',0.6)
    v.set('在下词穷，阁下你赢了!')
    first_word = True
    entry=askyesno('恭喜阁下','你用了%s 回合战胜在下，是否再来一盘？' % pktime)
    if entry==True:
        pktime=0
        root.attributes('-alpha',1)
        MyText.delete(1.0,END)#新开始游戏时消除记录
        chengyu=[]
        findtime=0
    else:
        root.destroy()

def before_the_game():
    global record,word_example,word_net
    record = ''
    word_example=[]
    word_net=[]

def write_result():
    v2.set(record)
    MyEntry.configure(fg='blue',font=('楷体',64))
    MyEntry.insert(0,word_result[len(word_result)-1])
    MyText.tag_configure('pc',foreground='red')
    MyText.insert(END,word_result+'>>>','pc')

def find_chengyu():
    global word_list,word_len,record,word_result,first_word,pktime,chengyu,findtime
    root.attributes('-alpha',0.8)
    before_the_game()#ready for
    find_it = False
    fit=True
    letter = word_result
    u=word_result#保存中间值
    mean=letter+'\n'
    try:
        letter=letter[len(letter)-1]
    except:
        showinfo('错误','阁下，你还没有输入')
        root.attributes('-alpha',1)
        return

    for i in range(word_len):
        if letter == word_list[i][0]:
            word_example.append(word_list[i].rstrip('\n'))#要去掉每个记录中最后的换行符
            find_it=True
            first_word = False

    if find_it == False:
        showinfo('检测帮助','很遗憾，在下读书少，也找不到其它成语了……')
    elif find_it == True:
        word_result=''
        for i in word_example:
            if i not in chengyu:
                word_result=i
                if findtime!=findtime_max:#如果没有达到帮助限制，则可以帮助
                    findtime+=1
                    showinfo('检测帮助','找到了： %s \n你还有： %d 次帮助机会' % (word_result,findtime_max-findtime))
                    MyEntry.configure(fg='orange',font=('宋体',64))
                    MyEntry.delete(0,END)
                    MyEntry.insert(0,word_result)
                elif findtime==findtime_max:#如果次数已经满了，则不帮助
                    showinfo('检测帮助','阁下，你已经用完了所有的帮助机会了')
                break
        if word_result=='':
            showinfo('检测帮助','很遗憾，在下读书少，也找不到其它成语了……')

    root.attributes('-alpha',1)
    word_result=u#变量还原
    return
#------主进程开始------

#unit_0 start

def findword_0(*arg):
    global word_list,word_len,record,first_word,word_result,pktime,chengyu
    before_the_game()#ready for
    find_it = False
    fit=True
    letter = MyEntry.get()#获得输入
    mean=letter+'\n'

    if len(letter)==0:
        entry=showinfo('错误','阁下，你没有输入成语')
        return
    else:
        if first_word:
            MyText.delete(1.0,END)#新开始游戏时消除记录
        else:
            if word_result[len(word_result)-1]!=letter[0]:
                entry=showinfo('错误','阁下，你输入的成语不符合成语接龙规则')
                return
    chengyu.append(letter)

    MyEntry.delete(0,END)#清除输入框
    record+=letter+' '#增加接龙记录
    MyText.insert(END,letter+'>>>')#显示更新记录
    v2.set(record)

    letter=letter[len(letter)-1]

    for i in range(word_len):
        if letter == word_list[i][0]:
            word_example.append(word_list[i].rstrip('\n'))#要去掉每个记录中最后的换行符
            find_it=True
            first_word = False

    if find_it == False:
        loser()#pc lose the game
        return

    else:
        pktime+=1
        for i in word_example:
            if i not in chengyu:
                word_result=i
                chengyu.append(i)
                break
            else:
                loser()
                return
        v.set('第%d回合：%s' % (pktime,word_result))
        record+=word_result+' '
        write_result()
        if word_list.index(word_result+'\n')<=60933:
            chengyu_web.configure(state='active')
        else:
            chengyu_web.configure(state='disable')
        return

#unit_0 end

#unit_1 start
def findword_1(*arg):
    global word_list,word_len,record,first_word,word_result,pktime,chengyu
    before_the_game()#ready for
    find_it = False
    fit=True
    letter = MyEntry.get()#获得输入
    mean=letter+'\n'

    if len(letter)==0:
        entry=showinfo('错误','阁下，你没有输入成语')
        return
    else:
        if first_word:
            MyText.delete(1.0,END)#新开始游戏时消除记录
        else:
            if word_result[len(word_result)-1]!=letter[0]:
                entry=showinfo('错误','阁下，你输入的成语不符合成语接龙规则')
                return

    if mean not in word_before:
        if letter not in word_before:
            entry=askyesno('错误','阁下，词库未检测到有该成语，是否添加?')
            if entry==True:
                f=open('模块文档\私有词库.txt','a',encoding='ansi')
                f.write(letter+'\n')
                f.close()
                wordinit()
            else:
                pass
            return
    chengyu.append(letter)

    MyEntry.delete(0,END)#清除输入框
    record+=letter+' '#增加接龙记录
    MyText.insert(END,letter+'>>>')#显示更新记录
    v2.set(record)

    letter=letter[len(letter)-1]

    for i in range(word_len):
        if letter == word_list[i][0]:
            word_example.append(word_list[i].rstrip('\n'))#要去掉每个记录中最后的换行符
            find_it=True
            first_word = False

    if find_it == False:
        loser()#pc lose the game
        return

    else:
        word_result=''
        pktime+=1
        for i in word_example:
            if i not in chengyu:
                word_result=i
                chengyu.append(i)
                break
            else:
                pass
        if word_result!='':
            v.set('第%d回合：%s' % (pktime,word_result))
            record+=word_result+' '
            chengyu.append(word_result)
            chengyu.append(word_result)
            write_result()
            if word_list.index(word_result+'\n')<=60933:
                chengyu_web.configure(state='active')
            else:
                chengyu_web.configure(state='disable')
            return
        else:
            loser()
            return
#unit_1 end

#unti_2 start
def findword_2(*arg):
    global word_list,word_len,record,first_word,word_result,pktime,chengyu
    before_the_game()#ready for
    find_it = False
    fit=True
    letter = MyEntry.get()#获得输入
    mean=letter+'\n'
    last_pinyin=letter[-1]

    if len(letter)==0:
        entry=showinfo('错误','阁下，你没有输入成语')
        return
    else:
        if first_word:
            MyText.delete(1.0,END)#新开始游戏时消除记录
        else:
            if word_result[len(word_result)-1]!=letter[0]:
                if lazy_pinyin(letter[0])!=lazy_pinyin(word_result[-1]):
                    entry=showinfo('错误','阁下，你输入的成语不符合成语接龙规则')
                    return

    if mean not in word_before:
        if letter not in word_before:
            entry=showinfo('错误','阁下，你输入的成语不在词库，请重新输入')
            return

    if letter in chengyu:
        showinfo('错误','阁下，游戏中已经出现过该成语了！')
        return
    chengyu.append(letter)

    MyEntry.delete(0,END)#清除输入框
    record+=letter+' '#增加接龙记录
    MyText.insert(END,letter+'>>>')#显示更新记录
    v2.set(record)

    letter=letter[len(letter)-1]

    for i in range(word_len):
        if letter == word_list[i][0]:
            word_example.append(word_list[i].rstrip('\n'))#要去掉每个记录中最后的换行符
            find_it=True
            first_word = False

    if find_it == False:
        try_pinyin=lazy_pinyin(last_pinyin)
        pinyin=False
        for i in word_list:#拼音识别
            example_pinyin=lazy_pinyin(i[0])#成语库的成语的第一个字的拼音
            if try_pinyin==example_pinyin:
                word_example.append(i.rstrip('\n'))
                pinyin=True
            else:
                pass

        if pinyin==False:
            loser()#pc lose the game
        else:
            word_result=''
            for i in word_example:
                if i not in chengyu:
                    word_result=i
                    break
                else:
                    pass
            if word_result!='':
                pktime+=1
                v.set('第%d回合：%s' % (pktime,word_result))
                record+=word_result+' '
                chengyu.append(word_result)
                first_word = False#确认开始游戏
                write_result()
                if word_list.index(word_result)<=60933:
                    chengyu_web.configure(state='active')
                else:
                    chengyu_web.configure(state='disable')
                return
            else:
                loser()
                return


    else:
        word_result=''
        pktime+=1
        for net in word_example:
            net=net[len(net)-1]
            for q in range(word_len):
                if net == word_list[q][0]:
                    word_net.append(word_list[q].rstrip('\n'))
                    fit=True
                    fiw=False
                if fit==False:
                    for i in word_net:
                        if i not in chengyu:
                            word_result=i
                            break
                        else:
                            pass
                    if word_result!='':
                        v.set('第%d回合：%s' % (pktime,word_result))
                        record+=word_result+' '
                        chengyu.append(word_result)
                        write_result()
                        if word_list.index(word_result+'\n')<=60933:
                            chengyu_web.configure(state='active')
                        else:
                            chengyu_web.configure(state='disable')
                        return
                    else:
                        loser()
                        return
                else:
                    for i in word_example:
                        if i not in chengyu:
                            word_result=i
                            break
                        else:
                            pass
                    if word_result!='':
                        v.set('第%d回合：%s' % (pktime,word_result))
                        record+=word_result+' '
                        chengyu.append(word_result)
                        write_result()
                        if word_list.index(word_result+'\n')<=60933:
                            chengyu_web.configure(state='active')
                        else:
                            chengyu_web.configure(state='disable')
                        return
                    else:
                        loser()
                        return
#unit_2 end

def closewindow():
    root.attributes('-alpha',0.75)
    entry = askyesno(title='确认', message='阁下实在答不出来？退出？')
    if entry==True:
        root.destroy()
    else:
        root.attributes('-alpha',1)
    return

#主程序截止----------------
def gybx():
    root.attributes('-alpha',0.8)
    showinfo('编写说明','编写者:Smart-Space 🐲'+'\n'
             '说明：该游戏基于Pyhon3.8，同时配备相关模块以及进程'+'\n'
             '本游戏的主题为成语接龙，是一项中国传统游戏。展示你的成语储备吧！'+'\n'
             '注：该版本优化词库策略。详情请看版本说明。'+'\n')
    root.attributes('-alpha',1)
    return

def bbsm():
    root.attributes('-alpha',0.8)
    showinfo('版本说明','总版本：成语接龙 第七代'+'\n'
             '内部版本：7.0'+'\n'
             '版本信息：~~~~~混进了一些非成语的词语~~~~~'+'\n'
             '优化项目：1、严格版支持拼音接龙（无视音调，使用电脑的拼音接龙时，会增加cpu能耗）'+'\n'
             '2、优化检测帮助'+'\n'
             '3、允许玩家添加额外词库'+'\n'
             '4、按回车即可接龙')
    root.attributes('-alpha',1)
    return

def ckxx():
    root.attributes('-alpha',0.8)
    showinfo('词库信息','主词库：4.0'+'\n'
             '多元词库：4.0'+'\n'
             '自定义词库：自定转换'+'\n'
             '说明：该版本的自定义词库可以根据玩家需求，玩家主动添加词汇')
    root.attributes('-alpha',1)
    return

def check_web():
    if word_result=='':
        showinfo('网络查询','机器没有输出任何成语。该功能只针对电脑输出的成语进行查询。')
        return
    webopen('https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&ch=3&tn=98012088_4_dg&wd='+word_result)
    return

def cksr():
    root.attributes('-alpha',0.7)
    newin=askstring('成语输入（给功能只作为补充功能）','请在下方输入你想有新增的成语，请尊重中国传统文化==>>>',initialvalue='键入成语')
    try:
        f=open('模块文档\私有词库.txt','a',encoding='ansi')
        f.write(newin+'\n')
        f.close()
        wordinit()
    except:
        pass
    root.attributes('-alpha',1)
    return

def find_newciku():
    global word_list,word_before,word_len
    newfile=askyesno('添加词库','将*.txt词库添加到模块文档以后永久有效'+'\n'
                     '如果现在添加新词库，只是本次有效，需要utf-8编码的文件'+'\n'
                     '是否添加新词库')
    if newfile==True:
        ciku=askopenfilename(title='添加词库',filetype=[('新词库','*.txt')],initialdir='G:/')
        if ciku=='':
            return
        else:
            with open(ciku,mode='r',encoding='utf-8') as f:
                new=f.readlines()
            word_list = word_list+new
            word_before=list(word_list)
            word_len = len(word_list)

            put_in=askyesno('建立永久词库','是否将所选词库放入原生词库文档？')
            if put_in==True:
                f=open(r'模块文档\new_ciku.txt',mode='w',encoding='utf-8')
                if new[-1][-1]=='\n':#如果最后是换行符，直接写入；否则加一行
                    for i in new:
                        f.write(i)
                else:
                    for i in new:
                        f.write(i)
                    f.write('\n')
                f.close()
            else:
                pass
    else:
        pass

def find_kaiyuan():
    showinfo('开源项目','最终版本发布后，已开源至CSDN'+'\n'
             'https://download.csdn.net/download/tinga_kilin/12134956')
    return
#配置程序截止------------------

#前置选择-------------
start=Tk()
start.withdraw()
programme=askstring('版本输入','请输入版本以开始游戏（键入数字）'+'\n'+'学习版（0）'+'\n'+'基础版（1）'+'\n'+'严格版（2）',initialvalue='（键入数字,exit退出）')

while programme!='exit':
    if programme=='0':
        os=0
        form='学习版'
        break
    elif programme=='1':
        os=1
        form='基础版'
        break
    elif programme=='2':
        os=2
        form='严格版'
        break
    else:
        showinfo('错误','此命令无法生效，请再次输入')
        programme=askstring('版本输入','请输入版本以开始游戏（键入数字）'+'\n'+'学习版（0）'+'\n'+'基础版（1）'+'\n'+'严格版（2）',initialvalue='（键入数字,exit退出）')

start.destroy()
#前置选择-------------
root = Tk() #创建tk窗口
root.geometry('1024x790') #定义窗口大小
root.title('词语接龙7.0    '+form)
root['background']='whitesmoke'

word_list=[]    #建立汉语常用词语列表
word_before=[]
word_len=0
first_word=True #是否第一次输入词语
word_result=''

record='' #词语接龙的记录

v = StringVar()
Label(root,textvariable=v,fg='black',bg='snow',font=('宋体',48)).pack()
v.set('输入一个成语开始游戏：')

MyEntry=Entry(root,fg='blue',bg='powderblue',width=18,relief='groove',font=('楷体',64))
MyEntry.pack()

if os==0:
    form=Button(root,text='确认成语',width=10, font=('宋体',32),fg='cyan',activebackground='lightskyblue',default='normal',relief='groove',command=findword_0)
    findtime_max=50
    root.bind('<Return>',findword_0)
elif os==1:
    form=Button(root,text='确认成语',width=10, font=('宋体',32),fg='cyan',activebackground='lightskyblue',default='normal',relief='groove',command=findword_1)
    findtime_max=10
    root.bind('<Return>',findword_1)
elif os==2:
    form=Button(root,text='确认成语',width=10, font=('宋体',32),fg='cyan',activebackground='lightskyblue',default='normal',relief='groove',command=findword_2)
    findtime_max=5
    root.bind('<Return>',findword_2)
form.pack()

Button(root,text='失败退出',width=10, font=('宋体',32),fg='pink',bg='whitesmoke',activebackground='red',activeforeground='blue',relief='flat',command=closewindow).pack()

use_ciku=IntVar()
seem=Frame(root)
seem.pack(side='top')
Label(seem,text='词库状态: ').pack(side='left')
Radiobutton(seem,text='取消主词库',value=1,variable=use_ciku,command=no_main_ciku).pack(side='left')
Radiobutton(seem,text='默认主词库',value=2,variable=use_ciku,command=re_main_ciku).pack(side='left')
use_ciku.set(2)

cbox=Frame(root)
cbox.pack()
Button(cbox,text='关于编写',font=('宋体',18),activebackground='mediumturquoise',relief='ridge',comman=gybx).pack(side='left')
Button(cbox,text='版本说明',font=('宋体',18),activebackground='mediumturquoise',relief='ridge',comman=bbsm).pack(side='left')
Button(cbox,text='词库信息',font=('宋体',18),activebackground='mediumturquoise',relief='ridge',comman=ckxx).pack(side='left')
chengyu_input=Button(cbox,text='词库输入',font=('宋体',18),activebackground='mediumturquoise',relief='ridge',comman=cksr)
chengyu_input.pack(side='left')
if os==0 or os==1:
    chengyu_input.configure(state='disable')
chengyu_web=Button(cbox,text='成语查询',font=('宋体',18),activebackground='mediumturquoise',relief='ridge',comman=check_web)
chengyu_web.pack(side='left')
try_help=Button(cbox,text='检测帮助',font=('宋体',18),activebackground='mediumturquoise',comman=find_chengyu)
try_help.pack(side='left')
Button(cbox,text='添加词库',font=('宋体',18),activebackground='mediumturquoise',comman=find_newciku).pack(side='left')
Button(cbox,text='开源项目',font=('宋体',18),activebackground='mediumturquoise',comman=find_kaiyuan).pack(side='left')

v2 = StringVar()
MyText=scrolledtext.ScrolledText(root, fg='cyan',bg='darkslateblue', font=('宋体',24))
MyText.pack(side=BOTTOM)

try:
    wordinit() #读入常用词语表
except:
    entry=showinfo('错误','词库选入异常！请查看词库是否保存关闭！')
    root.destroy()

chengyu=[]

MyEntry.focus_set()
mainloop()