from django.contrib import admin

# Register your models here.
from swiss_gui.models import Round,InitialPlayerList,ParticipatedPlayerList,CurrentRoundPlayerList,PooledResults,ResultsHistory

admin.site.register([Round,InitialPlayerList,ParticipatedPlayerList,CurrentRoundPlayerList,PooledResults,ResultsHistory])