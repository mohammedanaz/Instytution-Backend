from rest_framework import status ,generics
from rest_framework.response import Response
from rest_framework.views import APIView
<<<<<<< HEAD
from rest_framework.permissions import IsAuthenticated
from .serializers import CourseSerializer, LessonSerializer
=======
from .serializers import CourseSerializer
>>>>>>> dev
from accounts.permissions import IsCourseAdmin
from courses.models import Course
from urllib.parse import unquote
from rest_framework.serializers import ValidationError
from django.shortcuts import get_object_or_404
from courses.models import Program
from .serializers import *

class CourseCreateView(APIView):
    """ api for create new course and return its data """
    permission_classes = [IsCourseAdmin]

    def get(self, request, *args, **kwargs):
        course_name = unquote(kwargs.get('course_name', None))  
        if course_name: 
            try:
                course = Course.objects.get(name=course_name)
                serializer = CourseSerializer(course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Course.DoesNotExist:
                return Response({"error": "Course not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        print('request data',request.data)
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(created_by=request.user, updated_by=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AddCourseLessonView(APIView):
    """To add or update Lesson instance of a particular Course"""
    permission_classes = [IsAuthenticated, IsCourseAdmin]

    def post(self, request, course_name, *args, **kwargs):
        lessons_data = self.restructure_lessons_data(request.data)
        course = Course.objects.get(name__iexact=course_name)

        for lesson_data in lessons_data:
            lesson_data['name'] = lesson_data.pop('lessonName', None)
            lesson_data['description'] = lesson_data.pop('lessonDescription', None)
            lesson_data['course'] = course.id 

            if 'week' in lesson_data:
                lesson_data['week'] = int(lesson_data['week'])

            serializer = LessonSerializer(data=lesson_data, context={'request': request})

            if serializer.is_valid():
                try:
                    serializer.save()
                except Exception as e:
                    print('Error while creating Lesson instance - ', str(e))
                    print('Errors serializer:', serializer.errors)
            else:
                print('LessonSerializer data not valid error inside AddCourseLessonView')
                print('Errors:', serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"status": "lessons created"}, status=status.HTTP_201_CREATED)
    
    def restructure_lessons_data(self, data):
        """Reorganize QueryDict data into a structured lessons list to pass to LessonSerializer"""
        lessons = {}
        
        for key, value in data.lists():
            if key.startswith('lessons'):
                lesson_index = int(key.split('[')[1].split(']')[0])
                
                if lesson_index not in lessons:
                    lessons[lesson_index] = {
                        'lessonName': '',
                        'lessonDescription': '',
                        'week': 0,
                        'images': [],
                        'pdfs': [],
                        'videos': [],
                    }

                if 'pdfs' in key:
                    lessons[lesson_index]['pdfs'].append({'pdf': value[0]})
                elif 'images' in key:
                    lessons[lesson_index]['images'].append({'image': value[0]})
                elif 'videos' in key:
                    lessons[lesson_index]['videos'].append({'video': value[0]})
                else:
                    field_name = key.split(']')[1].lstrip('[').rstrip(']')
                    if field_name == 'week':
                        lessons[lesson_index][field_name] = int(value[0])
                    lessons[lesson_index][field_name] = value[0]

        lessons_list = [lesson_data for lesson_data in lessons.values()]
        return lessons_list

class CourseUpdateView(generics.UpdateAPIView):
    """ API for updating an existing course """
    permission_classes = [IsCourseAdmin]
    serializer_class = CourseSerializer

    def get_object(self):
        """ Retrieve the course instance to be updated. """
        course_name = self.kwargs.get('course_name', None)
        if course_name:
            return get_object_or_404(Course, name=unquote(course_name))
        raise ValidationError({"course_name": "Course name is required."})

    def patch(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProgramCreateAPIView(generics.CreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsCourseAdmin]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            updated_by=self.request.user
        )

class ProgramRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    lookup_field = 'name'   
