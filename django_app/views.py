from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Sum
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import *
from django_app.make_token import get_tokens_for_user
from django_app.serializers import LoginSerializer


class LoginUser ( APIView ) :
    permission_classes = [AllowAny]

    @swagger_auto_schema (
        request_body=LoginSerializer,
        responses={200 : '{"refresh": "string", "access": "string"}'}
    )
    def post(self, request) :
        serializer = LoginSerializer ( data=request.data )
        serializer.is_valid ( raise_exception=True )
        user = serializer.validated_data['user']
        token = get_tokens_for_user ( user )
        return Response ( data=token, status=status.HTTP_200_OK )


@swagger_auto_schema (
    method='get',
    manual_parameters=[
        openapi.Parameter ( 'month', openapi.IN_QUERY, description="Month (1-12)", type=openapi.TYPE_INTEGER,
                            required=True ),
        openapi.Parameter ( 'year', openapi.IN_QUERY, description="Year (For example: 2023)", type=openapi.TYPE_INTEGER,
                            required=True ),
    ],
    operation_description='Statistics of all employees'
)
@api_view ( ['GET'] )
def employee_statistics_list(request) :
    month = request.GET.get ( 'month' )
    year = request.GET.get ( 'year' )

    if not month or not year :
        return Response (
            {"error" : "input month and year"},
            status=status.HTTP_400_BAD_REQUEST
        )

    employees = Employee.objects.all ()
    result = []

    for employee in employees :
        orders = Order.objects.filter (
            employee=employee,
            order_date__month=month,
            order_date__year=year
        )

        customers_count = orders.values ( 'customer' ).distinct ().count ()

        total_sales = orders.aggregate ( Sum ( 'total_price' ) )['total_price__sum'] or 0

        result.append ( {
            'employee_id' : employee.id,
            'full_name' : employee.full_name,
            'customers_count' : customers_count,
            'total_sales' : float ( total_sales )
        } )

    return Response ( result )


@swagger_auto_schema (
    method='get',
    manual_parameters=[
        openapi.Parameter ( 'month', openapi.IN_QUERY, description="Month (1-12)", type=openapi.TYPE_INTEGER,
                            required=True ),
        openapi.Parameter ( 'year', openapi.IN_QUERY, description="Year (For example: 2023)", type=openapi.TYPE_INTEGER,
                            required=True ),
    ],
    operation_description='Statistics of the employee (detailed)'
)
@api_view ( ['GET'] )
def employee_statistics_detail(request, employee_id) :
    month = request.GET.get ( 'month' )
    year = request.GET.get ( 'year' )

    if not month or not year :
        return Response (
            {"error" : "input month and year"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try :
        employee = Employee.objects.get ( id=employee_id )
    except Employee.DoesNotExist :
        return Response (
            {"error" : "Employee not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    orders = Order.objects.filter (
        employee=employee,
        order_date__month=month,
        order_date__year=year
    )

    customers_count = orders.values ( 'customer' ).distinct ().count ()

    orders_count = orders.count ()

    products_count = OrderProduct.objects.filter (
        order__in=orders
    ).aggregate ( Sum ( 'quantity' ) )['quantity__sum'] or 0

    total_sales = orders.aggregate ( Sum ( 'total_price' ) )['total_price__sum'] or 0

    result = {
        'employee_id' : employee.id,
        'full_name' : employee.full_name,
        'customers_count' : customers_count,
        'products_count' : products_count,
        'orders_count' : orders_count,
        'total_sales' : float ( total_sales )
    }

    return Response ( result )


@swagger_auto_schema (
    method='get',
    manual_parameters=[
        openapi.Parameter ( 'month', openapi.IN_QUERY, description="Month (1-12)", type=openapi.TYPE_INTEGER,
                            required=True ),
        openapi.Parameter ( 'year', openapi.IN_QUERY, description="Year (For example: 2023)", type=openapi.TYPE_INTEGER,
                            required=True ),
    ],
    operation_description='Statistics of all employees'
)
@api_view ( ['GET'] )
def customer_statistics_list(request) :
    month = request.GET.get ( 'month' )
    year = request.GET.get ( 'year' )

    if not month or not year :
        return Response (
            {"error" : "input month and year"},
            status=status.HTTP_400_BAD_REQUEST
        )

    customers = Customer.objects.all ()
    result = []

    for customer in customers :
        orders = Order.objects.filter (
            customer=customer,
            order_date__month=month,
            order_date__year=year
        )

        products_count = OrderProduct.objects.filter (
            order__in=orders
        ).aggregate ( Sum ( 'quantity' ) )['quantity__sum'] or 0

        total_purchases = orders.aggregate ( Sum ( 'total_price' ) )['total_price__sum'] or 0

        result.append ( {
            'customer_id' : customer.id,
            'full_name' : customer.full_name,
            'products_count' : products_count,
            'total_purchases' : float ( total_purchases )
        } )

    return Response ( result )


@swagger_auto_schema (
    method='get',
    manual_parameters=[
        openapi.Parameter ( 'month', openapi.IN_QUERY, description="Month (1-12)", type=openapi.TYPE_INTEGER,
                            required=True ),
        openapi.Parameter ( 'year', openapi.IN_QUERY, description="Year (For example: 2023)", type=openapi.TYPE_INTEGER,
                            required=True ),
    ],
    operation_description='Statistics of the customer (detailed)'
)
@api_view ( ['GET'] )
def customer_statistics_detail(request, customer_id) :
    month = request.GET.get ( 'month' )
    year = request.GET.get ( 'year' )

    if not month or not year :
        return Response (
            {"error" : "input month and year"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try :
        customer = Customer.objects.get ( id=customer_id )
    except Customer.DoesNotExist :
        return Response (
            {"error" : "Customer not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    orders = Order.objects.filter (
        customer=customer,
        order_date__month=month,
        order_date__year=year
    )

    orders_count = orders.count ()

    products_count = OrderProduct.objects.filter (
        order__in=orders
    ).aggregate ( Sum ( 'quantity' ) )['quantity__sum'] or 0

    total_purchases = orders.aggregate ( Sum ( 'total_price' ) )['total_price__sum'] or 0

    result = {
        'customer_id' : customer.id,
        'full_name' : customer.full_name,
        'products_count' : products_count,
        'orders_count' : orders_count,
        'total_purchases' : float ( total_purchases )
    }

    return Response ( result )