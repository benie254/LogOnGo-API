class PastLogCreditCards(APIView):
    permission_classes=(AllowAny,)
    
    def get(self,request,past_date):
        try:
        # convert data from the string url
            date = dt.datetime.strptime(past_date, '%Y-%m-%d').date()

        except ValueError:
            # raise 404 when value error is thrown
            raise Http404()
            assert False

        if date == dt.date.today():
            today = dt.date.today()
            past_credit_card_logs = LogCreditCard.objects.filter(date=today)
            serializers = LogCreditCardSerializer(past_credit_card_logs,many=True)
            return Response(serializers.data)

        past_credit_card_logs = LogCreditCard.objects.filter(date=date)
        serializers = LogCreditCardSerializer(past_credit_card_logs,many=True)
        return Response(serializers.data)