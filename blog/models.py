from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
        default=timezone.now)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title


class File(models.Model):
    kobocat_domain = models.CharField(max_length=200, blank='true')
    koboform_domain = models.CharField(max_length=200, blank='true')
    enketo_server_domain = models.CharField(max_length=200, blank='true')
    enketo_web_domain = models.CharField(max_length=200, blank='true')


    kobocat_port = models.CharField(max_length=200, blank='true');
    koboform_port = models.CharField(max_length=200, blank='true');
    enketo_server_port = models.CharField(max_length=200, blank='true' );
    enketo_web_port = models.CharField(max_length=200, blank='true' );


    src_directory = models.CharField(max_length=200, blank='true')

    kobocat_socket = models.CharField(max_length=200, blank='true');
    koboform_socket = models.CharField(max_length=200, blank='true');
    socket_status = models.CharField(max_length=200 , blank='true');

    virtualenv = models.CharField(max_length=200, blank='true')

    db_database_name = models.CharField(max_length=200, blank='true')
    db_user = models.CharField(max_length=200, blank='true')
    db_password = models.CharField(max_length=200, blank='true')
    db_server_ip = models.CharField(max_length=200, blank='true')
    db_port = models.CharField(max_length=200, blank='true')



class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

class CupReport(models.Model):
    name = models.CharField(max_length=250, blank=True);
    category = models.CharField(max_length=250, blank = True);
    value = models.DecimalField(decimal_places= 3, max_digits=20);




