1.d0100630200Ff.objects.filter(meter_id=meter_id).order_by('-_00_00_01_00_00_FF')[:1]
2.InstantSeri(pk.instant_models.last()) if pk.instant_models.exists() else None
3.b01005E5B00Ff.objects.filter(meter_id=pk.meter_id).latest('-_00_00_01_00_00_FF')

class Profile(views.APIView):#28.62
#prefetch_related
    def get(self, request, format=None):
        queryset = RsmMeterMaster.objects.prefetch_related(
            Prefetch('instant_models', queryset=b01005E5B00Ff.objects.order_by('-_00_00_01_00_00_FF')),
            Prefetch('meter_models', queryset=c0100630100Ff.objects.order_by('-_00_00_01_00_00_FF')),
            Prefetch('daily_models', queryset=d0100630200Ff.objects.order_by('-_00_00_01_00_00_FF'))
        ).all()

        latest_records = []
        for pk in queryset:
            instant_serializer = InstantSeri(pk.instant_models.last()) if pk.instant_models.exists() else None
            meter_serializer = MeterloadSeri(pk.meter_models.last()) if pk.meter_models.exists() else None
            daily_serializer = DailyloadSeri(pk.daily_models.last()) if pk.daily_models.exists() else None

            latest_records.append({
                "meter_id": pk.meter_id,
                "meter_serial_number": pk.meter_serial_number,
                **(instant_serializer.data if instant_serializer else {"InstantProfile": None}),
                **(meter_serializer.data if meter_serializer else {"MeterloadProfile": None}),
                **(daily_serializer.data if daily_serializer else {"DailyloadProfile": None})
            })

        return Response(latest_records)

class Profile(views.APIView): #28.62

    def get(self, request, format=None):
        queryset = RsmMeterMaster.objects.prefetch_related(
            Prefetch('instant_models', queryset=b01005E5B00Ff.objects.order_by('-_00_00_01_00_00_FF'), to_attr='instant_records'),
            Prefetch('meter_models', queryset=c0100630100Ff.objects.order_by('-_00_00_01_00_00_FF'), to_attr='meter_records'),
            Prefetch('daily_models', queryset=d0100630200Ff.objects.order_by('-_00_00_01_00_00_FF'), to_attr='daily_records')
        ).all()

        latest_records = []
        for pk in queryset:
            ins_serializer = None
            meter_serializer = None
            daily_serializer = None

            if pk.instant_records:
                ins_record = b01005E5B00Ff.objects.filter(meter_id=pk.meter_id).latest('-_00_00_01_00_00_FF')
                ins_serializer = InstantSeri(ins_record)

            if pk.meter_records:
                meter_record = c0100630100Ff.objects.filter(meter_id=pk.meter_id).latest('-_00_00_01_00_00_FF')
                meter_serializer = MeterloadSeri(meter_record)

            if pk.daily_records:
                daily_record = d0100630200Ff.objects.filter(meter_id=pk.meter_id).latest('-_00_00_01_00_00_FF')
                daily_serializer = DailyloadSeri(daily_record)

            latest_records.append({
                "meter_id": pk.meter_id,
                "meter_serial_number": pk.meter_serial_number,
                **(ins_serializer.data if ins_serializer else {"InstantProfile": None}),
                **(meter_serializer.data if meter_serializer else {"MeterloadProfile": None}),
                **(daily_serializer.data if daily_serializer else {"DailyloadProfile": None})
            })

        return JsonResponse(latest_records,safe=False)

class Profile(views.APIView): #nearly 1.30
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]
    def get(self, request, format=None):
        queryset = RsmMeterMaster.objects.select_related().all()

        latest_records = []
        for pk in queryset:
            instant_serializer = InstantSeri(pk.instant_models.last()) if pk.instant_models.exists() else None
            meter_serializer = MeterloadSeri(pk.meter_models.last()) if pk.meter_models.exists() else None
            daily_serializer = DailyloadSeri(pk.daily_models.last()) if pk.daily_models.exists() else None

            latest_records.append({
                "meter_id": pk.meter_id,
                "meter_serial_number": pk.meter_serial_number,
                **(instant_serializer.data if instant_serializer else {"InstantProfile": None}),
                **(meter_serializer.data if meter_serializer else {"MeterloadProfile": None}),
                **(daily_serializer.data if daily_serializer else {"DailyloadProfile": None})
            })

        return JsonResponse(latest_records, safe=False)