#select_related:
#models
class RsmMeterMaster(models.Model):
    meter_id = models.CharField(db_column='METER_ID', primary_key=True, max_length=45)
    meter_serial_number = models.CharField(db_column='METER_SERIAL_NUMBER', max_length=45, blank=True, null=True)

class InstantModel(models.Model):
    auto_index = models.AutoField(db_column='AUTO_INDEX', primary_key=True)
    meter_id = models.ForeignKey(RsmMeterMaster,db_column='METER_ID', on_delete=models.CASCADE, related_name='instant_models')
    _00_00_01_00_00_FF = models.CharField(db_column='00_00_01_00_00_FF', max_length=100, blank=True, null=True)

class MeterloadModel(models.Model):
    auto_index = models.AutoField(db_column='AUTO_INDEX', primary_key=True)
    meter_id = models.ForeignKey(RsmMeterMaster,db_column='METER_ID', on_delete=models.CASCADE, related_name='meter_models')
    _00_00_01_00_00_FF = models.CharField(db_column='00_00_01_00_00_FF', max_length=100, blank=True, null=True)

class DailyloadModel(models.Model):
    auto_index = models.AutoField(db_column='AUTO_INDEX', primary_key=True)
    meter_id = models.ForeignKey(RsmMeterMaster,db_column='METER_ID', on_delete=models.CASCADE, related_name='daily_models')
    _00_00_01_00_00_FF = models.CharField(db_column='00_00_01_00_00_FF', max_length=100, blank=True, null=True)

#serializers
class InstantSeri(serializers.ModelSerializer):
    InstantProfile = serializers.CharField(source='_00_00_01_00_00_FF')
    class Meta:
        model = b01005E5B00Ff
        fields = ['InstantProfile',]

class MeterloadSeri(serializers.ModelSerializer):
    MeterloadProfile = serializers.CharField(source='_00_00_01_00_00_FF')

    class Meta:
        model = c0100630100Ff
        fields = ['MeterloadProfile',]

class DailyloadSeri(serializers.ModelSerializer):
    DailyloadProfile = serializers.CharField(source='_00_00_01_00_00_FF')
    class Meta:
        model = d0100630200Ff
        fields = ['DailyloadProfile',]
class ProfileSerializer(serializers.ModelSerializer):
    instant_models = InstantSeri(many=True)
    meter_models = MeterloadSeri(many=True)
    daily_models = DailyloadSeri(many=True)

    class Meta:
        model = RsmMeterMaster
        fields = ['meter_id', 'meter_serial_number', 'instant_models', 'meter_models', 'daily_models']
        queryset = RsmMeterMaster.objects.select_related('instant_models', 'meter_models', 'daily_models')

#views:
class ProfileList(generics.ListAPIView):
    queryset = RsmMeterMaster.objects.select_related().all()
    serializer_class = ProfileSerializer
