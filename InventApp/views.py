from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .serializers import SignUpSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes, permission_classes

@method_decorator(csrf_exempt, name='dispatch')
class UserSignupView(APIView):
    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            refresh_token = str(refresh)
            
            
            return Response(
                {
                    "message": "User authenticated successfully",
                    "statuscode": 201,
                    "token": token,
                    "refresh_token": refresh_token,
                    "email": user.email,
                    "id": user.id 
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    "message": "Credentials incomplete, kindly re-enter",
                    "statusCode": 400,
                    "errors": serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

@authentication_classes([])
@permission_classes([])
class Login(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "Invalid email, please check your email address", "status": 404},
                status=status.HTTP_404_NOT_FOUND
            )

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response(
                {
                    "message": "User authenticated successfully",
                    "statusCode": 200,
                    "data": {
                        "access_token": token,
                        "refresh_token": refresh_token,
                        "email": user.email,
                        "id": user.id,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Incorrect password, kindly re-enter your password", "statusCode": 401},
                status=status.HTTP_401_UNAUTHORIZED,
            )

            

from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
        except KeyError:
            return Response({"error": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)
        except InvalidToken:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        except TokenError:
            return Response({"error": "Token error"}, status=status.HTTP_400_BAD_REQUEST)
        


from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Product
from .serializers import ProductSerializer



class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from .models import Order
from .serializers import OrderCreateSerializer

class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





        
        
### Admin views
        

@method_decorator(csrf_exempt, name='dispatch')
class AdminLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"message": "Invalid email, please check your email address", "status": 404}, status=status.HTTP_404_NOT_FOUND
            )

        if not user.is_staff:
            return Response(
                {"message": "Not authorized!. Admin access required.", "status": 403}, status=status.HTTP_403_FORBIDDEN
            )

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            token = str(refresh.access_token)

            
            return Response(
                {
                    "message": "Admin authenticated successfully",
                    "statusCode": 200,
                    "data": {
                        "access_token": token,
                        "email": user.email,
                        "id": user.id,
                        "is_admin": user.is_staff
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"message": "Incorrect password, kindly re-enter your password", "statusCode": 401}, status=status.HTTP_401_UNAUTHORIZED,
            )
        
        

from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import Product
from .serializers import ProductSerializer



class ProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProductCreateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
from .models import Order
from .serializers import OrderSerializer

class OrderStatusUpdateView(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        status = request.data.get('status')
        if status not in dict(Order.STATUS_CHOICES):
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        order.status = status
        order.save()
        return Response({"status": "Order status updated"}, status=status.HTTP_200_OK)
