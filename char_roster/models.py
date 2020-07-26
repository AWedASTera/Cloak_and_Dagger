from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator
from random import randint
from django.shortcuts import redirect
# Create your models here.

class Country(models.Model):
    name = models.CharField(unique = True, max_length=100)
    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    work_bonus = models.PositiveIntegerField(default = 3)
    steal_bonus = models.PositiveIntegerField(default = 3)
    attack_bonus = models.PositiveIntegerField(default = 3)
    heal_bonus = models.PositiveIntegerField(default = 0)
    cover_bonus = models.PositiveIntegerField(default = 0)
    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(unique = True, max_length=100)
    country = models.ForeignKey(Country, on_delete = models.CASCADE)
    victory_points = models.PositiveIntegerField(default = 0)
    def __str__(self):
        return self.name


class Route(models.Model):
    origin_loc = models.ForeignKey(Location, on_delete = models.CASCADE)
    destination_loc = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='+')
    cost = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.origin_loc.name + ' - ' + self.destination_loc.name

class Agent(models.Model):
    name = models.CharField(unique = True, max_length=100)
    player = models.ForeignKey(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    work_power_origin = models.PositiveIntegerField(default = 5)
    steal_power_origin = models.PositiveIntegerField(default = 5)
    attack_power_origin = models.PositiveIntegerField(default = 5)
    work_power = models.PositiveIntegerField(default = 5)
    steal_power = models.PositiveIntegerField(default = 5)
    attack_power = models.PositiveIntegerField(default = 5)
    max_hp = models.IntegerField(default = 35)
    curr_hp = models.IntegerField(default = 35)
    curr_loc = models.ForeignKey(Location, on_delete=models.CASCADE)
    fame = models.PositiveIntegerField(default=0)
    famous = models.BooleanField(default = False)
    money = models.PositiveIntegerField(default=0)
    work_stat = models.PositiveIntegerField(default = 0)
    steal_stat = models.PositiveIntegerField(default = 0)
    attack_stat = models.PositiveIntegerField(default = 0)
    heal_stat = models.PositiveIntegerField(default = 0)
    cover_stat = models.PositiveIntegerField(default = 0)
    spended_money = models.PositiveIntegerField(default = 0)
    
    def __str__(self):
        return self.name + ', ' + self.team.name

    def get_absolute_url(self):
        return reverse('agent-detail', kwargs={'pk': self.pk})
    
    def save(self):
        if (self.curr_hp > self.max_hp):
            return redirect('/')
        if self.fame>=10 and self.famous==False:
            self.famous=True
        self.work_power = self.work_power_origin + self.work_stat // 30
        self.attack_power = self.attack_power_origin + self.attack_stat // 30
        self.steal_power = self.steal_power_origin + self.steal_stat // 30
        self.max_hp = 35 + self.heal_stat // 20
        super().save()

    
