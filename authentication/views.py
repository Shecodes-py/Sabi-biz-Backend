from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User 
import json
from django.db.models import Sum
from .models import Sales, Expense
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

@csrf_exempt
def login_view(request):
    if request.method == "POST":
        try: 
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return JsonResponse({"error": "Username and password are required"}, status=400)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)  # creates session
                return JsonResponse({"message": "Login successful", "user": user.username})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
    return JsonResponse({"error": "POST required"}, status=405)

# register
@csrf_exempt
def register(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            email = data.get("email")
            password = data.get("password")

            if not all({username, email, password}):
                return JsonResponse({"error": "All fields are required"}, status=400)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"error": "Email already exists"}, status=400)

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)
            
            # Create user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            return JsonResponse({"message": "Registration successful"}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        
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

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('home')