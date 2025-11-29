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

    # Total expenses and profit
    total_expenses = Expense.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    total_sales = Sales.objects.filter(user=user).aggregate(total=Sum('amount'))['total'] or 0
    profit = total_sales - total_expenses

    # Best selling product
    best_selling = (
        Sales.objects.filter(user=user)
        .values('product_name')
        .annotate(total_qty=Sum('quantity'))
        .order_by('-total_qty')
        .first()
    )
    best_selling_name = best_selling['product_name'] if best_selling else None

    # Recent activity
    recent_sales = list(Sales.objects.filter(user=user).order_by('-date')[:5].values(
        'product_name', 'quantity', 'amount', 'date'
    ))
    recent_expenses = list(Expense.objects.filter(user=user).order_by('-date')[:5].values(
        'description', 'amount', 'date'
    ))

    recent_activity = {
        'sales': recent_sales,
        'expenses': recent_expenses
    }

    return JsonResponse({
        "username": user.username,
        'total_sales': total_sales,
        'total_expenses': total_expenses,
        'profit': profit,
        'best_selling_product': best_selling_name,
        'recent_activity': recent_activity
    })

@csrf_exempt
@login_required
def add_sale(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            product_name = data.get("product_name")
            quantity = data.get("quantity")
            amount = data.get("amount")

            if not all([product_name, quantity, amount]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            sale = Sales.objects.create(
                user=request.user,
                product_name=product_name,
                quantity=quantity,
                amount=amount
            )
            sale.save()

            return JsonResponse({"message": "Sale added successfully"}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "POST required"}, status=405)

@csrf_exempt
@login_required
def add_expense(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            name = data.get("name")
            description = data.get("description")
            amount = data.get("amount")

            if not all([name, description, amount]):
                return JsonResponse({"error": "All fields are required"}, status=400)

            expense = Expense.objects.create(
                user=request.user,
                name=name,
                description=description,
                amount=amount
            )
            expense.save()

            return JsonResponse({"message": "Expense added successfully"}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "POST required"}, status=405)

@csrf_exempt
def logout_view(request):
    logout(request)
    return redirect('home')