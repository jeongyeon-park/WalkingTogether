import json
from django.shortcuts import render

from django.views.generic.base import View
from rest_auth.utils import jwt_encode
import jwt
import requests
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers, status

from .models import User, SocialPlatform, Pet
from .serializer import UserSerializer, UserInfoUpdateSerializer, PetSerializer
import my_settings

# Create your views here.
def home(request):
    return render(request, 'home.html')


# JWT 토큰 유효성 검사
class id_auth:

    def __init__(self, f):
        self.func = f

    def __call__(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            print(access_token)
            payload      = jwt.decode(access_token, my_settings.JWT_SECRET_KEY, my_settings.JWT_ALGORITHM)
            user         = User.objects.get(email = payload["email"])
            request.user = user

            self.func(request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({'MESSAGE': 'INVALID_TOKEN'}, status=401)

        except jwt.InvalidTokenError:
            return JsonResponse({'MESSAGE': 'INVALID_ACCESS_TOKEN'}, status=401)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status=401)

        except User.DoesNotExist:
            return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)


@method_decorator(csrf_exempt, name='dispatch')
class KakaoLoginView(View): #카카오 로그인

    def get(self, request):
        access_token = request.headers["Authorization"]
        headers      = ({"Authorization" : f"{access_token}"})
        url          = "https://kapi.kakao.com/v2/user/me" # Authorization(프론트에서 받은 토큰)을 이용해서 회원의 정보를 확인하기 위한 카카오 API 주소
        response     = requests.request("POST", url, headers=headers) # API를 요청하여 회원의 정보를 response에 저장
        user         = response.json()
        print(user)

        if User.objects.filter(social_login_id=user['id']).exists(): #기존에 소셜로그인을 했었는지 확인
            user_info = User.objects.get(social_login_id=user['id'])
            print(user_info)
            encoded_jwt = jwt.encode({'email': user_info.email}, my_settings.JWT_SECRET_KEY, my_settings.JWT_ALGORITHM) # jwt토큰 발행
            # print(jwt.decode(encoded_jwt, my_settings.JWT_SECRET_KEY, my_settings.JWT_ALGORITHM))

            response_data = {
                'token'           : encoded_jwt.decode('UTF-8'),
                'nickname'        : user_info.nickname,
                'email'           : user_info.email,
                'age_range'       : user_info.age_range,
                'gender'          : user_info.gender
            }
            return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False}, status = 200)            
        else:
            new_user_info = User(
                social_login_id = user['id'],
                social          = SocialPlatform.objects.get(platform ="Kakao"),
                nickname        = user['properties'].get('nickname', None),
                email           = user['kakao_account'].get('email'),
                age_range       = user['kakao_account'].get('age_range', None),
                gender          = user['kakao_account'].get('gender', None)
            )
            new_user_info.save()
            encoded_jwt = jwt.encode({'email': new_user_info.email}, my_settings.JWT_SECRET_KEY, my_settings.JWT_ALGORITHM) # jwt토큰 발행
            # print(jwt.decode(encoded_jwt, my_settings.JWT_SECRET_KEY, my_settings.JWT_ALGORITHM))
            none_member_type = 1
            response_data = {
                'token'             : encoded_jwt.decode('UTF-8'),
                'nickname'          : new_user_info.nickname,
                'email'             : new_user_info.email,
                'age_range'         : new_user_info.age_range,
                'gender'            : new_user_info.gender
                }
            return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False}, status = 200)


@method_decorator(csrf_exempt, name='dispatch')
class GoogleLoginView(View): #구글 로그인

    def post(self, request):
        user = JSONParser().parse(request)
        print(user)

        if User.objects.filter(social_login_id=user['googleId']).exists(): #기존에 소셜로그인을 했었는지 확인
            user_info = User.objects.get(social_login_id=user['googleId'])
            print(user_info)
            encoded_jwt = jwt.encode({'email': user_info.email}, my_settings.JWT_SECRET_KEY, my_settings.JWT_ALGORITHM) # jwt토큰 발행
            # print(jwt.decode(encoded_jwt, my_settings.JWT_SECRET_KEY, my_settings.JWT_ALGORITHM))

            response_data = {
                'token'           : encoded_jwt.decode('UTF-8'),
                'nickname'        : user_info.nickname,
                'email'           : user_info.email,
                'age_range'       : user_info.age_range,
                'gender'          : user_info.gender
            }
            return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False}, status = 200)            
        else:
            new_user_info = User(
                social_login_id = user['googleId'],
                social          = SocialPlatform.objects.get(platform ="Google"),
                nickname        = user.get('name', None),
                email           = user['email']
            )
            new_user_info.save()
            encoded_jwt = jwt.encode({'email': new_user_info.email}, my_settings.JWT_SECRET_KEY, my_settings.JWT_ALGORITHM) # jwt토큰 발행
            # print(jwt.decode(encoded_jwt, my_settings.JWT_SECRET_KEY, my_settings.JWT_ALGORITHM))
            none_member_type = 1
            response_data = {
                'token'             : encoded_jwt.decode('UTF-8'),
                'nickname'          : new_user_info.nickname,
                'email'             : new_user_info.email
                }
            return JsonResponse(response_data, json_dumps_params={'ensure_ascii': False}, status = 200)


@method_decorator(csrf_exempt, name='dispatch')
class UserInfoUpdateView(APIView):

    @id_auth
    def get(request):
        user = request.user
        serializer = UserInfoUpdateSerializer(user)
        return Response(serializer.data)

    @id_auth
    def put(request):
        user = request.user
        serializer = UserInfoUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PetListView(APIView):

    @id_auth
    def get(self, request):
        user = request.user
        pets = Pet.objects.filter(owner=user.email)
        serializer = PetSerializer(pets, many=True)
        return Response(serializer.data)


@method_decorator(csrf_exempt, name='dispatch')
class PetAddView(APIView):

    @id_auth
    def post(self, request, format=None):
        user = request.user
        serializer = PetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.owner = user.email
            serializer.save()
            user.number_of_pet += 1
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class PetInfoUpdateView(APIView):

    @id_auth
    def get_object(self, pk):
        try:
            return Pet.objects.get(pk=pk)
        except Pet.DoesNotExist:
            raise Http404

    @id_auth
    def get(self, request, pk, format=None):
        user = request.user
        pet = self.get_object(pk)
        serializer = PetSerializer(pet)
        if pet.owner == user.email:
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    @id_auth
    def put(self, request, pk, format=None):
        user = request.user
        pet = self.get_object(pk)
        serializer = PetSerializer(pet, data=request.data)
        if pet.owner == user.email:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)

    @id_auth
    def delete(self, request, pk, format=None):
        user = request.user
        pet = self.get_object(pk)
        serializer = PetSerializer(pet, data=request.data)
        if pet.owner == user.email:
            pet.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)