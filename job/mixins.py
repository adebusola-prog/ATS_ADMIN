from rest_framework.response import Response
from rest_framework import generics
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT


class CustomMessageCreateMixin(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer=serializer)
        response = {
            "message": "Created Successfully"
        }
        return Response(response, status=HTTP_201_CREATED)
    

class CustomMessageUpdateMixin(generics.CreateAPIView):
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception = True)
        self.perform_create(serializer=serializer)
        response = {
            "message": "Updated Successfully"
        }
        return Response(response, status=HTTP_201_CREATED)