import os
import sys
import requests


class Attachment:  # - класс приложенного файла
    def __init__(self, name, path):
        self.name = name
        self.path = path

    def full_link(self):
        return "https://2ch.hk" + self.path


class Post:  # - класс поста
    def __init__(self, num, subject, comment, date, name, isop, files):
        self.num = num  # - номер поста
        self.subject = subject  # - заголовок
        self.comment = comment  # - текст поста
        self.date = date  # - дата, когда был оставлен пост
        self.name = name  # - имя (анон)
        self.isop = isop  # - это оп?
        self.files = files  # - лист приложенных файлов

    def op(self):  # - вернет строку "#OP", если isop
        if self.isop == 1:
            return "#OP"
        else:
            return ""


class Thread:  # - класс треда (параметр - url треда.html)
    def __init__(self, url, proxy=""):
        self.proxy = { "https" : proxy}
        jsn = requests.get(url.replace(".html", ".json"), proxies=self.proxy).json()  # - JSON
        self.Board = jsn["Board"]  # - код доски
        self.BoardName = jsn["BoardName"]  # - имя доски
        self.BoardInfoOuter = jsn["BoardInfoOuter"]  # - описание доски
        self.files_count = jsn["files_count"]  # - кол-во файлов
        self.posts = []  # - список постов (заполняется ниже)
        for p in jsn["threads"][0]["posts"]:  # - обход постов
            files = []  # - список файлов поста (заполняется ниже)
            for f in p["files"]:  # - обход файлов поста
                files.append(Attachment(f["fullname"], f["path"]))
            self.posts.append(Post(p["num"], p["subject"], p["comment"], p["date"], p["name"], p["op"], files))
        print("Thread uploaded")

    def make_html(self):
        ## - готовим каталоги
        ##
        thread_num = self.posts[0].num  # - номер треда (наверно стоило его еще в поля добавлять, но чет хз)
        thread_name = self.posts[0].subject  # - имя треда (см. выше)
        catalog_sym = "\\" if os.name == "nt" else "/"  # - путь разделяющий каталоги -- в никсах - слеш, в окнах - бекслеш
        thread_path = "{bd}-{num}".format(cs=catalog_sym, bd=self.Board, num=thread_num)  # - по данному пути находится thr.html и каталог аттачментов
        copy_number = 0  # - номер копии каталога, если такой thread_path уже существует
        while os.path.exists(thread_path):  # - если такой каталог уже есть, то добавляем ему copy №
            copy_number += 1
            thread_path = "{prev_name}-copy-{cn}".format(prev_name=thread_path, cn=copy_number)  # - ДОПИЛИТЬ -- вместо названий copy 1, copy 2, ... идут copy 1, copy 1 copy 2, ...
        attach_path = "{tp}{cs}attachments".format(cs=catalog_sym, tp=thread_path)  # - путь до аттачментов
        os.makedirs(attach_path)  # - делай котологи
        ## - пилим html-пагу треда
        ##
        html_thread_path = "{thr_path}{cs}thread.html".format(thr_path=thread_path, cs=catalog_sym)  # - путь до html треда
        html_thread = open(html_thread_path, "w", encoding="utf8")
        html_thread.write("<html>\n")
        # - Название страницы
        html_thread.write("<title>{code}-{name}</title>\n".format(code=self.Board, name=thread_name))
        # - Тело
        html_thread.write("<body>\n")
        # - Заголовок тела
        html_thread.write("<h1>/{code}/ - {name}</h1><br>\n".format(code=self.Board, name=self.BoardName))
        html_thread.write("{descr}<br><hr>\n".format(descr=self.BoardInfoOuter))
        # - Посты
        i = 0
        for p in self.posts:  # - обход постов
            # - Якорь
            # - Заголовок поста
            html_thread.write("<b id=\"{num}\">{sub}</b> - <i>{name} {date} <a href=\"#{num}\">№{num}</a></i><br>\n".format(sub=p.subject, name=p.name, date=p.date, num=p.num))
            # - Обрабатываем приложения
            html_thread.write("<table>\n<tr>\n")  # - все пики/вебмы пихаем в табличку
            for a in p.files:
                # - Выкачиваем пик/вебм
                attach_file_path = "{ap}{cs}{an}".format(ap=attach_path, cs=catalog_sym, an=a.name)
                att_resp = requests.get(a.full_link(), proxies=self.proxy)
                attach = open(attach_file_path, "wb")
                attach.write(att_resp.content)
                attach.close()
                # - пихухивоем его в таблицу (тут меняем бекслеши на прямой слеш, пушто бровзеры следуют уних-вей)
                html_thread.write("<td><a href=\"../{afp}\" target=\"_blank\"><img src=\"../{afp}\" width=200 alt=\"{an}\"></a></td>\n".format(afp=attach_file_path, an=a.name).replace("\\","/"))
            html_thread.write("</tr></table><br>\n")  # - закрываем таблу
            # - прежде чем писать текст поста надо пофиксить ссылки
            fixed_comment = p.comment.replace("/{bd}/res/".format(bd=self.Board), "")
            fixed_comment = fixed_comment.replace("{}.html".format(thread_num), "")
            # - Текст поста
            html_thread.write("<p>{comm}</p>\n".format(comm=fixed_comment, num=p.num))
            html_thread.write("<br><hr>\n")
            i += 1
            print("Post {}/{} uploaded".format(i,len(self.posts)))
        html_thread.close()


# - UI (нет)
url = ""
if len(sys.argv)==1:  # - если юзер не указал ссылку на тред
    url = input("Paste the thread\'s URL: ")  # - то предложить ему вставить ссылку на тред
else:
    url = sys.argv[1]
t = Thread(url, "https://proxy.inn.intel.com:911")
t.make_html()
