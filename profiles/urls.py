from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('profiles/', login_required(views.ProfileListView.as_view(), login_url='login'), name='profiles'),
    path('profiles/accept', views.accept_invitation, name='accept_invite'),
    path('profiles/reject', views.reject_invitation, name='reject_invite'),
    path('myprofile/', views.my_profile, name='my_profile_view'),
    path('my-invites/', views.invites_received_view, name='my_invites_view'),
    path('to-invite/', views.invite_profiles_list_view, name='invite_profiles_view'),
    path('send-invite/', views.send_invitation, name='send-invite'),
    path('remove-friend/', views.remove_friend, name='remove-friend'),
]