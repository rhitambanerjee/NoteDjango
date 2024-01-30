from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Task
from .serializer import TaskSerializer
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status


# Create your views here.

@api_view(['GET','POST','DELETE'])
def handleData(request):
    if request.method == 'GET':
        app = Task.objects.all()
        serializer = TaskSerializer(app, many=True)
        print(serializer.data[0]['id'])
        return Response({'tasks':serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if 'tasks' in request.data:
            data = request.data.get('tasks', [])
            ids=[]
            for item in data:
                serializer = TaskSerializer(data=item)
                if serializer.is_valid():
                    serializer.save()
                    ids.append({"id": serializer.data['id']})
                else:
                    return Response("Please follow the given structure for creating the notes",status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response({"tasks": ids}, status=status.HTTP_201_CREATED)
        else:
            serializer = TaskSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
            return Response({"id": serializer.data['id']}, status=status.HTTP_201_CREATED)

    elif request.method == 'DELETE':
        data = request.data.get('tasks', [])
        ids = [item.get('id') for item in data]
        if not ids:
            return Response('No IDs provided for deletion')

        tasks_deleted = Task.objects.filter(id__in=ids).delete()

        if tasks_deleted[0] > 0:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response('No tasks with the given id are found',status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET','DELETE','PUT','PATCH'])
def GetDeleteById(request,pk):
    
    if request.method=='GET':
        try:
            task=Task.objects.get(pk=pk)
        except:
            return Response("There is no task at that id",status=status.HTTP_404_NOT_FOUND)
        data=TaskSerializer(task)
        return Response(data.data, status=status.HTTP_200_OK)
    
    elif request.method=='DELETE':
        try:
            task=Task.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_204_NO_CONTENT)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    elif request.method=='PUT':
        try:
            task=Task.objects.get(pk=pk)
        except:
            return Response("There is no task at that id",status=status.HTTP_404_NOT_FOUND)
        data=JSONParser().parse(request)
        taskSerialzer=TaskSerializer(task,data)
        if taskSerialzer.is_valid():
            taskSerialzer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Please follow the given model for data",status=status.HTTP_406_NOT_ACCEPTABLE)
    
    elif request.method=='PATCH':
        try:
            task=Task.objects.get(pk=pk)
        except:
            return Response("There is no task at that id",status=status.HTTP_404_NOT_FOUND)
        data=JSONParser().parse(request)
        taskSerialzer=TaskSerializer(task,data,partial=True)
        if taskSerialzer.is_valid():
            taskSerialzer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("Please follow the given model for data",status=status.HTTP_406_NOT_ACCEPTABLE)
    else:
        return Response('No such method allowed',status=status.HTTP_405_METHOD_NOT_ALLOWED)
