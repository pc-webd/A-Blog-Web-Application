
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

class LoginView(APIView):

    def post(self,request):
        response={}
        response['status']=500
        response['message']='something went Wrong'

        try:
            data=request.data

            if data.get('username') is None:
                response['message']='Key Username not found'
                raise Exception('Key Username not found')
            
            if data.get('password') is None:
                response['message']='Key password not found'
                raise Exception('Key Password not found')

            check_user=User.objects.filter(username=data.get('username')).first()
            if check_user is None:
                response['message']='Invalid Username'
                raise Exception('User not found')  

            user_obj=authenticate(username= data.get('username'), password=data.get('password'))

            if user_obj:
                login(request,user_obj)
                response['status']=200
                response['message']='Welcome'
            else:
                response['message']='Invalid Password'
                raise Exception('Password not match') 

        except Exception as e:
            print(e)

        return Response(response)

LoginView= LoginView.as_view()


class RegisterView(APIView):

    def post(self,request):
        response={}
        response['status']=500
        response['message']='something went Wrong'

        try:
            data=request.data

            if data.get('username') is None:
                response['message']='Key Username not found'
                raise Exception('Key Username not found')
            
            if data.get('password') is None:
                response['message']='Key password not found'
                raise Exception('Key Password not found')

            check_user=User.objects.filter(username=data.get('username')).first()
            if check_user:
                response['message']=' Username has been already taken'
                raise Exception(' Username has been already taken')  

            user_obj=User.objects.create(username=data.get('username'))
            user_obj.set_password(data.get('password'))
            user_obj.save()
            response['status']=200
            response['message']='User Created'
        

        except Exception as e:
            print(e)

        return Response(response)

RegisterView= RegisterView.as_view()