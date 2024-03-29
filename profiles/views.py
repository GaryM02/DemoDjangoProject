from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile, Relationship
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.db.models import Q

# Create your views here.

@login_required(login_url='login')
def my_profile(request):
    profile = Profile.objects.get(user=request.user)
    context={'profile':profile}
    return render(request, 'profiles/myprofile.html', context)

@login_required(login_url='login')
def invites_received_view(request):
    profile = Profile.objects.get(user=request.user)
    qs = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, qs))

    is_empty = False
    if len(results) == 0:
        is_empty = True

    context = {'qs':results, 'is_empty':is_empty}



    return render(request, 'profiles/my_invites.html', context)

@login_required(login_url='login')
def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()

    return redirect('profiles')

@login_required(login_url='login')
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        receiver = Profile.objects.get(user=request.user)
        sender = Profile.objects.get(pk=pk)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('profiles')

@login_required(login_url='login')
def invite_profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles_to_invite(user)

    context = {'qs':qs}

    return render(request, 'profiles/to_invite_list.html', context)

@login_required(login_url='login')
def profiles_list_view(request):
    user = request.user
    qs = Profile.objects.get_all_profiles(user)

    context = {'qs':qs}

    return render(request, 'profiles/profile_list.html', context)

    

class ProfileListView(ListView):
    model = Profile
    template_name = 'profiles/profiles.html'
    context_object_name = 'qs'

    def get_queryset(self):

       
        query = self.request.GET.get('username')
        if query:
            users = User.objects.filter(username__icontains=query)
            qs = []
            for user in users:
                print(user)
                profile = Profile.objects.get(user=user)
                qs.append(profile)
            return qs
        else:
            qs = Profile.objects.get_all_profiles(self.request.user)
            return qs
        # qs = Profile.objects.get_all_profiles(self.request.user)
        # print(qs[0].user.username)
        # return qs
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile = Profile.objects.get(user=user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        
        qs = Relationship.objects.invitations_received(profile)
        results = list(map(lambda x: x.sender, qs))

        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)



        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        context['invites'] = results
        context['foundusers'] = None


        if len(self.get_queryset()) == 0:
            context['is_empty'] = True


        return context

@login_required(login_url='login')
def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my-profile-view')

@login_required(login_url='login')
def remove_friend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        print(rel)
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('my-profile-view')



