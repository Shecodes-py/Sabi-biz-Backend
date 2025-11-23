from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum

# Create your views here.

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only return transactions belonging to the currently logged-in user
        return Transaction.objects.filter(user=self.request.user).order_by('-date')
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        qs = self.get_queryset()
        total_sales = qs.filter(type='SALE').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expenses = qs.filter(type='EXPENSE').aggregate(Sum('amount'))['amount__sum'] or 0
        net_profit = total_sales - total_expenses

        return Response({
            "total_sales": total_sales,
            "total_expenses": total_expenses,
            "net_profit": net_profit,
            "recent_transactions": TransactionSerializer(qs[:5], many=True).data
        })