class GasSummaryToday(APIView):
    permission_classes=(AllowAny,)
    def get_today_fuel_logs(self):
        today = dt.date.today()
        try:
            gas_info = Fuel.objects.all().filter(fuel_type='Gas').first()
            gas_id = gas_info.id
            return Fuel.objects.all().filter(fuel_id=gas_id).first()
        except Log.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        today = dt.date.today()
        yesterday = today - dt.timedelta(days=1)
        pump_one = Pump.objects.all().filter(pump_name='Pump One').first()
        pump_two = Pump.objects.all().filter(pump_name='Pump Two').first()
        pump_three = Pump.objects.all().filter(pump_name='Pump Three').first()
        pump_four = Pump.objects.all().filter(pump_name='Pump Four').first()
        gas_info = Fuel.objects.all().filter(fuel_type='Gas').first()
        today_gas_info = Fuel.objects.all().filter(fuel_type='Gas').filter(date=today).last()
        yesterday_gas_info = Fuel.objects.all().filter(fuel_type='Gas').filter(date=yesterday).last()
        if gas_info:
            gas_id = gas_info.id 
        else:
            Http404

        if pump_one:
            pump_one_id = pump_one.id
        else:
            Http404
        if pump_two:
            pump_two_id = pump_two.id
        else:
            Http404
        if pump_three:
            pump_three_id = pump_three.id
        else:
            Http404
        if pump_four:
            pump_four_id = pump_four.id
        else:
            Http404
        today_fuel_log = Log.objects.all().filter(date=today).filter(fuel_id=gas_id).filter(pump_id=pump_one_id).first()
        today_log_two = Log.objects.all().filter(date=today).filter(fuel_id=gas_id).filter(pump_id=pump_two_id).first()
        today_log_three = Log.objects.all().filter(date=today).filter(fuel_id=gas_id).filter(pump_id=pump_three_id).first()
        today_log_four = Log.objects.all().filter(date=today).filter(fuel_id=gas_id).filter(pump_id=pump_four_id).first()
        gas_received = FuelReceived.objects.all().filter(fuel_id=gas_id).filter(date_received=today).aggregate(TOTAL = Sum('litres_received'))['TOTAL']
        if today_fuel_log and today_log_two and today_log_three and today_log_four and gas_info:
            gas_id = gas_info.id
            gas_received = FuelReceived.objects.all().filter(date_received=today).filter(fuel_id=gas_id).last()
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold
            total_three = today_log_three.total_litres_sold 
            total_four = today_log_four.total_litres_sold 
            gas_info.total_litres_sold_today = (total_one) + (total_two) + (total_three) + (total_four)
            gas_info.save()
            gas_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today
            amount_three = today_log_three.amount_earned_today 
            amount_four = today_log_four.amount_earned_today 
            gas_info.amount_earned_today = (amount_one) + (amount_two) + (amount_three) + (amount_four)
            gas_info.save()
            gas_info.refresh_from_db()
            if yesterday_gas_info and gas_info.total_litres_sold_today:
                gas_info.balance_yesterday = yesterday_gas_info.balance 
                gas_info.save()
                gas_info.refresh_from_db()
                bal_yesterday = gas_info.balance_yesterday
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.balance_yesterday and gas_info.total_litres_sold_today:
                bal_yesterday = gas_info.balance_yesterday
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.total_litres_sold_today:
                init = gas_info.initial_litres_in_tank 
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (init) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                    
                if gas_info.balance and gas_received.litres_received:
                    gas_received = gas_received.litres_received
                    bal = gas_info.balance
                    gas_info.updated_balance = (bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
                    updated_bal = gas_info.updated_balance 
                elif updated_bal and gas_received:
                    gas_info.updated_balance = (updated_bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()

        elif today_fuel_log and today_log_two and today_log_three and gas_info:
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold 
            total_three = today_log_three.total_litres_sold 
            gas_info.total_litres_sold_today = (total_one) + (total_two) + (total_three)
            gas_info.save()
            gas_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today 
            amount_three = today_log_three.amount_earned_today 
            gas_info.amount_earned_today = (amount_one) + (amount_two) + (amount_three)
            gas_info.save()
            gas_info.refresh_from_db()
            if yesterday_gas_info and gas_info.total_litres_sold_today:
                gas_info.balance_yesterday = yesterday_gas_info.balance 
                gas_info.save()
                gas_info.refresh_from_db()
                bal_yesterday = gas_info.balance_yesterday
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.balance_yesterday and gas_info.total_litres_sold_today:
                bal_yesterday = gas_info.balance_yesterday
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.total_litres_sold_today:
                init = gas_info.initial_litres_in_tank 
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (init) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance
                if bal and gas_received:
                    gas_info.updated_balance = (bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
                    updated_bal = gas_info.updated_balance 
                elif updated_bal and gas_received:
                    gas_info.updated_balance = (updated_bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
        elif today_fuel_log and today_log_two and gas_info:
            total_one = today_fuel_log.total_litres_sold 
            total_two = today_log_two.total_litres_sold 
            gas_info.total_litres_sold_today = (total_one) + (total_two)
            gas_info.save()
            gas_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            amount_two = today_log_two.amount_earned_today 
            gas_info.amount_earned_today = (amount_one) + (amount_two)
            gas_info.save()
            gas_info.refresh_from_db()
            if yesterday_gas_info and gas_info.total_litres_sold_today:
                gas_info.balance_yesterday = yesterday_gas_info.balance 
                gas_info.save()
                gas_info.refresh_from_db()
                bal_yesterday = gas_info.balance_yesterday
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.balance_yesterday and gas_info.total_litres_sold_today:
                bal_yesterday = gas_info.balance_yesterday
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.total_litres_sold_today:
                init = gas_info.initial_litres_in_tank 
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (init) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance
                if bal and gas_received:
                    gas_info.updated_balance = (bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
                    updated_bal = gas_info.updated_balance 
                elif updated_bal and gas_received:
                    gas_info.updated_balance = (updated_bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
        elif today_fuel_log and gas_info:
            total_one = today_fuel_log.total_litres_sold 
            print("total one:",total_one)
            gas_info.total_litres_sold_today = total_one
            gas_info.save()
            gas_info.refresh_from_db()
            amount_one = today_fuel_log.amount_earned_today 
            gas_info.amount_earned_today = amount_one
            gas_info.save()
            gas_info.refresh_from_db()
            if yesterday_gas_info and gas_info.total_litres_sold_today:
                gas_info.balance_yesterday = yesterday_gas_info.balance 
                gas_info.save()
                gas_info.refresh_from_db()
                bal_yesterday = gas_info.balance_yesterday
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.balance_yesterday and gas_info.total_litres_sold_today:
                bal_yesterday = gas_info.balance_yesterday
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (bal_yesterday) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance 
            elif gas_info.total_litres_sold_today:
                init = gas_info.initial_litres_in_tank 
                total_sold = gas_info.total_litres_sold_today
                gas_info.balance = (init) - (total_sold)
                gas_info.save()
                gas_info.refresh_from_db()
                bal = gas_info.balance
                if bal and gas_received:
                    gas_info.updated_balance = (bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
                    updated_bal = gas_info.updated_balance 
                elif updated_bal and gas_received:
                    gas_info.updated_balance = (updated_bal) + (gas_received)
                    gas_info.save()
                    gas_info.refresh_from_db()
        serializers = FuelSerializer(gas_info,many=False)
        return Response(serializers.data)

