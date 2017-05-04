from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', views.post_detail, name='post_detail'),
    url(r'^post/new/$', views.post_new, name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/createFile/$', views.post_createFile, name='post_createFile'),
    url(r'^post/fileInfo/$',views.post_showFileInfo, name="post_showFileInfo"),
    url(r'^post/info/(?P<pk>\d+)/$', views.post_filedetail, name='post_filedetail'),
    url(r'^post/info/(?P<pk>\d+)/edit/$', views.post_editfileinfo, name='post_editfileinfo'),
    url(r'^post/fileupload/$', views.simple_upload, name='simple_upload'),
    url(r'^post/modelform/$', views.model_form_upload, name="model_form_upload"),
    url(r'^create/$', views.create , name = "create"),
    url(r'^blog/report/$', views.makechart , name="report"),
    url(r'^blog/cupReport/$', views.cupReportChart, name="cupReport"),

## ************ Cup Dash Board *********************

    url(r'^blog/cup_Dashboard/hh_profile_analytics/$',views.cup_hh_profile_analytics,name='cup_hh_profile'),
    url(r'^blog/cup_Dashboard/form_Submission_Enomenator/$',views.form_Submission_Enomenator,name='form_Submission_Enomenator'),
    url(r'^blog/cup_Dashboard/waveMoney_Waiting_Time/$', views.waveMoney_Waiting_Time,name='waveMoney_Waiting_Time'),
    url(r'^blog/cup_Dashboard/hh_graduation_competency/$', views.hh_graduation_competency, name='hh_graduation_competency'),
    url(r'^blog/cup_Dashboard/R_SLA_Formed/$', views.R_SLA_Formed,name='R_SLA_Formed'),
    url(r'^blog/cup_Dashboard/health_service_seeking/$', views.health_service_seeking, name='health_service_seeking'),
    url(r'^blog/cup_Dashboard/hh_schooling_status/$', views.hh_schooling_status, name='hh_schooling_status'),
    url(r'^blog/cup_Dashboard/hunger_experience/$', views.hunger_experience, name='hunger_experience'),
    url(r'^blog/cup_Dashboard/hh_access_to_neutritious_food/$', views.hh_access_to_neutritious_food,name='hh_access_to_neutritious_food'),
    url(r'^blog/cup_Dashboard/hh_borrowing_sources/$', views.hh_borrowing_sources,name='hh_borrowing_sources'),
    url(r'^blog/cup_Dashboard/Training_Capacity_pay_off_debts_bills/$', views.Training_Capacity_pay_off_debts_bills, name='Training_Capacity_pay_off_debts_bills'),
    url(r'^blog/cup_Dashboard/Training_Capacity_budget_following/$', views.Training_Capacity_budget_following,name='Training_Capacity_budget_following'),
    url(r'^blog/cup_Dashboard/Planning_MF_Saving_Purposes/$', views.Planning_MF_Saving_Purposes,name='Planning_MF_Saving_Purposes'),
    url(r'^blog/cup_Dashboard/training_conducted/$', views.training_conducted,name='training_conducted'),
    url(r'^blog/cup_Dashboard/planning_MF_ends_meet/$', views.planning_MF_ends_meet, name='planning_MF_ends_meet'),
    url(r'^blog/cup_Dashboard/income_changes/$', views.income_changes, name='income_changes'),



    ## ***************** End ******************************

]
