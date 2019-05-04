from rest_framework.views import APIView
from rest_framework.response import Response
from api.logic import computing_salary


class ComputingSalary(APIView):

    def post(self, request, format=None):
        to_place = request.POST.get("to_place", None)
        from_place = request.POST.get("from_place", None)
        weight = request.POST.get("weight", None)

        if to_place and from_place and weight:
            salary = computing_salary(to_place, from_place, weight)
            content = {"expected_salary": salary}
            return Response(content, status=status.HTTP_200_OK)
        return Response({"message": "error"}, status=status.HTTP_409_CONFLICT)
