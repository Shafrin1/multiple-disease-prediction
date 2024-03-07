

from flask import Flask, render_template, request, redirect,  flash, abort, url_for

from heart_prob import app,mail
from heart_prob import app
from heart_prob.models import *
import pandas as pd
import os
import sys
import pickle
from datetime import datetime,date
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os
from PIL import Image
from flask_mail import Message
import os
import glob
import tensorflow as tf
from flask import Flask, render_template, request, send_from_directory
from tensorflow.keras.preprocessing.image import ImageDataGenerator

@app.route('/',methods=['GET','POST'])
def index():
    return render_template("index.html")



@app.route('/about',methods=['GET','POST'])
def about():
    return render_template("about.html")

@app.route('/services',methods=['GET','POST'])
def services():
    return render_template("services.html")    

     

@app.route('/feedback',methods=['GET','POST'])
def feedback():
    

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        text = request.form['text']
        my_data = contact(name=name,email=email,number=number,text=text)
        db.session.add(my_data) 
        db.session.commit()
        d="Message Sent Successfully"
        return render_template("feedback.html",d=d)
    return render_template("feedback.html")



@app.route('/contact',methods=['GET','POST'])
def conta():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        text = request.form['text']
        my_data = contact(name=name,email=email,number=number,text=text)
        db.session.add(my_data) 
        db.session.commit()
        d="Message Sent Successfully"
        return render_template("contact.html",d=d)
    return render_template("contact.html")



@login_required
@app.route('/feedbackview',methods=["GET","POST"])
def feedbackview():
    obj = contact.query.all()
    return render_template("feedbackview.html",obj=obj) 



@login_required
@app.route('/viewpatientforadmin',methods=["GET","POST"])
def adminviewpatient():
    obj = registration.query.filter_by(usertype="patient").all()
    return render_template("viewpatientforadmin.html",obj=obj)


@login_required
@app.route('/viewpatient_for_labtec',methods=["GET","POST"])
def viewpatient_for_labtec():
    obj = registration.query.filter_by(usertype="patient",lid=current_user.id).all()
    return render_template("viewpatient_for_labtec.html",obj=obj)


@login_required
@app.route('/vw_test',methods=["GET","POST"])
def vw_test():
    obj = registration.query.filter_by(usertype="patient",lid=current_user.id).all()
    return render_template("vw_test.html",obj=obj)

@login_required
@app.route('/viewpatient_for_Dr',methods=["GET","POST"])
def viewpatientDr():
    obj = registration.query.filter_by(usertype="patient").all()
    return render_template("viewpatient_for_Dr.html",obj=obj)


@login_required
@app.route('/viewlabtec',methods=["GET","POST"])
def viewlabtec():
    obj = registration.query.filter_by(usertype="labtec").all()
    return render_template("viewlabtec.html",obj=obj)


@login_required
@app.route('/vw_queries',methods=["GET","POST"])
def all_queries():
    obj = Qresponses.query.all()
    return render_template("all_queries.html",obj=obj)

@login_required
@app.route('/reply_query/<int:id>',methods=["GET","POST"])
def reply_query(id):
    h=Qresponses.query.filter_by(id=id).first()
   
    if request.method == 'POST':
        h.response = request.form['res']
       
        db.session.commit()
        d="Response Sent Successfully"
        return redirect('/dr_vw_queries')

    return render_template("reply_query.html",h=h)

@login_required
@app.route('/make_query/<int:id>',methods=["GET","POST"])
def make_query(id):
    f=registration.query.filter_by(id=current_user.id).first()
    do=registration.query.filter_by(id=id).first()
    if request.method == 'POST':
        query = request.form['query']
        my_data = Qresponses(uid=[f],did=[do],que=query)
        db.session.add(my_data) 
        db.session.commit()
        d="Query Sent Successfully"
        return render_template('make_query.html',d=d)

    return render_template("make_query.html")






@login_required
@app.route('/viewDr',methods=["GET","POST"])
def viewDr():
    obj = registration.query.filter_by(usertype="Dr").all()
    return render_template("viewDr.html",obj=obj)


@login_required
@app.route('/vw_doc',methods=["GET","POST"])
def vw_doc():
    obj = registration.query.filter_by(usertype="Dr").all()
    return render_template("vw_doc.html",obj=obj)

@login_required
@app.route('/viewDr_for_patient',methods=["GET","POST"])
def viewDr_for_patient():
    obj = registration.query.filter_by(usertype="Dr").all()
    return render_template("viewDr_for_patient.html",obj=obj)    




@app.route('/labtec_reg',methods=['GET','POST'])
def labtec_reg():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        # address=request.form['address']
        number = request.form['number']
        password = request.form['password']
        Qualification=request.form['Qualification']
        # confirm_password = request.form['confirm_password']
        my_data = registration(name=name,email=email,number=number,Qualification=Qualification,password=password,usertype="labtec")
        db.session.add(my_data) 
        db.session.commit()
        ad_sendmail(email,password)
        return redirect('/viewlabtec')
    return render_template("labtec_reg.html")


@app.route('/Dr_reg',methods=['GET','POST'])
def Dr_reg():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        Specialisation=request.form['Specialisation']
        Qualification=request.form['Qualification']

        img=request.files['image']
        pic_file = save_picture(img)
        view = pic_file
        print(view) 


        # address=request.form['address']
        number = request.form['number']
        password = request.form['password']
        # confirm_password = request.form['confirm_password']
        my_data = registration(name=name,email=email,Image=view,number=number,Qualification=Qualification,Specialisation=Specialisation,password=password,usertype="Dr")
        db.session.add(my_data) 
        db.session.commit()
        ad_sendmail(email,password)
        return redirect('/viewDr')
    return render_template("Dr_reg.html")   

def ad_sendmail(email,password):
    msg = Message(' Successfully Added',recipients=[email])
    msg.body = f''' You can login using your Email ID and  Your Password is, {password}  '''
    mail.send(msg)


def app_sendmail(email):
    msg = Message('Approved Successfully ',recipients=[email])
    msg.body = f''' Your Booking is Approved Successfully '''
    mail.send(msg)

def rej_sendmail(email):
    msg = Message('Booking Rejected  ',recipients=[email])
    msg.body = f''' Sorry Your Booking is Rejected  '''
    mail.send(msg)


def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/pics', picture_fn)
    
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn



def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)



@app.route('/patient_reg',methods=['GET','POST'])
def patient_reg():

    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        gender = request.form['gender']
        email = request.form['email']
        address=request.form['address']
        number = request.form['number']
        password = request.form['password']
        # confirm_password = request.form['confirm_password']
        my_data = registration(name=name,lid=current_user.id,email=email,number=number,age=age,gender=gender,address=address,password=password,usertype="patient")
        db.session.add(my_data) 
        db.session.commit()
        ad_sendmail(email,password)
        return redirect('/viewpatient_for_labtec')
    return render_template("patient_reg.html")





@app.route('/delete_patient/<int:id>', methods = ['GET','POST'])
def delete_patient(id):

    delet = registration.query.get_or_404(id)
    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/viewpatient_for_labtec')
    except:
        return 'There was a problem deleting that task'


@app.route('/delete_Dr/<int:id>', methods = ['GET','POST'])
def delete_Dr(id):

    delet = registration.query.get_or_404(id)
    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/viewDr')
    except:
        return 'There was a problem deleting that task'


@app.route('/delete_labtec/<int:id>', methods = ['GET','POST'])
def delete_labtec(id):

    delet = registration.query.get_or_404(id)
    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/viewlabtec')
    except:
        return 'There was a problem deleting that task'        













@app.route('/editpatient_forlabtec/<int:id>',methods=["GET","POST"])
def editpatient_forlabtec(id):
    c= registration.query.get_or_404(id)
    if request.method == 'POST':
        c.name =  request.form['name']
        c.age =  request.form['age']
        c.gender =  request.form['gender']
        c.address =  request.form['address']
        c.email =  request.form['email']
        c.number =  request.form['number']
        
        db.session.commit()
        return redirect('/viewpatient_for_labtec')
    else:
        return render_template('editpatient_forlabtec.html',c=c)

        

@app.route('/editlabtec/<int:id>',methods=["GET","POST"])
def edit_labtec(id):
    c= registration.query.get_or_404(id)
    if request.method == 'POST':
        c.name =  request.form['name']
        # c.address =  request.form['address']
        c.email =  request.form['email']
        c.number =  request.form['number']
        c.Qualification =  request.form['Qualification']
        db.session.commit()
        return redirect('/viewlabtec')
    else:
        return render_template('editlabtec.html',c=c)   


@app.route('/editDr/<int:id>',methods=["GET","POST"])
def edit_Dr(id):
    c= registration.query.get_or_404(id)
    if request.method == 'POST':
        c.name =  request.form['name']
        # c.address =  request.form['address']
        c.email =  request.form['email']
        c.number =  request.form['number']
        c.Specialisation =  request.form['Specialisation']
        c.Qualification =  request.form['Qualification']

        db.session.commit()
        return redirect('/viewDr')
    else:
        return render_template('editDR.html',c=c)   


@app.route('/Dr_book_for_patient/<int:id>',methods=['GET','POST'])
def Dr_book_for_patient(id):

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        number = request.form['number']
        text = request.form['text']

        my_data = contact(name=name,email=email,number=number,text=text)
        db.session.add(my_data) 
        db.session.commit()
    return render_template("Dr_book_for_patient.html")










@app.route('/adminpage',methods=['GET','POST'])
def adminpage():
    return render_template("adminpage.html")

@app.route('/adminlayout',methods=['GET','POST'])
def adminpagelayout():
    return render_template("adminpagelayout.html")

@app.route('/labtecpage/<int:id>',methods=['GET','POST'])
def labtecpage(id):
    return render_template("labtecpage.html")

@app.route('/labteclayout',methods=['GET','POST'])
def labtecpagelayout():
    return render_template("labteclayout.html")
   

@app.route('/patientpage/<int:id>',methods=['GET','POST'])
def patientpage(id):
    return render_template("patientpage.html")

@app.route('/patientlayout',methods=['GET','POST'])
def patientpagelayout():
    return render_template("patientlayout.html")


@app.route('/Drpage/<int:id>',methods=['GET','POST'])
def Drpage(id):
    return render_template("Drpage.html")



@app.route('/approve_buk/<int:id>',methods=['GET','POST'])
def approve_buk(id):
    d=BookDoctor.query.filter_by(id=id).first()
    d.status="Approved"
    db.session.commit()
    for i in d.uid:
        app_sendmail(i.email)
    return redirect('/dr_buks')


@app.route('/reject_buk/<int:id>',methods=['GET','POST'])
def reject_buk(id):
    d=BookDoctor.query.filter_by(id=id).first()
    d.status="Rejected"
    db.session.commit()
    for i in d.uid:
        rej_sendmail(i.email)
    return redirect('/dr_buks')


@app.route('/Dr_layout',methods=['GET','POST'])
def Drlayout():
    return render_template("Dr_layout.html")


@app.route('/hd_reports',methods=['GET','POST'])
def hd_reports():
    
    obj=Test.query.filter_by(test_type="Diseases").join(registration.tes).filter(registration.id==current_user.id).all()
    return render_template("hd_reports.html",obj=obj)


@app.route('/sc_reports',methods=['GET','POST'])
def sc_reports():
    
    obj=Test.query.filter_by(test_type="Skin Cancer").join(registration.tes).filter(registration.id==current_user.id).all()
    return render_template("sc_reports.html",obj=obj)

@app.route('/ad_vw_tests',methods=['GET','POST'])
def ad_vw_tests():
    
    obj=Test.query.all()
    return render_template("ad_vw_tests.html",obj=obj)

@app.route('/pt_vw_test',methods=['GET','POST'])
def pt_vw_test():
    
    obj=Test.query.join(registration.tests).filter(registration.id==current_user.id).all()
    # obj=Test.query.all()
    return render_template("pt_vw_test.html",obj=obj)

@app.route('/my_queries',methods=['GET','POST'])
def my_queries():
    obj=Qresponses.query.join(registration.ques).filter(registration.id==current_user.id).all()
    return render_template("my_queries.html",obj=obj)

@app.route('/dr_vw_queries',methods=['GET','POST'])
def dr_vw_queries():
    obj=Qresponses.query.join(registration.queries).filter(registration.id==current_user.id).all()
    return render_template("dr_vw_queries.html",obj=obj)


@app.route('/us_buks',methods=['GET','POST'])
def us_buks():
    obj=BookDoctor.query.join(registration.buks).filter(registration.id==current_user.id).all()
    return render_template("us_buks.html",obj=obj)


@app.route('/dr_buks',methods=['GET','POST'])
def dr_buks():
    obj=BookDoctor.query.join(registration.books).filter(registration.id==current_user.id).all()
    return render_template("dr_buks.html",obj=obj)

@app.route('/buk_doctor/<id>',methods=['GET','POST'])
def buk_doctor(id):
    d=registration.query.filter_by(id=id).first()
    f=registration.query.filter_by(id=current_user.id).first()
    if request.method=="POST":
        date=request.form['date']
        time=request.form['time']
        my_data=BookDoctor(uid=[f],did=[d],date=date,time=time)
        db.session.add(my_data)
        db.session.commit()
        return redirect('/us_buks')
    return render_template("buk_doctor.html")


@app.route('/pt_vw_hd_report/<id>',methods=['GET','POST'])
def pt_vw_hd_report(id):
    t=Test.query.filter_by(id=id).first()
    return render_template("pt_vw_hd_report.html",t=t)

@app.route('/vw_hd_report/<id>',methods=['GET','POST'])
def vw_hd_report(id):
    t=Test.query.filter_by(id=id).first()
    return render_template("vw_hd_report.html",t=t)

@app.route('/ad_vw_hd_report/<id>',methods=['GET','POST'])
def ad_vw_hd_report(id):
    t=Test.query.filter_by(id=id).first()
    return render_template("ad_vw_hd_report.html",t=t)



@app.route('/heart_disease/<id>',methods=['GET','POST'])
def heart_disease(id):
    d=registration.query.filter_by(id=id).first()
    l=registration.query.filter_by(id=current_user.id).first()
    
    
    if request.method == 'POST':

    

        f = open('heart_prob/nb_classifier_selected_diseases.pickle', 'rb')
        classifier = pickle.load(f)
        f.close()
      

        dic = {
            "diarrhoea": [request.form['value1']],
            "chills": [request.form['value2']],
            "high_fever" : [request.form['value3']],
            "polyuria" : [request.form['value4']],
            "itching" : [request.form['value5']],
            "skin_rash" : [request.form['value6']],
            "nodal_skin_eruptions" : [request.form['value7']],
            "dehydration" : [request.form['value8']],
            "increased_appetite" : [request.form['value9']],
            "patches_in_throat" : [request.form['value10']]
        }
        dataFrame = pd.DataFrame(dic)
      

        prognosis = classifier.predict(dataFrame)
      
        
        OUTPUT=prognosis[0]
       



        model = pickle.load(open("heart_prob\model.pkl", "rb"))

        gender = request.form['gender']
        age = request.form['age']
        Tremor_of_one_hand = request.form['Tremor_of_one_hand']
        Rigidity = request.form['Rigidity']
        Clumsy_Leg = request.form['Clumsy_Leg']
        One_side_of_the_face_may_be_affect =request.form['One_side_of_the_face_may_be_affect']
        Loss_of_facial_expression = request.form['Loss_of_facial_expression']
        Decrease_blinking = request.form['Decrease_blinking']
        Speech_abnormalities = request.form['Speech_abnormalities']
        Balancing_problem = request.form['Balancing_problem']
        Fall_when_standing_or_turning = request.form['Fall_when_standing_or_turning']
        Freeze_or_stumble_when_walking = request.form['Freeze_or_stumble_when_walking']
        Hallucinations = request.form['Hallucinations']
        Loss_of_automatic_movements = request.form['Loss_of_automatic_movements']
        Writing_changes = request.form['Writing_changes']
        Need_assistance_for_walking = request.form['Need_assistance_for_walking']
        
        k=str(date.today())
       

        df1 = pd.DataFrame(data=[[gender,Tremor_of_one_hand,Rigidity,Clumsy_Leg,One_side_of_the_face_may_be_affect,Loss_of_facial_expression,Decrease_blinking,Speech_abnormalities,Balancing_problem,Fall_when_standing_or_turning,
                          Freeze_or_stumble_when_walking,Hallucinations,Loss_of_automatic_movements,Writing_changes,Need_assistance_for_walking,age]],columns=['Gender', 'Tremor of one hand', 'Rigidity', 'Clumsy Leg', 'One side of the face may be affect',
                                                                                            'Loss of facial expression', 'Decrease blinking', 'Speech abnormalities', 'Balancing problem', 
                                                                                            'Fall when standing or turning', 'Freeze or stumble when walking', 'Hallucinations', 'Loss of automatic movements', 
                                                                                            'Writing changes', 'Need assistance for walking', 'Age'])
        
        
  
        
        

        mildlist=[Tremor_of_one_hand,Rigidity,Clumsy_Leg,One_side_of_the_face_may_be_affect,Loss_of_facial_expression,
                Decrease_blinking,Speech_abnormalities]
        moderatelist = [Balancing_problem,Loss_of_automatic_movements]
        severelist = [Fall_when_standing_or_turning,Freeze_or_stumble_when_walking,Hallucinations,Writing_changes,Need_assistance_for_walking]

        type1count = 0
        for i in mildlist:
            if (i == 'yes') or (i == 'y'):
                type1count = type1count +1
        type2count = 0
        for i in moderatelist:
            if (i == 'yes') or (i == 'y'):
                type2count = type2count +1
                
        type3count = 0
        for i in severelist:
            if (i == 'yes') or (i == 'y'):
                type3count = type3count +1


        prediction = model.predict(df1)[0]
        if prediction == 1:
            pred1 = "Parkinson Detected"
            if type1count >= 1:
                if type2count >= 1 :
                    if type3count >= 2 :
                        stage = "severe"
                    else:
                        stage = "moderate"
                else:
                    stage = "mild"
            else:
                stage = "mild"
                
        elif prediction == 0:
            pred1 = "Negative"
            stage = "None"

       


        models = pickle.load(open("naive_bayes_model.pkl", "rb"))

        age = int(request.form['age'])
        gender = int(request.form['gender'])
        thal = int(request.form['thal'])
        cp = int(request.form['cp'])
        trestbps = int(request.form['trestbps'])
        chol = int(request.form['chol'])
        fbs = int(request.form['fbs'])
        restecg = int(request.form['restecg'])
        thalach = int(request.form['thalach'])
        exang = int(request.form['exang'])
        oldpeak = float(request.form['oldpeak'])
        slope = int(request.form['slope'])
        ca = int(request.form['ca'])


        
        
        cp_1 = 0
        cp_2 = 0
        cp_3 = 0
        cp_4 = 0
        
        thal_3 = 0
        thal_6 = 0
        thal_7 = 0
        
        slope_1 = 0
        slope_2 = 0
        slope_3 = 0
        
        
        if cp == 1:
            cp_1 = 1
        elif cp ==2:
            cp_2 =1
        elif cp == 3:
            cp_3 = 1
        elif cp ==4:
            cp_4 =1
            
        if thal == 3:
            thal_3 = 1
        elif thal == 6:
            thal_6 =1
        elif thal == 7:
            thal_7 =1
            
        if slope == 1:
            slope_1 = 1
        elif slope == 2:
            slope_2 =1
        elif slope ==3:
            slope_3 = 1




        df1 = pd.DataFrame(data=[[age,gender,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,ca,cp_1,cp_2,cp_3,cp_4,thal_3,thal_6,thal_7,
                            slope_1,slope_2,slope_3]],columns=['age', 'sex','trestbps', 'chol','fbs', 'restecg', 'thalach', 'exang', 
                'oldpeak', 'ca', 'cp_1','cp_2','cp_3','cp_4','thal_3.0','thal_6.0','thal_7.0','slope_1','slope_2','slope_3' ])

    


        prediction = models.predict(df1)[0]
        if prediction == 1:
            pred = "Heart Disease Detected"

        elif prediction == 0:
            pred = "No Heart Disease Detected"

        


        now = datetime.now()
        current_time = now.strftime("%H:%M%p")
        my_data = Test(uid=[d],lid=[l],date=date.today(),time=current_time,cp=pred1,trestbps=stage,chol=OUTPUT,pred=pred,test_type="Diseases")
        db.session.add(my_data) 
        db.session.commit()
        return render_template('result.html',pred=pred,output=OUTPUT,pred1=pred1,stage=stage)
        
      



    return render_template("heart_disease.html")










@app.route('/login', methods=["GET","POST"])
def login():

   
    if request.method=="POST":


        username=request.form['email']
        password=request.form['password']
        admin = registration.query.filter_by(email=username, password=password,usertype='admin').first()

         
        labtec=registration.query.filter_by(email=username,password=password, usertype='labtec').first()
         
        patient=registration.query.filter_by(email=username,password=password, usertype='patient').first()

        Dr=registration.query.filter_by(email=username,password=password, usertype='Dr').first()

        if admin:
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/adminpage') 
         
        elif labtec:
            login_user(labtec)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/labtecpage/'+str(labtec.id)) 

        elif patient:

            login_user(patient)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/patientpage/'+str(patient.id)) 

        elif Dr:

            login_user(Dr)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/Drpage/'+str(Dr.id))          

        else:

            d="Invalid Username or Password!"
            return render_template("login.html",d=d)
    return render_template("login.html")



@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')









