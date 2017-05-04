from django.shortcuts import render
from django.utils import timezone
from .models import Post
from django.shortcuts import render, get_object_or_404
from .forms import PostForm
from django.shortcuts import redirect
from .models import File
from .forms import FileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import DocumentForm
from django.http import HttpResponse
import os
from random import randint
from .models import CupReport
from django.db import connection, transaction
import json
import decimal
from collections import OrderedDict
from collections import Set


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_details.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})


def post_filedetail(request, pk):
    info = get_object_or_404(File, pk=pk)
    return render(request, 'blog/post_filedetail.html', {'info': info})


def post_createFile(request):
    if request.method == 'POST':
        fileform = FileForm(request.POST)
        if fileform.is_valid():
            info = fileform.save()
            generateFile(info.pk)
            return redirect('post_filedetail', pk=info.pk)
    else:
        fileform = FileForm()
    return render(request, 'blog/post_createFile.html', {'fileform': fileform})


def post_editfileinfo(request, pk):
    filenumber = get_object_or_404(File, pk=pk)
    if request.method == 'POST':
        fileform = FileForm(request.POST, instance=filenumber)
        if fileform.is_valid():
            info = fileform.save()
            generateFile(info.pk)
            return redirect('post_filedetail', pk=info.pk)
    else:
        fileform = FileForm(instance=filenumber)
    return render(request, 'blog/post_createFile.html', {'fileform': fileform})


def post_showFileInfo(request):
    fileinfo = File.objects.all()
    return render(request, 'blog/post_showFileInfo.html', {'fileinfo': fileinfo})


def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'blog/simple_upload.html', {'uploaded_file_url': uploaded_file_url})
    return render(request, 'blog/simple_upload.html')


def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = DocumentForm()
    return render(request, 'blog/model_form_upload.html', {'form': form})


def generateFile(pk):
    getinfo = get_object_or_404(File, pk=pk)

    if len(getinfo.kobocat_port) > 0 and len(getinfo.kobocat_domain) > 0 and len(getinfo.src_directory) > 0 and len(
            getinfo.kobocat_socket) > 0:
        #   filename = getnewfilename()
        #    fo = open(filename, "w")

        filename = os.path.join(os.path.abspath('/home/sazzad/djangogirls/blog/CreatedFile'), 'kobocat')
        fo = open(filename, "w")
        fo.write("server {\n" +
                 "    listen " + getinfo.kobocat_port + ";\n" +
                 "    server_name " + getinfo.kobocat_domain + ";\n\n" +

                 "    location = /favicon.ico { access_log off; log_not_found off; }\n" +
                 "    location /static/ {\n" +
                 "        root " + getinfo.src_directory + "/kobocat-template;\n" +
                 "        try_files $uri $uri/ @secondStatic;\n" +
                 "    }\n" +
                 "    location @secondStatic {\n" +
                 "        root " + getinfo.src_directory + "/kobocat/onadata/apps/main;\n" +
                 "        try_files $uri $uri/ @thirdStatic;\n" +
                 "    }\n" +
                 "    location @thirdStatic {\n" +
                 "        root " + getinfo.src_directory + "/kobocat/onadata;\n" +
                 "    }\n" +
                 "    location /media {\n" +
                 "        alias " + getinfo.src_directory + "/kobocat/onadata/media;\n" +
                 "    }\n" +
                 "    location / {\n" +
                 "        include         uwsgi_params;\n" +
                 "        uwsgi_pass      unix:" + getinfo.kobocat_socket + ";\n" +
                 "        proxy_redirect off;\n" +
                 "        proxy_set_header Host $host;\n" +
                 "        proxy_set_header X-Real-IP $remote_addr;\n" +
                 "        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;\n" +
                 "    }\n"
                 "}\n")
    if len(getinfo.koboform_domain) > 0 and len(getinfo.koboform_port) > 0 and len(getinfo.src_directory) > 0 and len(
            getinfo.koboform_socket) > 0:
        filename = os.path.join(os.path.abspath('/home/sazzad/djangogirls/blog/CreatedFile'), 'koboform')
        print("File name" + filename)
        fo = open(filename, "w")
        fo.write("server {\n" +
                 "    listen " + getinfo.koboform_port + ";\n" +
                 "    server_name " + getinfo.koboform_domain + ";\n\n" +

                 "    location = /favicon.ico { access_log off; log_not_found off; }\n" +
                 "    location /static/ {\n" +
                 "        root " + getinfo.src_directory + "/koboform/dkobo;\n" +
                 "        try_files $uri $uri/ @secondStatic;\n" +
                 "    }\n" +
                 "    location @secondStatic {\n" +
                 "        root " + getinfo.src_directory + "/koboform;\n" +
                 "    }\n" +
                 "    location / {\n" +
                 "        include         uwsgi_params;\n" +
                 "        uwsgi_pass      unix:" + getinfo.koboform_socket + ";\n" +
                 "    }\n"
                 "}\n")

    if len(getinfo.enketo_server_domain) > 0 and len(getinfo.enketo_server_port) > 0 and len(
            getinfo.enketo_web_domain) > 0 and len(getinfo.enketo_web_port) > 0:
        filename = os.path.join(os.path.abspath('/home/sazzad/djangogirls/blog/CreatedFile'), 'enketo')
        fo = open(filename, "w")
        fo.write("server {\n" +
                 "    listen " + getinfo.enketo_server_port + ";\n" +
                 "    server_name " + getinfo.enketo_server_domain + ";\n\n" +
                 "    location / {\n" +
                 "        proxy_pass  http://" + getinfo.enketo_web_domain + ":" + getinfo.enketo_web_port + ";\n" +
                 "        proxy_redirect off;\n" +
                 "        proxy_set_header Host $host;\n" +
                 "        proxy_set_header X-Real-IP $remote_addr;\n" +
                 "        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;\n" +
                 "    }\n"
                 "}\n")

    if len(getinfo.koboform_socket) > 0 and len(getinfo.src_directory) > 0 and len(getinfo.virtualenv) > 0 \
            and len(getinfo.koboform_domain) > 0 and len(getinfo.koboform_port) > 0 and len(
        getinfo.kobocat_domain) > 0 and len(getinfo.kobocat_port) > 0 \
            and len(getinfo.db_database_name) > 0 and len(getinfo.db_user) > 0 and len(getinfo.db_password) > 0 and len(
        getinfo.db_server_ip) > 0 \
            and len(getinfo.db_port) > 0 and len(getinfo.enketo_server_domain) > 0:
        filename = os.path.join(os.path.abspath('/home/majbah/djangogirls/blog/CreatedFile/uwsgi/sites'),
                                'koboform.ini')
        fo = open(filename, "w")
        fo.write("[uwsgi]\n" +
                 "socket=" + getinfo.koboform_socket + "\n" +
                 "chmod-socket=777\n" +
                 "uid=www-data\n" +
                 "gid=www-data"        "chdir=" + getinfo.src_directory + "/koboform\n" +
                 "module=dkobo.wsgi:application\n" +
                 "master=True\n" +
                 "processes=8\n" +
                 "vacuum=True                 # clear environment on exit\n" +
                 "logto=/home/devashish/log/koboform.log\n" +
                 "virtualenv=" + getinfo.virtualenv + "\n" +
                 "static-map=/static=" + getinfo.src_directory + "/koboform/dkobo/static\n" +
                 "buffer-size=8192\n" +
                 "env=HTTPS=on\n" +
                 "env=PROFILE_PATH=/home/devashish/.profile\n" +
                 "env=V_R=/home/devashish\n" +
                 "env=V_E=/home/devashish/env\n" +
                 "env=V_S=/home/devashish/scripts\n" +
                 "env=V_L=/home/devashish/logs\n" +
                 "env=SRC_DIR=" + getinfo.src_directory + "\n" +
                 "env=HTTP_PROTOCOL=http\n" +
                 "env=PIP_DOWNLOAD_CACHE=/home/devashish/.pip_cache\n" +
                 "env=SERVER_IP=127.0.0.1\n" +
                 "env=ip=192.168.22.25\n" +
                 "env=KOBOFORM_URL=http://" + getinfo.koboform_domain + ":" + getinfo.koboform_port + "\n" +
                 "env=KOBOFORM_SERVER_PORT=" + getinfo.koboform_port + "\n" +
                 "env=KOBOCAT_URL=http://" + getinfo.kobocat_domain + ":" + getinfo.kobocat_port + "\n" +
                 "env=KOBOCAT_SERVER_PORT=" + getinfo.kobocat_port + "\n" +
                 "env=KOBOCAT_INTERNAL_URL=http://" + getinfo.kobocat_domain + ":" + getinfo.kobocat_port + "\n" +
                 "env=ENKETO_EXPRESS_SERVER_PORT=80\n" +
                 "env=KOBOCAT_REPO=https://github.com/kobotoolbox/kobocat.git\n" +
                 "env=KOBOCAT_BRANCH=master\n" +
                 "env=KOBOCAT_PATH=" + getinfo.src_directory + "/kobocat\n" +
                 "env=KOBOCAT_TEMPLATES_REPO=https://github.com/kobotoolbox/kobocat-template.git\n" +
                 "env=KOBOCAT_TEMPLATES_BRANCH=master\n" +
                 "env=KOBOCAT_TEMPLATES_PATH=" + getinfo.src_directory + "/kobocat-template\n" +
                 "env=KOBOFORM_PREVIEW_SERVER=http://" + getinfo.koboform_domain + ":" + getinfo.koboform_port + "\n" +
                 "env=KOBOFORM_REPO=https://github.com/kobotoolbox/dkobo.git\n" +
                 "env=KOBOFORM_BRANCH=master\n" +
                 "env=KOBOFORM_PATH=" + getinfo.src_directory + "/koboform\n" +
                 "env=PSQL_ADMIN=postgres\n" +
                 "env=KOBO_PSQL_DB_NAME=" + getinfo.db_database_name + "\n" +
                 "env=KOBO_PSQL_DB_USER=" + getinfo.db_user + "\n" +
                 "env=KOBO_PSQL_DB_PASS=" + getinfo.db_password + "\n" +
                 "env=DATABASE_SERVER_IP=" + getinfo.db_server_ip + "\n" +
                 "env=DATABASE_URL=postgis://" + getinfo.db_user + ":" + getinfo.db_password + "@" + getinfo.db_server_ip + ":" + getinfo.db_port + "/" + getinfo.db_database_name + "\n" +
                 "env=DEFAULT_KOBO_USER=kobo\n" +
                 "env=DEFAULT_KOBO_PASS=kobo\n" +
                 "env=ENKETO_EXPRESS_REPO_DIR=" + getinfo.src_directory + "/enketo-express\n" +
                 "env=ENKETO_EXPRESS_UPDATE_REPO=false\n" +
                 "env=ENKETO_SERVER=http://" + getinfo.enketo_server_domain + "\n" +
                 "env=ENKETO_PREVIEW_URI=/preview\n" +
                 "env=ENKETO_URL=http://" + getinfo.enketo_server_domain + "\n" +
                 "env=ENKETO_API_ROOT=/api/v2\n" +
                 "env=ENKETO_OFFLINE_SURVEYS=True\n" +
                 "env=ENKETO_API_ENDPOINT_PREVIEW=/preview\n" +
                 "env=ENKETO_PROTOCOL=http\n" +
                 "env=ENKETO_API_TOKEN=enketorules\n" +
                 "env=SENDER_MANAGER_PATH" +
                 '","' + getinfo.src_directory + '/messagesender\n' +
                 "env=SENDER_MANAGER_HOST=192.168.22.25\n" +
                 "env=SENDER_MANAGER_PORT=1884\n" +
                 "env=SENDER_MANAGER_DATABASE_SCHEMA=innovation\n" +
                 "env=SENDER_MANAGER_DATABASE_HOST=127.0.0.1\n" +
                 "env=SENDER_MANAGER_DATABASE_PORT=" + getinfo.db_port + "\n" +
                 "env=SENDER_MANAGER_DATABASE_USER=" + getinfo.db_user + "\n" +
                 "env=SENDER_MANAGER_DATABASE_PWD=" + getinfo.db_password + "\n" +
                 "env=DJANGO_LIVE_RELOAD=False\n" +
                 "env=DJANGO_SITE_ID=1\n" +
                 "env=DJANGO_SECRET_KEY=P2Nerc3oG2564z5mHTGUhAoh2CzOMVenWBNMNWgWU796n\n" +
                 "env=CLEAN_APT_CACHE=True\n" +
                 "env=AUTOLAUNCH=1\n" +
                 "env=PYTHONPATH=/home/devashish/env:\n" +
                 "env=DJANGO_SETTINGS_MODULE=dkobo.settings\n")

    if len(getinfo.kobocat_socket) > 0 and len(getinfo.src_directory) > 0 and len(getinfo.virtualenv) > 0 \
            and len(getinfo.koboform_domain) > 0 and len(getinfo.koboform_port) > 0 and len(
        getinfo.kobocat_domain) > 0 and len(getinfo.kobocat_port) > 0 \
            and len(getinfo.db_database_name) > 0 and len(getinfo.db_user) > 0 and len(getinfo.db_password) > 0 and len(
        getinfo.db_server_ip) > 0 \
            and len(getinfo.db_port) > 0 and len(getinfo.enketo_server_domain) > 0 and len(
        getinfo.enketo_server_port) > 0:
        filename = os.path.join(os.path.abspath('/home/sazzad/djangogirls/blog/CreatedFile/uwsgi/sites'), 'kobocat.ini')
        fo = open(filename, "w")
        fo.write("[uwsgi]\n" +
                 "#http=:3030\n" +
                 "socket=" + getinfo.kobocat_socket + "\n" +
                 "chmod-socket=777\n" +
                 "uid=www-data\n" +
                 "gid=www-data\n" +
                 "chdir=" + getinfo.src_directory + "/kobocat\n" +
                 "module=onadata.apps.main.wsgi:application\n" +
                 "master=True\n" +
                 "processes=8\n" +
                 "pidfile=/home/devashish/log/ona.pid\n" +
                 "vacuum=True                 # clear environment on exit\n" +
                 "harakiri=240                # respawn processes taking more than 240 seconds\n" +
                 "max-requests=5000           # respawn processes after serving 5000 requests\n" +
                 "logto=/home/devashish/log/onadata.log\n" +
                 "virtualenv=" + getinfo.virtualenv + "\n" +
                 "static-map=/static=" + getinfo.src_directory + "/kobocat/onadata/apps/main/static\n" +
                 "buffer-size=8192\n" +
                 "env=HTTPS=on\n" +
                 "stats=/tmp/onastats.sock\n" +
                 "env=PROFILE_PATH=/home/devashish/.profile\n" +
                 "env=V_R=/home/devashish\n" +
                 "env=V_E=/home/devashish/env\n" +
                 "env=V_S=/home/devashish/scripts\n" +
                 "env=V_L=/home/devashish/logs\n" +
                 "env=SRC_DIR=" + getinfo.src_directory + "\n" +
                 "env=HTTP_PROTOCOL=https\n" +
                 "env=PIP_DOWNLOAD_CACHE=/home/devashish/.pip_cache\n" +
                 "env=SERVER_IP=127.0.0.1\n" +
                 "env=ip=192.168.22.25\n" +
                 "env=KOBOFORM_URL=http://" + getinfo.koboform_domain + ":" + getinfo.koboform_port + "\n" +
                 "env=KOBOFORM_SERVER_PORT=" + getinfo.koboform_port + "\n" +
                 "env=KOBOCAT_URL=http://" + getinfo.kobocat_domain + ":" + getinfo.kobocat_port + "\n" +
                 "env=KOBOCAT_SERVER_PORT=" + getinfo.kobocat_port + "\n" +
                 "env=KOBOCAT_INTERNAL_URL=http://" + getinfo.kobocat_domain + ":" + getinfo.kobocat_port + "\n" +
                 "env=ENKETO_EXPRESS_SERVER_PORT=8005\n" +
                 "env=KOBOCAT_REPO=https://github.com/kobotoolbox/kobocat.git\n" +
                 "env=KOBOCAT_BRANCH=master\n" +
                 "env=KOBOCAT_PATH=" + getinfo.src_directory + "/kobocat\n" +
                 "env=KOBOCAT_TEMPLATES_REPO=https://github.com/kobotoolbox/kobocat-template.git\n" +
                 "env=KOBOCAT_TEMPLATES_BRANCH=master\n" +
                 "env=KOBOCAT_TEMPLATES_PATH=" + getinfo.src_directory + "/kobocat-template\n" +
                 "env=KOBOFORM_PREVIEW_SERVER=http://" + getinfo.koboform_domain + ":" + getinfo.koboform_port + "\n" +
                 "env=KOBOFORM_REPO=https://github.com/kobotoolbox/dkobo.git\n" +
                 "env=KOBOFORM_BRANCH=master\n" +
                 "env=KOBOFORM_PATH=" + getinfo.src_directory + "/koboform\n" +
                 "env=PSQL_ADMIN=postgres\n" +
                 "env=KOBO_PSQL_DB_NAME=" + getinfo.db_database_name + "\n" +
                 "env=KOBO_PSQL_DB_USER=" + getinfo.db_user + "\n" +
                 "env=KOBO_PSQL_DB_PASS=" + getinfo.db_password + "\n" +
                 "env=DATABASE_SERVER_IP=" + getinfo.db_server_ip + "\n" +
                 "env=DATABASE_URL=postgis://" + getinfo.db_user + ":" + getinfo.db_password + "@" + getinfo.db_server_ip + ":" + getinfo.db_port + "/" + getinfo.db_database_name + "\n" +
                 "env=DEFAULT_KOBO_USER=" + getinfo.db_user + "\n" +
                 "env=DEFAULT_KOBO_PASS=" + getinfo.db_password + "\n" +
                 "env=ENKETO_EXPRESS_REPO_DIR=" + getinfo.src_directory + "/enketo-express\n" +
                 "env=ENKETO_EXPRESS_UPDATE_REPO=false\n" +
                 "env=ENKETO_SERVER=http://" + getinfo.enketo_server_domain + ":" + getinfo.enketo_server_port + "\n" +
                 "env=ENKETO_PREVIEW_URI=/preview\n" +
                 "env=ENKETO_URL=http://" + getinfo.enketo_server_domain + ":" + getinfo.enketo_server_port + "\n" +
                 "env=ENKETO_API_ROOT=/api/v2\n" +
                 "env=ENKETO_OFFLINE_SURVEYS=True\n"
                 "env=ENKETO_API_ENDPOINT_PREVIEW=/preview\n" +
                 "env=ENKETO_PROTOCOL=http\n" +
                 "env=ENKETO_API_TOKEN=enketorules\n" +
                 "env=SENDER_MANAGER_PATH"
                 '","' + getinfo.src_directory + '/messagesender\n' +
                 "env=SENDER_MANAGER_HOST=192.168.22.25\n" +
                 "env=SENDER_MANAGER_PORT=1884\n" +
                 "env=SENDER_MANAGER_DATABASE_SCHEMA=newdawn\n" +
                 "env=SENDER_MANAGER_DATABASE_HOST=127.0.0.1\n" +
                 "env=SENDER_MANAGER_DATABASE_PORT=" + getinfo.db_port + "\n" +
                 "env=SENDER_MANAGER_DATABASE_USER=" + getinfo.db_user + "\n" +
                 "env=SENDER_MANAGER_DATABASE_PWD=" + getinfo.db_password + "\n" +
                 "env=DJANGO_LIVE_RELOAD=False\n" +
                 "env=DJANGO_SITE_ID=1\n" +
                 "env=DJANGO_SECRET_KEY=P2Nerc3oG2564z5mHTGUhAoh2CzOMVenWBNMNWgWU796n\n" +
                 "env=CLEAN_APT_CACHE=True\n" +
                 "env=AUTOLAUNCH=1\n" +
                 "env=PYTHONPATH=/home/devashish/env:\n" +
                 "env=DJANGO_SETTINGS_MODULE=kobocat_settings")


## Create Normal File

def create(request):
    context = {'error': ''}
    if request.method == 'POST':
        if request.POST.__contains__('content'):
            filename = getnewfilename()
            fo = open(filename, "w")
            fo.write(request.POST['content'])
            return redirect('post_list')
        else:
            context['error'] += 'Request doesnt contain any content to create a file\n'
    else:
        context['error'] += 'Request type must be POST\n'

    return render(request, 'blog/create.html', {'context': context})


FILES = '/home/majbah/djangogirls/blog/CreatedFile'


## Create Normal File - Get FileName

def getnewfilename():
    td = str(randint(0, 10000))
    filename = 'koboform_' + td
    return os.path.join(os.path.abspath(FILES), filename)


## Reporting view

def makechart(request):
    return render(request, 'blog/report.html')


## Cup Report


## ******** Another Table field Data  (Satrt)***********

# def cupReportChart(request):
#     query = "SELECT * FROM blog_cupreport";
#     countLegend = "SELECT distinct(name) FROM blog_cupreport";
#
#     # order_dict = __db_fetch_values_dict(query);
#     jsonForChart = generateChartData('name', 'value', 'category', query)
#     return render(request, 'blog/cupReport.html', {'jsonForChart': jsonForChart})


## ************* Another Table filed Data (End) **************

def cupReportChart(request):
    query = "SELECT cast( (unnest(string_to_array(json->>\'school_age_child_status\',\' \'))) as int ) as name, to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month')  as category ,count(id) as value FROM logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null group by name,category order by name asc";
    queryTable = " SELECT (json-> 'hh_id' ) as hh_id, string_to_array(json->>'school_age_child_status',' ') as name , to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month') as category FROM public.logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null";

    # countLegend = "SELECT"
    # "distinct cast( (unnest(string_to_array(json->>'school_age_child_status',' '))) as int ) as name"
    # "FROM public.logger_instance where xform_id = 350"
    # "and (json->>'school_age_child_status') is not null order by name asc";
    jsonForChart = generateChartData('name', 'value', 'category', query)
    jsonForChartTable = generateChartDataTable(queryTable)
    return render(request, 'blog/cupReport.html', {'jsonForChart': jsonForChart,'jsonForChartTable':jsonForChartTable})




def generateChartDataTable(query):
    cursor = connection.cursor()
    cursor.execute(query)
    fetchVal = dictfetchall(cursor)
    cursor.close()
    listDataForTable = json.dumps({'tableData':fetchVal}, default=decimal_default)

    return listDataForTable;



def __db_fetch_values_dict(query):
    cursor = connection.cursor()
    cursor.execute(query)
    fetchVal = dictfetchall(cursor)
    cursor.close()
    return fetchVal


def dictfetchall(cursor):
    desc = cursor.description
    return [
        OrderedDict(zip([col[0] for col in desc], row))
        for row in cursor.fetchall()]


def generateChartData(name_field, data_field, category_field, query):

    dataset = __db_fetch_values_dict(query);
    uniqueList = getUniqueValues(dataset, name_field)
    category_list = getUniqueValues(dataset, category_field)
    seriesData = []
    for ul in uniqueList:
        print(ul)
        dict = {}
        dict['name'] = ul;

        dict['data'] = [nameTodata[data_field] for nameTodata in dataset if nameTodata[name_field] == ul]
        seriesData.append(dict)

    jsonForChart = json.dumps({'cat_list': category_list, 'total': seriesData}, default=decimal_default)

    return jsonForChart


def getUniqueValues(dataset, colname):
    list = [];

    for dis in dataset:
        if dis[colname] in list:
            continue;
        else:
            list.append(dis[colname]);
    return list;

##*********************Json Serialize (Start)****************

def date_handler(obj):
    return obj.isoformat() if hasattr(obj, 'isoformat') else obj


def decimal_default(obj):
    if isinstance(obj, decimal.Decimal):
        return float(obj)
    raise TypeError

##*********************Json Serialize (end )****************


## *************** Cup Related Dashboard (Start) **********

def cup_hh_profile_analytics(request):

    return render(request, 'blog/cup_Dashboard/hh_profile_analytics.html')

def form_Submission_Enomenator(request):
    return render(request, 'blog/cup_Dashboard/R_FormSubmission_Enumerators.html')

def waveMoney_Waiting_Time(request):
    return render(request, 'blog/cup_Dashboard/waveMoney_Waiting_Time.html')

def hh_graduation_competency(request):
    return render(request, 'blog/cup_Dashboard/hh_graduation_competency.html')

def R_SLA_Formed(request):
    return render(request, 'blog/cup_Dashboard/R_SLA_Formed.html')

def R_SLA_Formed(request):
    return render(request, 'blog/cup_Dashboard/R_SLA_Formed.html')

def health_service_seeking(request):
    return render(request, 'blog/cup_Dashboard/health_service_seeking.html')

def hh_schooling_status(request):
    query = "SELECT cast( (unnest(string_to_array(json->>\'school_age_child_status\',\' \'))) as int ) as name, to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month')  as category ,count(id) as value FROM logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null group by name,category order by name asc";
    queryTable = " SELECT (json-> 'hh_id' ) as hh_id, string_to_array(json->>'school_age_child_status',' ') as name , to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month') as category FROM public.logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null";

    # countLegend = "SELECT"
    # "distinct cast( (unnest(string_to_array(json->>'school_age_child_status',' '))) as int ) as name"
    # "FROM public.logger_instance where xform_id = 350"
    # "and (json->>'school_age_child_status') is not null order by name asc";
    jsonForChart = generateChartData('name', 'value', 'category', query)
    jsonForChartTable = generateChartDataTable(queryTable)
    return render(request, 'blog/cup_Dashboard/hh_schooling_status.html',{'jsonForChart': jsonForChart, 'jsonForChartTable': jsonForChartTable})

def hunger_experience(request):
    return render(request, 'blog/cup_Dashboard/hunger_experience.html')

def hh_access_to_neutritious_food(request):
    return render(request, 'blog/cup_Dashboard/hh_access_to_neutritious_food.html')

def hh_borrowing_sources(request):
    query = "SELECT cast( (unnest(string_to_array(json->>\'school_age_child_status\',\' \'))) as int ) as name, to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month')  as category ,count(id) as value FROM logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null group by name,category order by name asc";
    queryTable = " SELECT (json-> 'hh_id' ) as hh_id, string_to_array(json->>'school_age_child_status',' ') as name , to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month') as category FROM public.logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null";
    jsonForChart = generateChartData('name', 'value', 'category', query)
    jsonForChartTable = generateChartDataTable(queryTable)
    return render(request, 'blog/cup_Dashboard/hh_borrowing_sources.html', {'jsonForChart': jsonForChart, 'jsonForChartTable': jsonForChartTable})

def Training_Capacity_pay_off_debts_bills(request):
    query = "SELECT cast( (unnest(string_to_array(json->>\'school_age_child_status\',\' \'))) as int ) as name, to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month')  as category ,count(id) as value FROM logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null group by name,category order by name asc";
    queryTable = " SELECT (json-> 'hh_id' ) as hh_id, string_to_array(json->>'school_age_child_status',' ') as name , to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month') as category FROM public.logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null";
    jsonForChart = generateChartData('name', 'value', 'category', query)
    jsonForChartTable = generateChartDataTable(queryTable)
    return render(request, 'blog/cup_Dashboard/Training_Capacity_pay_off_debts_bills.html', {'jsonForChart': jsonForChart, 'jsonForChartTable': jsonForChartTable})

def Training_Capacity_budget_following(request):
    return render(request, 'blog/cup_Dashboard/Training_Capacity_budget_following.html')

def Planning_MF_Saving_Purposes(request):
        return render(request, 'blog/cup_Dashboard/Planning_MF_Saving_Purposes.html')

def training_conducted(request):
        return render(request, 'blog/cup_Dashboard/training_conducted.html')

def planning_MF_ends_meet(request):
    query = "SELECT cast( (unnest(string_to_array(json->>\'school_age_child_status\',\' \'))) as int ) as name, to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month')  as category ,count(id) as value FROM logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null group by name,category order by name asc";
    queryTable = " SELECT (json-> 'hh_id' ) as hh_id, string_to_array(json->>'school_age_child_status',' ') as name , to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month') as category FROM public.logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null";
    jsonForChart = generateChartData('name', 'value', 'category', query)
    jsonForChartTable = generateChartDataTable(queryTable)
    return render(request, 'blog/cup_Dashboard/planning_MF_ends_meet.html',{'jsonForChart': jsonForChart, 'jsonForChartTable': jsonForChartTable})

def income_changes(request):
    query = "SELECT cast( (unnest(string_to_array(json->>\'school_age_child_status\',\' \'))) as int ) as name, to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month')  as category ,count(id) as value FROM logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null group by name,category order by name asc";
    queryTable = " SELECT (json-> 'hh_id' ) as hh_id, string_to_array(json->>'school_age_child_status',' ') as name , to_char(to_date(json->>'visit_date', 'yyyy-mm-dd'), 'Month') as category FROM public.logger_instance where xform_id = 350 and (json->>'school_age_child_status') is not null";
    jsonForChart = generateChartData('name', 'value', 'category', query)
    jsonForChartTable = generateChartDataTable(queryTable)
    return render(request, 'blog/cup_Dashboard/income_changes.html',{'jsonForChart': jsonForChart, 'jsonForChartTable': jsonForChartTable})




    ##*************** Cup Related Dashboard (End) *********