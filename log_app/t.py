class TotalGasReceivedToday(APIView):
    permission_classes=(AllowAny,)
    def get_fuel_received_info(self,id):
        gas_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        if gas_info:
            gas_id = gas_info.id
        else:
            Http404
        log_details = Log.objects.all().filter(id=id).filter(fuel_id=gas_id).first() 
        if log_details:
            log_date = log_details.date
            try:
                return FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=log_date).last()
            except FuelReceived.DoesNotExist:
                return Http404
        else:
            Http404
    
    def get(self, request, id, format=None):
        today = dt.date.today()
        gas_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        if gas_info:
            print(gas_info)
            print(gas_info.id)
            gas_id = gas_info.id
        else:
            Http404
        log_details = Log.objects.all().filter(id=id).filter(fuel_id=gas_id).first() 
        if log_details:
            log_date = log_details.date
            gas_received_info = FuelReceived.objects.all().filter(fuel_id=gas_id).last()
            if gas_received_info:
                print("gas received!")
                gas_received_info.total_fuel_received_today = FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=log_date).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
                gas_received_info.fuel_name = gas_received_info.fuel.fuel_type
                gas_received_info.save()
                gas_received_info.refresh_from_db()
                fuel_received_info = FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=log_date).last()
                serializers = FuelReceivedSerializer(fuel_received_info,many=False)
                return Response(serializers.data)
            else:
                return Http404
        else:
            print("no logs")
            gas_received_info.total_fuel_received_today = FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
            gas_received_info.fuel_name = gas_received_info.fuel.fuel_type
            gas_received_info.save()
            gas_received_info.refresh_from_db()
            fuel_received_info = FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=log_date).last()
            serializers = FuelReceivedSerializer(fuel_received_info,many=False)
            return Response(serializers.data)