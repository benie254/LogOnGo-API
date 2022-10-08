class EmailCreditCardReport(APIView):
    permission_classes=(AllowAny,)
    def get_credit_card_reports(self):
        try:
            return CreditCardReport.objects.all()
        except CreditCardReport.DoesNotExist:
            return Http404

    def get(self, request, format=None):
        reports = CreditCardReport.objects.all()
        serializers = CreditCardReportSerializer(reports,many=True)
        return Response(serializers.data)

    def post(self, request,format=None):
        serializers = CreditCardReportSerializer(data=request.data)
        if serializers.is_valid():
            # serializer.is_valid(raise_exception=True)
            date=serializers.validated_data['date']
            card_name=serializers.validated_data['transaction_number']
            card_number=serializers.validated_data['customer_name']
            amount=serializers.validated_data['amount']
            amount_transferred_to_bank=serializers.validated_data['amount_transferred_to_bank']
            daily_total=serializers.validated_data['daily_total']
            cumulative_amount=serializers.validated_data['cumulative_amount']
            logged_by=serializers.validated_data['logged_by']
            username=serializers.validated_data['admin_name']
            receiver=serializers.validated_data['admin_email']
            serializers.save()
            
            sg = sendgrid.SendGridAPIClient(api_key=config('SENDGRID_API_KEY'))
            msg = "Here is your requested email report:</p> <br> <ul><li>date: " + str(date) + " </li><li>transaction no.: " + str(transaction_number) + "</li><li>customer's name: " + str(customer_name) + " </li><li>customer's phone number: " + str(customer_phone_number) + "</li><li>amount: " + str(amount) + "</li><li>amount transferred to bank: " + str(amount_transferred_to_bank) + "</li><li>daily total: " + str(daily_total) + "</li><li>cumulative amount: " + str(cumulative_amount) + "</li><li>logged by: " + str(logged_by) + "</li></ul> <br> <small> The data committee, <br> LogOnGo. <br> ©Pebo Kenya Ltd  </small>"
            message = Mail(
                from_email = Email("davinci.monalissa@gmail.com"),
                to_emails = receiver,
                subject = "Your CreditCard report",
                html_content='<p>Hello, ' + str(username) + '! <br><br>' + msg
            )
            try:
                sendgrid_client = sendgrid.SendGridAPIClient(config('SENDGRID_API_KEY'))
                response = sendgrid_client.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(e)
            status_code = status.HTTP_201_CREATED
            response = {
                'success' : 'True',
                'status code' : status_code,
                'message': 'Email report sent  successfully',
                }
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

