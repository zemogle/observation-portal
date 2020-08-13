from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response

from observation_portal.accounts.tasks import send_mail
from observation_portal.accounts.serializers import UserSerializer, AccountRemovalSerializer


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        if self.request.user.is_authenticated:
            return self.request.user
        else:
            return None


class RevokeApiTokenApiView(APIView):
    """
    View to revoke an API token.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        Token.objects.create(user=request.user)
        return Response({'message': 'API token revoked.'})


class AccountRemovalRequestApiView(APIView):
    """
    View to request account removal.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AccountRemovalSerializer(data=request.data)
        if serializer.is_valid():
            message = 'User {0} would like their account removed.\nReason:\n {1}'.format(
                request.user.email, serializer.validated_data['reason']
            )
            send_mail.send(
                'Account removal request submitted', message, 'portal@lco.global', ['science-support@lco.global']
            )
            return Response({'message': 'Account removal request successfully submitted.'})
        else:
            return Response(serializer.errors, status=400)
