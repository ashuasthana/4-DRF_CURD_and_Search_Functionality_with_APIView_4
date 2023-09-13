from django.shortcuts import render
from .models import Employee
from rest_framework.views import APIView
from .serializers import EmployeeSerializer
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status

# Create your views here.
class EmployeeListAPIView(APIView):
    serializer_class=EmployeeSerializer
    #Show all Employee=============================
    # def get(self,request,*args,**kwargs):
    #     qs=Employee.objects.all()
    #     serializer=EmployeeSerializer(qs,many=True)
    #     return Response(serializer.data)
    
    #Implement Search Operation viA 'ename' From Employee===http://127.0.0.1:8000/api/?search=Anil==========================
    def get(self,request,*args,**kwargs):
        # qs=Employee.objects.all()
        name=self.request.GET.get('search')
        if name is not None:
            # qs=qs.filter(ename__icontains=name)
            qs = Employee.objects.filter(ename__icontains=name)
            serializer=EmployeeSerializer(qs,many=True)
            if serializer.data:
                return Response(serializer.data)
            else:
                return Response({"message": "No employees found with that name."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "Please provide a name to search for."}, status=status.HTTP_400_BAD_REQUEST)
        
    
    #create a new Employee=============================
    def post(self, request, format=None):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EmployeeDetailAPIView(APIView):   
    """
    Retrieve, update or delete a Employee instance.
    """
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Employee = self.get_object(pk)
        serializer = EmployeeSerializer(Employee)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Employee = self.get_object(pk)
        serializer = EmployeeSerializer(Employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Employee = self.get_object(pk)
        Employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 