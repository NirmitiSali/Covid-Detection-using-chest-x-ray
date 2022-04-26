from django.shortcuts import render
from flask import request

from .models import *

from keras.models import load_model
import cv2
import numpy as np

from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import train_test_split
import pandas as pd

img_size = 100
model = load_model('app1\model-007_best_cnn.model')
label_dict = {'COVID19': 0, 'NORMAL': 1, 'PNEUMONIA': 2}


def preprocess(img):
	img = np.array(img)

	if (img.ndim == 3):
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	else:
		gray = img

	gray = gray / 255
	resized = cv2.resize(gray, (img_size, img_size))
	reshaped = resized.reshape(1, img_size, img_size)
	return reshaped


def modelss(X_train, Y_train):
	tree = DecisionTreeClassifier(criterion='entropy', random_state=0)
	tree.fit(X_train, Y_train)
	print('Decision Tree Classifier Training Accuracy:', tree.score(X_train, Y_train))
	return tree


def fromsymptoms(cough, fever, sore_throat, breath, headache, age):
	df = pd.read_csv('app1\covid_symptoms - covid_symptoms.csv')
	X = df.iloc[:, 1:7].values
	Y = df.iloc[:, -1].values
	X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)
	# from sklearn.preprocessing import StandardScaler
	# sc = StandardScaler()
	# X_train = sc.fit_transform(X_train)
	# X_test = sc.transform(X_test)
	model = modelss(X_train, Y_train)
	predic = [cough, fever, sore_throat, breath, headache, age]
	p = np.array(predic)
	# q = sc.transform(p.reshape(1,-1))
	if model.predict(p.reshape(1, -1)) == [1]:
		return "COVID POSITIVE"
	else:
		return "COVID NEGATIVE"


def result(last_patient, label, accuracy, sym):
	return render(request, 'result.html',
				  {'last_patient': last_patient, 'label': label, 'accuracy': accuracy, 'sym': sym})


# Create your views here.
def home(request):
	return render(request, 'home.html')

def call(request):
	return render(request, 'callforhelp.html')

def index(request):
	if request.method == "POST":
		symp = data()
		age = int(request.POST.get('age'))
		temp = int(request.POST.get('temp'))
		cough = int(request.POST.get('cough'))
		sore_throat = int(request.POST.get('sore_throat'))
		breathing = int(request.POST.get('breathing'))
		headache = int(request.POST.get('headache'))

		if age < 60:
			age_bool = 0
		else:
			age_bool = 1

		if temp < 98.6:
			fever = 0
		else:
			fever = 1
		sym = fromsymptoms(cough, fever, sore_throat, breathing, headache, age_bool)
		patient_name = request.POST.get('patient_name')
		symp.patient_name = patient_name
		symp.age = age
		symp.temp = temp
		symp.cough = cough
		symp.sore_throat = sore_throat
		symp.breathing = breathing
		symp.headache = headache
		symp.image = request.FILES['image']
		symp.result_from_symp = sym

		symp.save()
		last = data.objects.last()
		last_patient = last.patient_name

		# path = str(request.FILES['image'])
		# pre_path = "image/"
		# img_path = os.path.join(pre_path,path)
		img_path = str(last.image)

		print(img_path)

		image = cv2.imread(img_path)

		test_image = preprocess(image)
		prediction = model.predict(test_image)
		result = np.argmax(prediction, axis=1)[0]
		accuracy = float(np.max(prediction, axis=1)[0])
		accuracy=round(accuracy,2)
		for k, v in label_dict.items():
			if v == result:
				label = k
		last.result_from_xray = label
		last.save()
		# result(last_patient,label,accuracy,sym)
		return render(request, 'result.html',
					  {'last_patient': last_patient, 'label': label, 'accuracy': accuracy, 'sym': sym})
	return render(request, 'index.html')


from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from random import randrange
from covid_detection.settings import EMAIL_HOST_USER
from django.core.mail import send_mail


def usignup(request):
	if request.method == "POST":
		un = request.POST.get('un')
		em = request.POST.get('em')
		if request.POST['password'] == request.POST['confirm_password']:
			try:
				usr = User.objects.get(username=un)
				return render(request, 'usignup.html', {'msg': "Username already exists!!"})
			except User.DoesNotExist:
				try:
					usr = User.objects.get(email=em)
					return render(request, 'usignup.html', {'msg': 'Email already exists!!'})
				except User.DoesNotExist:
					usr = User.objects.create_user(username=request.POST['un'], password=request.POST['password'],
												   email=request.POST['em'])
					usr.save()
					return redirect('ulogin')
		else:
			return render(request, 'usignup.html', {'msg': "Incorrect Password"})
	return render(request, 'usignup.html')


def ulogin(request):
	if request.method == "POST":
		un = request.POST.get('un')
		pw = request.POST.get('pw')
		usr = authenticate(username=un, password=pw)
		if usr is None:
			return render(request, 'ulogin.html', {'msg': 'Invalid credentials!!'})
		else:
			login(request, usr)
			return redirect('index')
	else:
		return render(request, 'ulogin.html')


def ulogout(request):
	logout(request)
	return redirect('ulogin')



def contact_us(request):
	if request.method == "POST":
		name = request.POST.get('name')
		email = request.POST.get('email')
		subject = request.POST.get('subject')
		message = request.POST.get('message')
		obj = contact()
		obj.name = name
		obj.email = email
		obj.subject = subject
		obj.message = message
		obj.save()
		