from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from members.models import Member
from .serializer import MemberSerializer, EmailTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from rest_framework import status

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer
    permission_classes = [AllowAny]

@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_member_info(request):
    members = Member.objects.all()
    serializer = MemberSerializer(members, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    trainee_code = request.data.get('trainee_code')

    try:
        member = Member.objects.get(email=email)
    except Member.DoesNotExist:
        return Response(
            {"message": "Member with this email does not exist."},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    if member.user is not None:
        return Response(
            {"message": "This member already has an account."},
            status=400
        )
    User = get_user_model()

    user = User.objects.create_user(
        username=member.email,   
        email=member.email,
        password=password,
    )
    member.trainee_code = trainee_code
    member.user = user
    member.save()

    return Response(
        {"message": "User created successfully."},
        status=status.HTTP_201_CREATED
    )