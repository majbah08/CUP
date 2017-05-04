from django import forms
from .models import Post
from .models import File
from .models import Document



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = {'title', 'text', }


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = {'kobocat_domain', 'koboform_domain', 'enketo_server_domain', 'enketo_web_domain',
                  'kobocat_port', 'koboform_port', 'enketo_server_port', 'enketo_web_port',
                  'src_directory',
                  'kobocat_socket', 'koboform_socket','socket_status',
                  'virtualenv',
                  'db_database_name','db_user','db_password','db_server_ip','db_port'}


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )