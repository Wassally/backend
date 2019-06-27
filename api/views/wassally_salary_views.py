from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api.serializers import ComputingSalarySerializer

from api.utils import computing_salary


@api_view(['POST'])
def ComputingSalary(request):
    ''' view for computing salary '''

    serializer = ComputingSalarySerializer(data=request.data)
    if serializer.is_valid():
        from_location = serializer.data['from_location']
        to_location = serializer.data['to_location']
        weight = serializer.data['weight']

        salary = computing_salary(to_location, from_location, weight)
        content = {"expected_salary": salary}
        return Response(content, status=status.HTTP_200_OK)
    print(request.data, serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
