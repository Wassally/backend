from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ComputingSalarySerializer


@api_view(['POST'])
def ComputingSalary(request):
    ''' view for computing salary '''

    serializer = ComputingSalarySerializer(data=request.data)
    if serializer.is_valid():

        salary = 0
        content = {"expected_salary": salary}
        return Response(content, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
