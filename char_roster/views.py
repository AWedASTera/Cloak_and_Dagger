from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .models import Agent, Team, Route, Location
from .forms import AgentKillForm, AgentTravelForm
from random import randint
from django.contrib.auth.decorators import login_required
from django.db import transaction
from users.models import Profile
from django.core import serializers

@login_required
def attack(request, **kwargs):
    attacker = get_object_or_404(Agent, id=kwargs.get('id'))
    if attacker.player == request.user:
        if request.method == 'POST':
            form = AgentKillForm(request.POST)
            if form.is_valid():
                victim = form.cleaned_data['victim']
                if (victim.curr_hp != 0 and attacker.curr_hp != 0):
                    try:
                        with transaction.atomic():
                            power = randint(1,6) + attacker.attack_power + attacker.curr_loc.attack_bonus - (attacker.fame // 3)
                            if attacker.curr_loc.country == attacker.team.country:
                                power += 2
                            if power < victim.curr_hp:
                                victim.curr_hp -= power
                                attacker.attack_stat += power
                                attacker.fame += 2
                                messages.success(request, f'Injure success!')
                            else:
                                attacker.money += victim.money
                                attacker.attack_stat += victim.curr_hp
                                victim.money = 0
                                victim.curr_hp = 0
                                attacker.fame += 2
                                messages.success(request, f'Assasination success!')
                            attacker.save()
                            victim.save()
                    except:
                        messages.warning(request, f'Sorry, something went wrong')
                else:
                    messages.warning(request, f'exception target!')
                return redirect('agent-detail', attacker.id)
        else:
            form = AgentKillForm()
            form.fields['victim'].queryset = Agent.objects.filter(curr_loc = Agent.objects.get(id = kwargs['id']).curr_loc).exclude(team = Agent.objects.get(id = kwargs['id']).team)
        context = {
            'form': form
        }
        return render(request, 'char_roster/agent_attack.html', context)
    else:
        messages.warning(request, f'You have no power here xD')
        return redirect('/')

@login_required
def steal(request, **kwargs):
    attacker = get_object_or_404(Agent, id=kwargs.get('id'))
    if attacker.player == request.user:
        if request.method == 'POST':
            form = AgentKillForm(request.POST)
            if form.is_valid():
                victim = form.cleaned_data['victim']
                if (victim.curr_hp != 0 and attacker.curr_hp != 0):
                    try:
                        with transaction.atomic():
                            power = randint(1,6) + attacker.steal_power + attacker.curr_loc.steal_bonus - (attacker.fame // 3)
                            if attacker.curr_loc.country == attacker.team.country:
                                power += 2
                            if power < victim.money:
                                victim.money -= power
                                attacker.money +=power
                                attacker.steal_stat += power
                            else:
                                attacker.money += victim.money
                                attacker.steal_stat += victim.money
                                victim.money = 0
                            attacker.fame += 1
                            messages.success(request, f'Success robbery!')
                            attacker.save()
                            victim.save()
                    except:
                        messages.warning(request, f'Sorry, something went wrong')
                else:
                    messages.warning(request, f'exception target!')
                return redirect('agent-detail', attacker.id)
        else:
            form = AgentKillForm()
            form.fields['victim'].queryset = Agent.objects.filter(curr_loc = Agent.objects.get(id = kwargs['id']).curr_loc).exclude(team = Agent.objects.get(id = kwargs['id']).team)
        context = {
            'form': form
        }
        return render(request, 'char_roster/agent_attack.html', context)
    else:
        messages.warning(request, f'You have no power here xD')
        return redirect('/')

@login_required
def work(request, **kwargs):
    attacker = get_object_or_404(Agent, id=kwargs.get('id'))
    if attacker.player == request.user:
        if attacker.curr_hp != 0:
            try:
                with transaction.atomic():
                    power = randint(1,6) + attacker.work_power + attacker.curr_loc.work_bonus + (attacker.fame // 4)
                    if attacker.curr_loc.country == attacker.team.country:
                            power += 2
                    attacker.money += power
                    attacker.work_stat += power
                    messages.success(request, f'Success working!')
                    attacker.save()
            except:
                messages.warning(request, f'Sorry, something went wrong')
        else:
            messages.warning(request, f'Nobody can work with that health')
        return redirect('agent-detail', attacker.id)
    else:
        messages.warning(request, f'You have no power here xD')
        return redirect('/')

@login_required
def cover(request, **kwargs):
    attacker = get_object_or_404(Agent, id=kwargs.get('id'))
    if attacker.player == request.user:
        if (attacker.fame > 0 and attacker.curr_hp > 0):
            try:
                with transaction.atomic():
                    power = 1 + attacker.curr_loc.cover_bonus
                    if attacker.curr_loc.country == attacker.team.country:
                                power += 1
                    if power < attacker.fame:
                        attacker.fame -= power
                        attacker.cover_stat += power
                    else:
                        attacker.cover_stat += attacker.fame
                        attacker.fame = 0
                    messages.success(request, f'Success covering!')
                    attacker.save()
            except:
                messages.warning(request, f'Sorry, something went wrong')
        else:
            messages.warning(request, f'Nobody can cover with that health or fame')
        return redirect('agent-detail', attacker.id)
    else:
        messages.warning(request, f'You have no power here xD')
        return redirect('/')

@login_required
def heal(request, **kwargs):
    attacker = get_object_or_404(Agent, id=kwargs.get('id'))
    if attacker.player == request.user:
        try:
            with transaction.atomic():
                power = attacker.curr_loc.heal_bonus
                if attacker.curr_loc.country == attacker.team.country:
                    power += 5
                if attacker.money >= 10:
                    power += randint(1,10)
                    attacker.money -= 10
                    attacker.spended_money += 10
                if power + attacker.curr_hp < attacker.max_hp:
                    attacker.curr_hp += power
                    attacker.heal_stat += power
                else:
                    attacker.heal_stat += attacker.max_hp - attacker.curr_hp
                    attacker.curr_hp = attacker.max_hp
                messages.success(request, f'Success healing!')
                attacker.save()
        except:
            messages.warning(request, f'Sorry, something went wrong')
        return redirect('agent-detail', attacker.id)
    else:
        messages.warning(request, f'You have no power here xD')
        return redirect('/')

@login_required
def buy_point(request, **kwargs):
    attacker = get_object_or_404(Agent, id=kwargs.get('id'))
    if attacker.player == request.user:
        if (attacker.curr_hp != 0 and attacker.money >= 40):
            try:
                with transaction.atomic():
                    profile1 = get_object_or_404(Profile, id = attacker.player.profile.id)
                    team1 = get_object_or_404(Team, id = attacker.team.id)
                    attacker.money -= 40
                    profile1.score += 1
                    team1.victory_points += 1
                    messages.success(request, f'Success buying!')
                    profile1.save()
                    team1.save()
                    attacker.save()
            except:
                messages.warning(request, f'Sorry, something went wrong')
        else:
            messages.warning(request, f'Nobody can buy with that health or you have not enough money')
        return redirect('agent-detail', attacker.id)
    else:
        messages.warning(request, f'You have no power here xD')
        return redirect('/')

@login_required
def travel(request, **kwargs):
    agent = get_object_or_404(Agent, id=kwargs.get('id'))
    if agent.player == request.user:
        if request.method == 'POST':
            form = AgentTravelForm(request.POST)
            if form.is_valid():
                route = form.cleaned_data['route']
                if (agent.team.country == route.origin_loc.country and agent.team.country == route.destination_loc.country):
                    try:
                        with transaction.atomic():
                            agent.curr_loc = route.destination_loc
                            agent.save()
                    except:
                        messages.warning(request, f'Sorry, something went wrong')
                else:
                    if ((agent.money >= route.cost) or (agent.fame > 10 and agent.money >= route.cost // 2)):
                        try:
                            with transaction.atomic():
                                cost = route.cost
                                if (agent.fame > 10):
                                    cost = route.cost // 2
                                agent.money -= cost
                                agent.spended_money += cost
                                agent.curr_loc = route.destination_loc
                                agent.save()
                        except:
                            messages.warning(request, f'Sorry, something went wrong')
                    else:
                        messages.warning(request, f'Not enough money!')
                return redirect('agent-detail', agent.id)
        else:
            form = AgentTravelForm()
            form.fields['route'].queryset = Route.objects.filter(origin_loc = agent.curr_loc)
        context = {
            'form': form
        }
        return render(request, 'char_roster/agent_travel.html', context)
    else:
        messages.warning(request, f'You have no power here xD')
        return redirect('/')


def statistics(request):
    context = {
        'title': 'Statistics',
        'top_fame': Agent.objects.all().order_by('-fame')[:5],
        'top_team': Team.objects.all().order_by('-victory_points')[:5],
        'top_user': Profile.objects.all().order_by('-score')[:5]
    }
    return render(request, 'char_roster/statistics.html', context)

@login_required
def json_export(request):
    if request.user.is_staff:
        JSONSerializer = serializers.get_serializer("json")
        json_serializer = JSONSerializer()
        with open("file.json", "w") as out:
            json_serializer.serialize(Agent.objects.all(), stream=out)
        messages.success(request, f'JSON export success')
    else:
        messages.warning(request, f'You have tried to open something that you have not deserve xD')
    return redirect('/')

@login_required
def json_import(request):
    if request.user.is_staff:
        with open("file.json", "r") as in_stream :
            for agent in serializers.deserialize("json", in_stream):
                agent.save()
        messages.success(request, f'JSON import success')
    else:
        messages.warning(request, f'You have tried to open something that you have not deserve xD')
    return redirect('/')

class AgentListView(ListView):
    model = Agent
    template_name = 'char_roster/home.html' #<app>/<model>_<viewtype>.html
    context_object_name = 'agents'
    ordering = ['-id']

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Agent.objects.filter(famous = True)[:5]
        return Agent.objects.filter(player=self.request.user).order_by('-fame')
    
    

class UserAgentListView(ListView):
    model = Agent
    template_name = 'char_roster/user_agents.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'agents'

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        if user == self.request.user:
            return Agent.objects.filter(player=user).order_by('-fame')
        return Agent.objects.filter(player=user, famous=True).order_by('-fame')

class TeamAgentListView(ListView):
    model = Agent
    template_name = 'char_roster/team_agents.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'agents'

    def get_queryset(self):
        team = get_object_or_404(Team, name=self.kwargs.get('name'))
        return Agent.objects.filter(team=team, famous = True).order_by('-fame')

class AgentDetailView(DetailView):
    model = Agent

    def get_context_data(self, **kwargs):
        context = super(AgentDetailView, self).get_context_data(**kwargs)
        context['agents'] = Agent.objects.filter(curr_loc = self.object.curr_loc)
        return context
    
class AgentCreateView(LoginRequiredMixin, CreateView):
    model = Agent
    fields = ['name', 'team', 'curr_loc']

    def form_valid(self, form):
        form.instance.player = self.request.user
        return super().form_valid(form)
    
class AgentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Agent
    fields = ['name']

    def form_valid(self, form):
        form.instance.player = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        agent = self.get_object()
        if self.request.user == agent.player:
            return True
        return False


class AgentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Agent
    success_url = '/'

    def test_func(self):
        agent = self.get_object()
        if self.request.user == agent.player:
            return True
        return False

