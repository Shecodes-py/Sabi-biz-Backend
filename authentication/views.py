from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
from django.views.decorators.csrf import csrf_exempt
import json
from django.db.models import Sum
from .models import Sales, Expense, Product


# Create your views here.

@csrf_exempt  
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # creates session
            return JsonResponse({"message": "Login successful", "user": user.username})
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=400)

    return JsonResponse({"error": "POST required"}, status=405)

# register
def register(request):
    if request.method == "POST":
        username = user.get("username")
        email = user.get("email")
        password = user.get("password")
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        return JsonResponse({"message": "Registration successful"})
    return JsonResponse({"error": "POST required"}, status=405)

# dashboard

@login_required
def dashboard(request):
    user = request.user

    total_expenses = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    total_sales = Sales.objects.filter(user=user).aggregate(total=Sum('total_amount'))['total'] or 0
    profit = total_sales - total_expenses

    # Best selling product
    best_selling = (
        Sales.objects.filter(user=user)
        .values('product__name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')
        .first()
    )
    best_selling_name = best_selling['product__name'] if best_selling else None

    # Recent activity
    recent_sales = list(Sales.objects.filter(user=user).order_by('-date_created')[:5].values(
        'product__name', 'quantity', 'total_amount', 'date_created'
    ))
    recent_expenses = list(Expense.objects.filter(user=user).order_by('-date_created')[:5].values(
        'description', 'amount', 'date_created'
    ))

    recent_activity = {
        'sales': recent_sales,
        'expenses': recent_expenses
    }

    return JsonResponse({
        'total_expenses': total_expenses,
        'profit': profit,
        'best_selling_product': best_selling_name,
        'recent_activity': recent_activity
    })
