from django.shortcuts import render,redirect
from django.core.files.storage import FileSystemStorage
import pickle
from django.http import HttpResponseRedirect
# import joblib
import os
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
from .dl_model import getResult, get_className
from django.utils.text import get_valid_filename
from .dl_model_DR import preprocess_image, class_name
from django.conf import settings

from tensorflow.keras.models import load_model 
from sklearn.preprocessing import StandardScaler
import numpy as np

from .forms import SignUpForm,LoginForm
# Create your views here.
# model2 = 
# model = joblib.load('./models/svm.pkl')

def home(request):
    return render(request, 'index.html')

def diabetes(request):
    if request.method=='POST':
        pregnancies = float(request.POST['Pregnancies'])
        glucose = float(request.POST['glucose'])
        bp = float(request.POST['BP'])
        skinthickness = float(request.POST['skinthickness'])
        insulin = float(request.POST['insulin'])
        bmi = float(request.POST['bmi'])
        dpf = float(request.POST['DPF'])
        age = float(request.POST['age'])
        
        sc = pickle.load(open('models/sc.pkl','rb'))
        model1 = pickle.load(open('models/Diabetes_Prediction.pkl','rb'))
        
        input_data = np.array([[pregnancies, glucose, bp, skinthickness, insulin, bmi, dpf, age]])
        # scaler = StandardScaler()
        # # Transform the data using the pre-fitted scaler
        # scaled_data = scaler.transform(input_data)
        
        y_pred = model1.predict(sc.transform(input_data.reshape(1,-1)))
        
        
        # print(f"Raw prediction: {y_pred}, Converted prediction: {prediction}")
        
        if y_pred == [1]:
            result = "Positive - You may Have Diabetes"
        elif y_pred==[0]:
            result = "Negative - No Diabetes"
        else:
            result = "Unexpected prediction value"
        
        return render(request,'diabetes.html',{'result' : result})
        
    return render(request, 'diabetes.html')

# @csrf_exempt
def pneumonia(request):
    if request.method == 'POST'and request.FILES['file']:
        file = request.FILES['file']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        value = getResult(file_path)
        result = get_className(value)
        
        # Clean up the file after processing
        fs.delete(filename)
        
        return render(request, 'pneumonia.html', {'result': result})
    return render(request, 'pneumonia.html')
    
            

def DR(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        filename = get_valid_filename(file.name)
        file_storage = FileSystemStorage()
        file_path = file_storage.save(filename,file)
        file_full_path = file_storage.path(file_path)
        
        predicted_class = preprocess_image(file_full_path)
        result = class_name(predicted_class)
        # file_storage.delete(file_path)
        
        return render(request, 'DR.html', {'result': result})
    return render(request, 'DR.html')

# def breast_cancer(request):
#     if request.method=="POST":
        
# def user_signup(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             messages.success(request,"CONGRATULATION, You are Registered!")
#             form.save()
#             username = form.cleaned_data.get('username')
#             messages.success(request, f'Account created for {username}!')
#             return redirect('login')
#     else:
#         form=SignUpForm()
#     return render(request,'signup.html',{'form':form})

# def user_login(request):
#     if not request.user.is_authenticated:
#         if request.method == "POST":
#             form = LoginForm(request = request, data = request.POST)
#             if form.is_valid():
#                 uname = form.cleaned_data['username']
#                 pwd = form.cleaned_data['password']
#                 user = authenticate(username=uname, password=pwd)
#                 if user is not None:
#                     login(request, user)
#                     return redirect('home')
#         else:
#             form = LoginForm()
#         return render(request, 'login.html', {'form':form})
#     else:
#         return redirect('signup')

def remedies(request):
    return render(request, "remedies.html")