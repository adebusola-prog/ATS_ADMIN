# from django.test import TestCase
# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework import status
# from .models import Location, Job
# from .serializers import LocationSerializer, JobSerializer


# class LocationListAPIViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('jobs:location_list')
#         self.location1 = Location.objects.create(name='Location 1')
#         self.location2 = Location.objects.create(name='Location 2')

#     def test_list_locations(self):
#         response = self.client.get(self.url)
#         locations = Location.objects.all()
#         serializer = LocationSerializer(locations, many=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)


# class ApplicantJobListAPIViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse('jobs:job_list_create')
#         self.job1 = Job.objects.create(role='Job 1', skill_level='Level 1', posted_by=self.admin_user)
#         self.job2 = Job.objects.create(role='Job 2', skill_level='Level 2', posted_by=self.admin_user)
        

#     def test_list_jobs(self):
#         response = self.client.get(self.url)
#         jobs = Job.objects.all()
#         serializer = JobSerializer(jobs, many=True)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, serializer.data)

#     # Add more test methods for other views...

# # class JobListCreateAPIViewTestCase(TestCase):
# #     # Write tests for JobListCreateAPIView

# # class JobDetailUpdateAPIViewTestCase(TestCase):
# #     # Write tests for JobDetailUpdateAPIView

# # class JobDeleteAPIViewTestCase(TestCase):
# #     # Write tests for JobDeleteAPIView
