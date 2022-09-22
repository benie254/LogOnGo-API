class GasReceivedTodayInfo(APIView):
    permission_classes=(AllowAny,)
    def get_fuel_received_info(self):
        gas_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        if gas_info:
            print(gas_info)
            print(gas_info.id)
            gas_id = gas_info.id
        else:
            Http404
        today = dt.date.today()
        try:
            return FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=today)
        except FuelReceived.DoesNotExist:
            return Http404
    
    def get(self, request, format=None):
        today = dt.date.today()
        gas_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        if gas_info:
            print(gas_info)
            print(gas_info.id)
            gas_id = gas_info.id
        else:
            Http404
        gas_received_info = FuelReceived.objects.all().filter(fuel_id=gas_id).last()
        if gas_received_info:
            gas_received_info.total_fuel_received_today = FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
            gas_received_info.fuel_name = gas_received_info.fuel.fuel_type
            gas_received_info.save()
            gas_received_info.refresh_from_db()
        fuel_received_info = FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=today)
        serializers = FuelReceivedSerializer(fuel_received_info,many=True)
        return Response(serializers.data)