class GasInfo(APIView):
    def get_fuel_info(self):
        try:
            return Fuel.objects.all().filter(fuel_type='Gas').last()
        except Fuel.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        fuel_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        serializers = FuelSerializer(fuel_info,many=False)
        return Response(serializers.data)

    def put(self, request, format=None):
        fuel_info = Fuel.objects.all().filter(fuel_type='Gas').last()
        serializers = FuelSerializer(fuel_info,request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)