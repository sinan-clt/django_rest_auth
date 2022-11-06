from django.shortcuts import render
from rest_app.serializers import *
from rest_app.models import *
from django.http import QueryDict

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import datetime


# Create your views here.

# register **
class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['username'] = request.POST['email']
        request.POST._mutable = mutable
        serializer = UserSerializer(data=request.data)
        validate = serializer.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": serializer.errors})

        user = User.objects.create_user(name=request.POST['name'], phone_number=request.POST['phone_number'], username=request.POST['email'],
                                        email=request.POST['email'], password=request.POST['password'])
        user.is_active = True
        user.is_gmail_authenticated = True
        user.save()

        fields = ('id', 'username', 'email', 'phone_number', 'name')
        data = UserSerializer(user, many=False, fields=fields)
        response = {
            'success': 'True',
            'status': 200,
            'message': 'User created successfully',
            'data': data.data,
        }

        return Response(response)


# login **
class UserLogin(APIView):
    permission_classes = [AllowAny]

    class Validation(serializers.Serializer):
        email = serializers.CharField()
        password = serializers.CharField()

    def post(self, request):

        validation = self.Validation(data=request.data)
        validate = validation.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": validation.errors})

        user = User.objects.filter(
            email=request.POST['email'], is_gmail_authenticated=True).first()

        if user:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['password'] = request.POST['password']
            request.POST._mutable = mutable
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fields = ('id', 'username', 'email', 'phone_number', 'name')
            data = UserSerializer(user, many=False, fields=fields)
            response = {
                'success': 'True',
                'status': 200,
                'message': 'User logged in successfully',
                'token': serializer.data['token'],
                'data': data.data,
            }

            return Response(response)



# registration and auto login **
class RegisterandLogin(APIView):
    permission_classes = [AllowAny]

    class Validation(serializers.Serializer):
        email = serializers.CharField()
        name = serializers.CharField()

    def post(self, request):

        validation = self.Validation(data=request.data)
        validate = validation.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": validation.errors})

        user = User.objects.filter(
            email=request.POST['email'], is_gmail_authenticated=True).first()

        if user:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['password'] = 'captainamerica'
            request.POST._mutable = mutable
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fields = ('id', 'username', 'email', 'phone_number', 'name')
            data = UserSerializer(user, many=False, fields=fields)
            response = {
                'success': 'True',
                'status': 200,
                'message': 'User logged in  successfully',
                'token': serializer.data['token'],
                'data': data.data,
            }

            return Response(response)
        else:
            mutable = request.POST._mutable
            request.POST._mutable = True
            request.POST['password'] = 'captainamerica'
            request.POST['username'] = request.POST['email']
            request.POST._mutable = mutable
            serializer = UserSerializer(data=request.data)
            validate = serializer.is_valid()
            if validate is False:
                return Response({"status": 400, "message": "Incorrect Inputs", "data": serializer.errors})

            user = User.objects.create_user(name=request.POST['name'], username=request.POST['email'],
                                            email=request.POST['email'], password='captainamerica')
            user.is_active = True
            user.is_gmail_authenticated = True
            user.save()

            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            fields = ('id', 'username', 'email', 'phone_number', 'name')
            data = UserSerializer(user, many=False, fields=fields)
            response = {
                'success': 'True',
                'status': 200,
                'message': 'User created and logged in  successfully',
                'token': serializer.data['token'],
                'data': data.data,
            }

            return Response(response)



# authenticated_user **
class UserDetails(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(items, many=True)
        return Response({'data':serializer.data,'status': 200, "message": "success"})


# add-products **
class addProducts(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user.id
        name = request.data["name"]
        price = request.data["price"]
        quantity = request.data["quantity"]
        product_image = request.data["product_image"]
        ordinary_dict = {'seller': user, 'name': name, 'price': price,
                         'quantity': quantity,'product_image':product_image}
        query_dict = QueryDict('', mutable=True)
        query_dict.update(ordinary_dict)
        products_details = ProductSerializer(data=query_dict)
        if products_details.is_valid():
            products_details.save()
            data = {'status': 200, "message": "product added successfully",
                    "data": products_details.data}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'status': 400, "message": "can't add product", "error": products_details.errors}
            return Response(data, status=status.HTTP_200_OK)


# edit-products **
class editProducts(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        product = Products.objects.get(id=id)
        product.name = request.data["name"]
        product.price = request.data["price"]
        product.quantity = request.data["quantity"]
        product.product_image = request.data["product_image"]
        product.save()
        data = {'status': 200, "message": "product updated successfully"}
        return Response(data, status=status.HTTP_200_OK)

    # def put(self, request, id): 
    #     adrress = Products.objects.get(id=id)
    #     serializer = ProductSerializer(adrress, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #     data = {'status': 200, "message": "product updated successfully"}
    #     return Response(data, status=status.HTTP_200_OK)


# delete-products **
class deleteProducts(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, id):
        alreadyexist = Products.objects.filter(id=id).exists()
        if alreadyexist is True:
            products = Products.objects.get(id=id)

            products.is_deleted = True
            products.deleted_at = datetime.datetime.now()
            products.save()
            data = {'status': 400, "message": "product deleted successfully"}
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {'status': 400, "message": "product doesn't exist"}
            return Response(data, status=status.HTTP_200_OK)



# products-add-to-cart **
class addTocart(APIView):
    permission_classes = [IsAuthenticated]

    class CartParameter(serializers.Serializer):
        product = serializers.IntegerField()
        count = serializers.IntegerField()

    def post(self, request):
        if not request.POST:
            serializer = AddToCartSerializer(data=request.data)
            serializer.is_valid()
            return Response({"status": 400, "message": "Incorrect Inputs", "data": serializer.errors},
                            status=status.HTTP_200_OK)

        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['user'] = request.user.id
        request.POST._mutable = mutable
        serializer = self.CartParameter(data=request.data)
        validate = serializer.is_valid()
        if validate is False:
            return Response({"status": 400, "message": "Incorrect Inputs", "data": serializer.errors},
                            status=status.HTTP_200_OK)

        items = Cart.objects.filter(
            user=request.user, product=request.POST['product'], is_deleted=False)
        if items.exists():
            first_item = items.first()
            first_item.count += int(request.POST['count'])
            first_item.save()
            serializer = AddToCartSerializer(first_item, many=False)
            data = serializer.data
            return Response({"status": 200, "message": "item added to cart successfully", "data": data})
        else:
            item = Cart()
            item.user = request.user
            item.product = Products.objects.get(id=request.POST['product'])
            item.count = int(request.POST['count'])
            item.save()
            serializer = AddToCartSerializer(item, many=False)
            data = serializer.data
            return Response({"status": 200, "message": "item added to cart successfully", "data": data})

 
# fetching user-cart **
class fetchCart(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user.id
        cart_details = Cart.objects.filter(user=user, is_deleted=False)
        serializer = CartSerializer(cart_details, many=True)
        data = {'status': 200, "message": "success", "data": serializer.data}
        return Response(data, status=status.HTTP_200_OK)
