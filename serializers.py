from rest_framework.response import Response

from .models import *
from rest_framework import serializers

class RsmMeterMasterSeri(serializers.ModelSerializer):  # 0
    class Meta:
        model = RsmMeterMaster
        fields = '__all__'

class a00005E5B0AFfSeri(serializers.ModelSerializer):  # 1
    plate = RsmMeterMasterSeri(many=True, read_only=True)

    class Meta:
        model = a00005E5B0AFf
        fields = '__all__'

class b01005E5B00FfSeri(serializers.ModelSerializer):  # 2
    instant = a00005E5B0AFfSeri(many=True, read_only=True)
    class Meta:
        model = b01005E5B00Ff
        fields = '__all__'

class c0100630100FfSeri(serializers.ModelSerializer):  # 3
    block = b01005E5B00FfSeri(many=True, read_only=True)

    class Meta:
        model = c0100630100Ff
        fields = '__all__'

class d0100630200FfSeri(serializers.ModelSerializer):  # 4
    daily = c0100630100FfSeri(many=True, read_only=True)

    class Meta:
        model = d0100630200Ff
        fields = '__all__'

class Insseri (serializers.ModelSerializer):
    class Meta:
        model = b01005E5B00Ff
        fields = ['number_00_00_01_00_00_ff','meter_id']

class NPlateseri (serializers.ModelSerializer):
    Analysis = Insseri(many=True, read_only=True)

    class Meta:
        model =  a00005E5B0AFf
        fields = ['meter_id', 'Analysis']

class DataAnalysisSeri(serializers.ModelSerializer):
    class Meta:
        model = a00005E5B0AFf
        fields = ['meter_id']

class InstantSeri(serializers.ModelSerializer):
    class Meta:
        model = b01005E5B00Ff
        fields = ['number_00_00_01_00_00_ff']

class BlockloadSeri(serializers.ModelSerializer):
    class Meta:
        model = c0100630100Ff
        fields = ['number_00_00_01_00_00_ff']

    def validate(self, args):
        number = args.get('number_00_00_01_00_00_ff', None)
        tstamp2 = c0100630100Ff.objects.filter(number_00_00_01_00_00_ff=number).latest('updated_timestamp')
        return Response({'BLOCK LOAD PROFILE(BLP)': tstamp2})

class DailyloadSeri(serializers.ModelSerializer):
    class Meta:
        model = d0100630200Ff
        fields = ['number_00_00_01_00_00_ff']

        def validate(self, args):
            number = args.get('number_00_00_01_00_00_ff', None)
            tstamp3 = d0100630200Ff.objects.filter(number_00_00_01_00_00_ff=number).latest('updated_timestamp')
            return Response({'DAILY LOAD PROFILE(DLP)': tstamp3})

class a00005E5B0AFfSerializer(serializers.ModelSerializer):  # 1
    class Meta:
        model = a00005E5B0AFf
        fields = ['meter_id']

class b01005E5B00FfSerializer(serializers.ModelSerializer):  # 2
    data = a00005E5B0AFfSeri(read_only=True)

    class Meta:
        model = b01005E5B00Ff
        fields = ['meter_id','number_00_00_01_00_00_ff','data']