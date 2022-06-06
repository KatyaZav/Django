from rest_framework.serializers import ModelSerializer
from .models import Achive, Core, Boost

class CoreSerializer(ModelSerializer):
    class Meta:
        model = Core
        fields = ['coins', 'click_power', 'auto_click_power', 'achiveCount']

class BoostSerializer(ModelSerializer): 
    class Meta: 
        model = Boost 
        fields = '__all__'

class AchiveSerializer(ModelSerializer): 
    class Meta: 
        model = Achive 
        fields = '__all__'