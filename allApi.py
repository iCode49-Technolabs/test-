import re
import os
import json
from datetime import datetime
from flaskext.mysql import MySQL
from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from flask import request
from flask_cors import CORS
import mysql.connector
from commonUtils.commonUtils import create_json , param_verfication
from datetime import datetime
import random
import array
import logging
LOGGER = logging.getLogger(__name__)

api = ''
app = Flask(__name__)
api = Api(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'tollow'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql = MySQL(app)
codes = {'info': 'info', 
        'success': '200', 
        'invalid request': '400', 
        'missing environment variables': '400', 
        'configuration file missing': '400', 
        'internal error': '500', 
        'connection error': '501', 
        'database error': '502', 
        'incorrect Parameters': '401', 
        'directory missing' : '400', 
        'invalid method':'405', 
        'no Write Permission': '400', 
        'no records': '404'}


        
class studentDetails(Resource):
    def post(self):
        request_json = request.get_json()
        print("yes")
        request_verification = param_verfication(request_json, ['school','learning_coordinator'])
        if codes[request_verification] != '200':
            
            return create_json('invalid request', "invalid request")


        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select 
                            first_name
                          , last_name
                          , class_year
                          , iep
                          , user_id
                          , created_date
                          , disability_category
                          , email
                        from tollow.assessment_request
                        where user_id In ( select user_id from 
                        tollow.user_info where school_name=%s)
                        and learning_coordinator=%s''',
                        (request_json['school']
                        ,request_json['learning_coordinator'])
                       )
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        print(record)
        record_list=[]
        if not record or record[0] == 0:
            return create_json('no records', "no records found")
        for record in record:
            record_dict = {}
            for key, val in record.items():
                print(val)
                if key == 'created_date':
                    record_dict[key] = val.strftime("%d-%m-%Y")
                else:
                    record_dict[key] = val
            record_list.append(record_dict)
        print (record_list)
        result = create_json('success', record_list)
        return result


class createCategoryOfConcern(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name'
                        ,'category_of_concerns'
                        ,'subcategory_of_concerns'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
        
            school_check = cursor.fetchone()
            cursor.execute('''SELECT COUNT(*)
                                FROM category_of_concerns
                                WHERE category_of_concerns = %s and school_name = %s  and subcategory_of_concerns=%s''',(request_json['category_of_concerns'], request_json['school_name'], request_json["subcategory_of_concerns"]))
        
            category_of_concerns_check = cursor.fetchone()  
            print(category_of_concerns_check)          
            if school_check[0] == 1 and category_of_concerns_check[0] == 0:
                cursor.execute(''' INSERT INTO category_of_concerns(category_of_concerns, subcategory_of_concerns, school_name)
                                    VALUES (%s, %s, %s)''',  (request_json['category_of_concerns'], request_json["subcategory_of_concerns"], request_json["school_name"])
                                        )  
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from category_of_concerns
                                    where category_of_concerns = %s  and subcategory_of_concerns = %s and school_name = %s ''',(request_json['category_of_concerns'], request_json['subcategory_of_concerns'], request_json['school_name']))
                record = cursor.fetchone()
                print(record, 'Cheril')
                if record[0] == 1:             
                    return create_json('success', "Category Of Concern is Created.")
                else:
                    return create_json('internal error', "internal error")
            else:
                return create_json('internal error', "internal error")
          
        except Exception as error:
            print(error)

class editCategoryOfConcern(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name'
                        ,'category_of_concerns'
                        , 'subcategory_of_concerns'
                        ,'category_id'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
        
            school_check = cursor.fetchone()
            cursor.execute('''SELECT COUNT(*)
                                FROM category_of_concerns
                                WHERE category_id = %s ''',(request_json['category_id']))
        
            category_of_concerns_check = cursor.fetchone()
            print(category_of_concerns_check)
            if school_check[0] == 1 and category_of_concerns_check[0] == 1:
                cursor.execute(''' update category_of_concerns 
                                    set category_of_concerns = %s, subcategory_of_concerns = %s
                                    where category_id = %s ''',  (request_json['category_of_concerns'], request_json['subcategory_of_concerns'], request_json['category_id'])
                                        )  
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from category_of_concerns
                                    where category_of_concerns = %s and category_id = %s''',(request_json['category_of_concerns'], request_json['category_id']))
                record = cursor.fetchone()
                print(record, 'Cjeri')
                if record[0] == 1:             
                    return create_json('success', "Category Of Concern is Updated successfully.")
                else:
                    return create_json('internal error', "internal error")
            else:
                return create_json('internal error', "internal error")
        except Exception as error:
            print(error)

class viewCategoryOfConcern(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT *
                                FROM category_of_concerns
                                WHERE school_name = %s ''',(request_json['school_name']))
        
            # view_category_of_concern = cursor.fetchall()
            view_category_of_concern = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            if view_category_of_concern :
                return create_json('success', view_category_of_concern)
            else:
                return create_json('internal error', "Data is not Found.")
            

        except Exception as error:
            print(error)

class deleteCategoryOfConcern(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['category_of_concerns'
                        , 'subcategory_of_concerns'
                        ,'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM category_of_concerns
                                WHERE category_of_concerns = %s and school_name = %s and subcategory_of_concerns = %s ''',(request_json['category_of_concerns'], request_json['school_name'], request_json['subcategory_of_concerns']))
        
            check_category_of_concern = cursor.fetchone()
            print(check_category_of_concern)
            if check_category_of_concern[0] == 1:
                cursor.execute('''DELETE FROM category_of_concerns 
                                    WHERE category_of_concerns = %s AND subcategory_of_concerns = %s ''',(request_json['category_of_concerns'], request_json['subcategory_of_concerns']))
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from category_of_concerns
                                    where category_of_concerns = %s and subcategory_of_concerns= %s ''',(request_json['category_of_concerns'], request_json['subcategory_of_concerns']))
                record = cursor.fetchone()
                if record[0] == 0:             
                    return create_json('success', "Category Of Concern " + request_json['category_of_concerns'] + " is deleted.")
                else:
                    return create_json('internal error', "internal error")
            else:
                return create_json('internal error', "internal error")
        
            
        except Exception as error:
            print(error)





class createStudentViewReview(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'review_date'
                        , 'revisit_goal'
                        , 'assessment_result' 
                        , 'examples' 
                        , 'achieve_goals'
                        , 'any_conserns' 
                        , 'teachers_can_do_additionally'
                        , 'school'
                        ]
        
        today_date = date.today()
        review_date = request_json['review_date']
        review_date_object = datetime.strptime(review_date, '%Y-%m-%d').date()
        

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])



            cursor.execute('''SELECT adjustment_review_schedule, created_date
                            FROM iep_step_3
                            WHERE email = %s AND school_name = %s ''',(request_json['email'], request_json['school']))
        
            frequency = cursor.fetchone()
            print(frequency)
            if frequency[0].lower() == 'daily':
                current_date_step3 = frequency[1]
                new_review_date = current_date_step3 + timedelta(days=1)
                view_review_status_date = current_date_step3 + timedelta(days=0)

            elif frequency[0].lower() == 'every other day':
                current_date_step3 = frequency[1]
                new_review_date = current_date_step3 + timedelta(days=2)
                view_review_status_date = current_date_step3 + timedelta(days=1)

            elif frequency[0].lower()== 'weekly':
                current_date_step3 = frequency[1]
                new_review_date = current_date_step3 + timedelta(days=7)
                view_review_status_date = current_date_step3 + timedelta(days=3)
                print(new_review_date)
            elif frequency[0].lower() == 'fortnightly':
                current_date_step3 = frequency[1]
                new_review_date = current_date_step3 + timedelta(days=14)
                view_review_status_date = current_date_step3 + timedelta(days=7)
                print(new_review_date)
            elif frequency[0].lower() == 'once a month':
                current_date_step3 = frequency[1]
                new_review_date = current_date_step3 + timedelta(days=30)
                view_review_status_date = current_date_step3 + timedelta(days=15)

            cursor.execute('''SELECT COUNT(*)
                                FROM iep_step_3
                                WHERE duration_start_date < (SELECT CURDATE()) AND (SELECT CURDATE()) < duration_end_date AND email = %s; ''',(request_json['email']))      
            duration_email = cursor.fetchone()
            if duration_email[0] == 1 :
                cursor.execute('''UPDATE `student_view_review_iep` 
                                    SET `review_status`='Upcoming Review'
                                    WHERE view_review_status_date = (SELECT CURDATE());''')
                conn.commit()                
                cursor.execute('''UPDATE `student_view_review_iep` 
                                    SET `review_status`='Overdue Review'
                                    WHERE review_date < (SELECT CURDATE()) AND revisit_goal = '';''')
                conn.commit()
                cursor.execute('''SELECT COUNT(*) 
                                    FROM `iep_step_3` 
                                    WHERE email = %s AND school_name = %s ''',(request_json['email'], request_json['school']))
            
                get_id = cursor.fetchone()
                print(get_id)

                if get_id[0] == 1:
                    if review_date_object == today_date:
                        cursor.execute('''UPDATE student_view_review_iep
                                            SET revisit_goal=%s, 
                                                assessment_result=%s, 
                                                examples=%s, 
                                                achieve_goals=%s, 
                                                any_conserns=%s, 
                                                teachers_can_do_additionally=%s
                                            WHERE email = %s AND review_date = %s ''',
                                            ( request_json['revisit_goal'], 
                                            request_json['assessment_result'],
                                            request_json['examples'],
                                            request_json['achieve_goals'],
                                            request_json['any_conserns'],
                                            request_json['teachers_can_do_additionally'],
                                            request_json['email'], 
                                            request_json['review_date']))
                        conn.commit()
                        cursor.execute('''SELECT revisit_goal
                                            FROM student_view_review_iep
                                            WHERE email = %s AND review_date = %s ''',(request_json['email'], review_date))
                        revisit_goal = cursor.fetchone()
                        if revisit_goal[0] != '':
                            cursor.execute('''UPDATE student_view_review_iep
                                                SET review_status ='Done' 
                                                WHERE email = %s AND review_date = %s ''',(request_json['email'], request_json['review_date']))
                            conn.commit()

                            cursor.execute('''SELECT COUNT(*)
                                                FROM iep_step_3
                                                WHERE duration_start_date < (SELECT CURDATE()) AND (SELECT CURDATE()) < duration_end_date AND email = %s; ''',(request_json['email']))      
                            duration_email = cursor.fetchone()

                            if duration_email[0] == 1 :
                                cursor.execute(''' INSERT INTO student_view_review_iep(email,school_name, review_status, review_date, view_review_status_date, created_date)
                                                    VALUES(%s, %s, 'Review In Process', %s, %s, %s)''',  (request_json["email"], request_json["school"], str(new_review_date), str(view_review_status_date),str(today_date) )
                                                )  
                                conn.commit()

                            cursor.execute('''SELECT COUNT(*)
                                                FROM student_view_review_iep
                                                WHERE email = %s AND review_date = %s AND review_status ='Done' ''',(request_json['email'], request_json['review_date']))
                            record = cursor.fetchone()
                            if record[0] != 0:
                                return create_json('success', "Student review IEP is Done.")
                            else:
                                return create_json('internal error', "internal error") 
                    elif review_date_object < today_date:
                        pass

            else:
                cursor.execute('''UPDATE `student_view_review_iep` 
                                        SET `review_status`='Close IEP'
                                        WHERE user_id = (SELECT MAX(user_id)
                                                        FROM student_view_review_iep
                                                        WHERE email= %s )''' ,(request_json['email']))
                conn.commit()
                return create_json('success', "Student review IEP is Closed Now.")
                
        except Exception as error:
            print(error)



class forgetPassword(Resource):
    @app.route("/", methods=["POST"])
    def post(self):
        request_json = request.get_json()

        if request_json and 'username' not in request_json:
            return {'Status' : 'Invalid Request for username'}

        

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select count(*) from tollow.user_info where email=%s ''',
                       (request_json['username']))
        record = cursor.fetchone()

        if record[0] == 0:
            return {'Status': 'Invalid User Name '}
        elif record[0] != 0:
            passd = generatePassword()
            cursor.execute(''' update tollow.user_info set password = %s where email = %s 
                                                        ''', (passd, request_json["username"]))
            conn.commit()
            
            return {"Status" : 'Email sent'}
            
        elif not record[0]:
            return {"Status" : 'Invalid Request'}

def generatePassword():
    
    max_len = 12
    digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    lower_case_characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                         'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                         'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                         'z']
    
    upper_case_characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H',
                         'I', 'J', 'K', 'M', 'N', 'O', 'P', 'Q',
                         'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y',
                         'Z']
    
    symbols = ['@', '#', '$', '%', '=', ':', '?', '.', '/', '|', '~', '>',
               '*', '(', ')', '<']
    
    combined_list = digits + upper_case_characters + lower_case_characters + symbols
    
    rand_digit = random.choice(digits)
    rand_upper = random.choice(upper_case_characters)
    rand_lower = random.choice(lower_case_characters)
    rand_symbol = random.choice(symbols)
    
    temp_pass = rand_digit + rand_upper + rand_lower + rand_symbol
    
    for x in range(max_len - 4):
        temp_pass = temp_pass + random.choice(combined_list)
    
        temp_pass_list = array.array('u', temp_pass)
        random.shuffle(temp_pass_list)

    password = ""
    for x in temp_pass_list:
        password = password + x
    
    return password






class iepStep2(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['schools'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")


        conn = mysql.connect()
        cursor = conn.cursor()
        mysql_query = '''Select * from tollow.iep_assessment_type'''
        cursor.execute(mysql_query)
        LOGGER.info(mysql_query)
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        print (record)
        if not record:
            LOGGER.info("No records Found")
            return create_json('no records', "no records found")
           
       
        
        result = create_json('success', record)
       
        conn.close()
        return result

class roleDisplaySupportStaff(Resource):
    def post(self):
        request_json = request.get_json()

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select first_name,last_name,email
                            from tollow.user_info 
                            where role = %s and school_name = %s and active = %s ''', ( request_json['role'], request_json['schools'], request_json['active']))
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  cursor.fetchall()]
        if not record:
            return create_json('invalid request', "no records found")
        record_list = []
        result = create_json('success', record)
        return result

class preInformation(Resource):
    def post(self):
        request_json = request.get_json()

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            insert_sql = '''INSERT INTO tollow.iep_step_2 (
                                    subject_requiring_adjustment
                                   , support_staff_member
                                   , learning_or_social_difficulties
                                   , learning_or_social_difficulties_details
                                   , assessment_type
                                   , medical_or_wellbeing_issues
                                   , student_regular_school
                                   , student_regular_school_details
                                   , lc_email
                                   , email
                                   , school_name
                                   
                                   ) 
                                   VAlUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
            data = (
                                     request_json["subject_requiring_adjustment"]
                                    , request_json["support_staff_member"]
                                    , request_json["learning_or_social_difficulties"]
                                    , request_json["learning_or_social_difficulties_details"]
                                    , request_json["assessment_type"]
                                    , request_json["medical_or_wellbeing_issues"]
                                    , request_json["student_regular_school"]
                                    , request_json["student_regular_school_details"]
                                    , request_json["lc_email"]
                                    , request_json["email"]
                                    , request_json["school_name"]
                                   
                                    )


            cursor.execute(insert_sql, data)
            conn.commit()
            
            select_sql ='''Select count(*) from tollow.iep_step_2
                                where email = %s and school_name = %s
                                and support_staff_member = %s
                                
                                and subject_requiring_adjustment = %s
                                and learning_or_social_difficulties = %s
                                and learning_or_social_difficulties_details = %s
                                and medical_or_wellbeing_issues = %s
                                and student_regular_school = %s
                                and student_regular_school_details = %s
                                and lc_email = %s'''

            values = (request_json['email']
                    , request_json["school_name"]
                    , request_json["support_staff_member"]
                    , request_json["subject_requiring_adjustment"]
                    , request_json["learning_or_social_difficulties"]
                    , request_json["learning_or_social_difficulties_details"]
                    , request_json["medical_or_wellbeing_issues"]
                    , request_json["student_regular_school"]
                    , request_json["student_regular_school_details"]
                    , request_json["lc_email"]
            )
            cursor.execute(select_sql,values)

            record = cursor.fetchone()
           

            if not record and record[0] == 0:
                return create_json('internal error', "internal error")
           
            return create_json('success', "Student IEP Registered")
       
        except Exception as error:
            print(error)
        finally:
            conn.close()






class CreateIEPstep3(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school'
                        , 'transitions'
                        , 'assesment_adjustment'
                        , 'examination_adjustments'
                        , 'duration_start_date'
                        , 'duration_end_date'
                        , 'adjustment_review_schedule'
                        , 'student_discussion_schedule' 
                        , 'career_discussion_schedule' 
                        , 'lc_email'
                        , 'key_outcome_id'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            ##### Check Student
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE role = 'Student' and email = %s and school_name = %s ''',(request_json['email'], request_json['school']))
        
            student_check = cursor.fetchone()
            print(student_check)
            
            ##### Check Coordinator
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE role = 'Coordinator' and email = %s and school_name = %s ''',(request_json['lc_email'], request_json['school']))
        
            coordinator_check = cursor.fetchone()
            print(coordinator_check)
            ##### Check Teacher 
            # cursor.execute('''SELECT COUNT(*)
            #                     FROM user_info
            #                     WHERE role = 'Teacher' and email = %s and school_name = %s ''',(request_json['tag_teachers'], request_json['school']))
        
            # teacher_check = cursor.fetchone()
            #### Get step3 key outcome id
            # cursor.execute('''SELECT key_outcome_id 
            #                     from step3_key_outcome
            #                     WHERE email = %s AND school_name = %s  ''',(request_json['email'], request_json['school']))
        
            # keyoutcome_id_get = cursor.fetchall()
            # ##### Store all the key id in list
            # keyoutcome_id = []
            # for key in keyoutcome_id_get:
            #     keyoutcome_id.append(key[0]) 
            
            # key_outcome = keyoutcome_id
            # print(key_outcome,'Cheril Gandhi')[[123],[2,3]]

            if student_check[0] == 1 and coordinator_check[0] == 1:
                
                cursor.execute('''INSERT INTO iep_step_3 (email, school_name, transitions, assesment_adjustment,examination_adjustments, duration_start_date, duration_end_date, adjustment_review_schedule, student_discussion_schedule, career_discussion_schedule, lc_email, key_outcome_id)    
                                VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ''',
                                    (request_json['email'], 
                                    request_json['school'],
                                    str(request_json['transitions']),
                                    str(request_json['assesment_adjustment']),
                                    str(request_json['examination_adjustments']),
                                    str(request_json['duration_start_date']),
                                    str(request_json['duration_end_date']),
                                    str(request_json['adjustment_review_schedule']),
                                    str(request_json['student_discussion_schedule']),
                                    str(request_json['career_discussion_schedule']),
                                    request_json['lc_email'], str(request_json['key_outcome_id']))
                                )
                conn.commit()
                print(True)
                cursor.execute('''SELECT COUNT(*)
                                    FROM iep_step_3
                                    WHERE email = %s AND school_name = %s AND lc_email = %s''',(request_json['email'], request_json['school'], request_json['lc_email']))
                record = cursor.fetchone()
                print(record)
                if record[0] != 0:             
                    return create_json('success', "IEP Step 3 is Created Successfully.")
                else:   
                    return create_json('internal error', "internal error") 
                 
        except Exception as error:
            print(error)



class viewIEPStep2(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school'
                        ,'email']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT *
                                FROM iep_step_2
                                WHERE school_name = %s  and email = %s ''',(request_json['school'], request_json['email']))
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            list_of_record = []

            for record in records:
                record_dict = {}
                if record:
                    for key, val in record.items():
                        if key == 'created_date' and type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = val
                    list_of_record.append(record_dict)
            result = create_json('success', list_of_record)   
            return result

        except Exception as error:
            print(error)

###PLAYLOAD
# {
#     "email" : "Ashley.Williams@test.com",
#     "school" : "School A"
# }




class updateIEPStep2(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['iep_id'
                        , 'email'
                        , 'school_name'
                        , 'support_staff_member'
                        , 'subject_requiring_adjustment'
                        , 'learning_or_social_difficulties'
                        , 'learning_or_social_difficulties_details'
                        , 'assessment_type'
                        , 'medical_or_wellbeing_issues'
                        , 'student_regular_school'
                        , 'student_regular_school_details'
                        , 'lc_email']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM iep_step_2
                                WHERE iep_id = %s and email = %s and school_name = %s ''',(request_json['iep_id'], request_json['email'], request_json['school_name']))
            iep_id_check= cursor.fetchall()
            print(iep_id_check)
            if iep_id_check[0] != 0:
                cursor.execute(''' update iep_step_2 
                                    set support_staff_member = %s, 
                                        subject_requiring_adjustment = %s, 
                                        learning_or_social_difficulties = %s, 
                                        learning_or_social_difficulties_details = %s, 
                                        assessment_type = %s, 
                                        medical_or_wellbeing_issues = %s, 
                                        student_regular_school = %s, 
                                        student_regular_school_details = %s, 
                                        lc_email = %s
                                    where iep_id = %s ''',  (
                                        request_json['support_staff_member'], 
                                        request_json['subject_requiring_adjustment'],  
                                        request_json['learning_or_social_difficulties'],  
                                        request_json['learning_or_social_difficulties_details'],  
                                        request_json['assessment_type'],  
                                        request_json['medical_or_wellbeing_issues'],  
                                        request_json['student_regular_school'],  
                                        request_json['student_regular_school_details'],  
                                        request_json['lc_email'], 
                                        request_json['iep_id'])
                                )  
                conn.commit()
                cursor.execute('''Select count(*) 
                                        from iep_step_2 
                                        where support_staff_member = %s and
                                                subject_requiring_adjustment = %s and
                                                learning_or_social_difficulties = %s and 
                                                learning_or_social_difficulties_details = %s and 
                                                assessment_type = %s and 
                                                medical_or_wellbeing_issues = %s and 
                                                student_regular_school = %s and 
                                                student_regular_school_details = %s and 
                                                lc_email = %s and iep_id = %s ''',
                                                (request_json['support_staff_member'], 
                                                request_json['subject_requiring_adjustment'],  
                                                request_json['learning_or_social_difficulties'],  
                                                request_json['learning_or_social_difficulties_details'],  
                                                request_json['assessment_type'],  
                                                request_json['medical_or_wellbeing_issues'],  
                                                request_json['student_regular_school'],  
                                                request_json['student_regular_school_details'],  
                                                request_json['lc_email'], 
                                                request_json['iep_id']))
                record = cursor.fetchone()
                if record[0] == 1:             
                    return create_json('success', "IEP step 2 Updated Successfully.")
                else:
                    return create_json('internal error', "internal error")
            
        except Exception as error:
            print(error)








class viewIEPStep3(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school'
                        ,'email']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            print("result123")
            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT *
                                FROM iep_step_3
                                WHERE school_name = %s  and email = %s ''',( request_json['school'],request_json['email']))
            
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            list_of_record = []
            print("result12")
            if not records:
                
                return create_json('no records', "no records")

            for record in records:
                record_dict = {}
                if record:
                    for key, val in record.items():
                        if (key == 'created_date' or key == 'duration_start_date' or key == 'duration_end_date') and type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            
                            record_dict[key] = eval(str(val)) if (val and str(val)[0]=="[") else val
                    list_of_record.append(record_dict)
            result = create_json('success', list_of_record)
            print("result1")
            return result
            
        except Exception as error:
            
            print(error)
###PLAYLOAD
# {
#     "email" : "Ashley.Williams@test.com",
#     "school" : "School A"
# }


class updateIEPStep3(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['iep_id_3'
                        , 'email'
                        , 'school_name'
                        , 'transitions'
                        , 'assesment_adjustment'
                        , 'examination_adjustments'
                        , 'duration_start_date'
                        , 'duration_end_date'
                        , 'adjustment_review_schedule'
                        , 'student_discussion_schedule' 
                        , 'career_discussion_schedule' 
                        , 'lc_email']
        print(request_json)
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM iep_step_3
                                WHERE iep_id_3 = %s and email = %s and school_name = %s ''',(request_json['iep_id_3'], request_json['email'], request_json['school_name']))
            iep_id_check= cursor.fetchall()

            cursor.execute('''SELECT key_outcome_id 
                                from step3_key_outcome
                                WHERE email = %s AND school_name = %s  ''',(request_json['email'], request_json['school_name']))
        
            keyoutcome_id_get = cursor.fetchall()
            ##### Store all the key id in list
            keyoutcome_id = []
            for key in keyoutcome_id_get:
                keyoutcome_id.append(key[0]) 
            
            key_outcome = keyoutcome_id

            print(iep_id_check)
            if iep_id_check[0] != 0:
                cursor.execute(''' update iep_step_3 
                                    set transitions = %s, 
                                        assesment_adjustment = %s,
                                        examination_adjustments = %s, 
                                        duration_start_date = %s, 
                                        duration_end_date = %s, 
                                        adjustment_review_schedule = %s, 
                                        student_discussion_schedule = %s, 
                                        career_discussion_schedule = %s, 
                                        lc_email = %s, 
                                        key_outcome_id = %s
                                    where iep_id_3 = %s ''',  (
                                    str(request_json['transitions']),
                                    str(request_json['assesment_adjustment']),
                                    str(request_json['examination_adjustments']),
                                    str(request_json['duration_start_date']),
                                    str(request_json['duration_end_date']),
                                    str(request_json['adjustment_review_schedule']),
                                    str(request_json['student_discussion_schedule']),
                                    str(request_json['career_discussion_schedule']),
                                    request_json['lc_email'], 
                                    str(key_outcome), 
                                    request_json['iep_id_3'])
                                )  
                conn.commit()
                cursor.execute('''Select count(*) 
                                        from iep_step_3
                                        where transitions = %s and 
                                            assesment_adjustment = %s and
                                            examination_adjustments = %s and 
                                            duration_start_date = %s and 
                                            duration_end_date = %s and 
                                            adjustment_review_schedule = %s and 
                                            student_discussion_schedule = %s and 
                                            career_discussion_schedule = %s and 
                                            lc_email = %s and 
                                            key_outcome_id = %s and 
                                            iep_id_3 = %s ''',
                                                (request_json['transitions'],
                                                    request_json['assesment_adjustment'],
                                                    request_json['examination_adjustments'],
                                                    request_json['duration_start_date'],
                                                    request_json['duration_end_date'],
                                                    request_json['adjustment_review_schedule'],
                                                    request_json['student_discussion_schedule'],
                                                    request_json['career_discussion_schedule'],
                                                    request_json['lc_email'], 
                                                    str(key_outcome), 
                                                    request_json['iep_id_3']))
                record = cursor.fetchone()
                if record[0] == 1:             
                    return create_json('success', "IEP step 3 Updated Successfully.")
                else:
                    return create_json('internal error', "internal error")
            
        except Exception as error:
            print(error)

      
class teacherNames(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['school'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")


        conn = mysql.connect()
        cursor = conn.cursor()
        mysql_query = '''Select first_name, last_name, email from tollow.user_info as info where info.school_name = %s and info.role="Teacher"'''
        cursor.execute(mysql_query,(request_json['school']))
        LOGGER.info(mysql_query)
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
       
        if not record:
            LOGGER.info("No records Found")
            return create_json('no records', "no records found")
           
       
        print (record)
        result = create_json('success', record)
       
        conn.close()
        return result

class teacherTagging(Resource):
    def post(self):
        request_json = request.get_json()
        request_verification = param_verfication(request_json, ['email','teachers','view'])
       
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")
       
        conn = mysql.connect()
        cursor = conn.cursor()
        #teachers=[]
        #teachers = request_json['teachers'].split(",")
       
       
        update_sql = '''UPDATE tollow.''' + request_json["view"] + '''_view_inform_iep SET tag_teacher="%s" WHERE tollow.student_view_inform_iep.email = "%s" ;''' % ( request_json['teachers'],request_json['email'] )
        cursor.execute(update_sql)
        conn.commit()

        cursor.execute("Select count(*) from tollow.student_view_inform_iep where email = %s", request_json['email'])
        record = cursor.fetchone()
        if not record and record[0] == 0:
            conn.close()
            return create_json('internal error', "internal error")
       
        conn.close()
        return create_json('success', "Teachers Tagged")
       
   
class studentvoiceupdate(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['user_id',
                         'email',
                         'school_name',
                         'view',
                         'assessment_results',
                         'barriers_learning',
                         'review_learning_style',
                         'review_strength',
                         'review_interest',
                         'review_limiting_belief',
                         'review_enabling_belief',
                         'soft_name',
                         'soft_skill',
                         'negotiate_goal',
                         'how_goals_can_be_achieved',
                         'any_concerns',
                         'teachers_can_do_additionally',
                         'question',
                         'answer',
                         'created_date'
                         ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            mandate_param.append('created_date')
            mandata_param_value.append(str(datetime.now()))
                       
            query_value = ', '.join(['%s'] * len(mandata_param_value))

            columns = ', '.join(mandate_param)
           
            cursor.execute('''Select count(*) from tollow.'''+request_json['view']+'''_view_inform_iep
                                
                                WHERE email = %s and school_name = %s and created_date = %s''',(request_json['email'], 
                                                                                                request_json['school_name'],
                                                                                                request_json['created_date']))
            check_data = cursor.fetchall()
            print(check_data[0][0])
            if check_data[0][0] == 0:
                print(True)
                cursor.execute('''INSERT INTO tollow.'''+ request_json['view'] +'''_view_inform_iep(email,school_name,assessment_results,barriers_learning,review_learning_style,
                                                                                                    review_strength,review_interest,review_limiting_belief,review_enabling_belief,
                                                                                                    soft_name,soft_skill,negotiate_goal,how_goals_can_be_achieved,any_concerns,
                                                                                                    teachers_can_do_additionally,question,answer,created_date)
                                      VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ''',
                                        (request_json["email"]
                                        , request_json["school_name"]
                        
                                        , request_json["assessment_results"]
                                        , request_json["barriers_learning"]
                                        , request_json["review_learning_style"]
                                        , request_json["review_strength"]
                                        , request_json["review_interest"]
                                        , request_json["review_limiting_belief"]
                                        , request_json["review_enabling_belief"]
                                        , str(request_json["soft_name"])
                                        , str(request_json["soft_skill"])
                                        , str(request_json["negotiate_goal"])
                                        , str(request_json["how_goals_can_be_achieved"])
                                        , str(request_json["any_concerns"])
                                        , str(request_json["teachers_can_do_additionally"])
                                        , request_json["question"]
                                        , request_json["answer"],
                                                                                                request_json['created_date']
                                        ))
                conn.commit()
                print('1')
                cursor.execute('''Select count(*) from tollow.'''+request_json['view']+'''_view_inform_iep
                                
                                WHERE email = %s and school_name = %s and assessment_results = %s''',(request_json['email'], 
                                                                                                request_json['school_name'],
                                                                                                request_json['assessment_results']))
                record = cursor.fetchall()
                if record[0] != 0:
                    return create_json('success', "Know Your Student Registered")
                else:
                    return create_json('internal error', "internal error")
            
            else:
                update_sql = '''UPDATE tollow.''' + request_json["view"] + '''_view_inform_iep set
                                    assessment_results = %s
                                   , barriers_learning = %s
                                   , review_learning_style = %s
                                   , review_strength = %s
                                   , review_interest = %s
                                   , review_limiting_belief = %s
                                   , review_enabling_belief = %s
                                   , soft_name = %s
                                   , soft_skill = %s
                                   , negotiate_goal = %s
                                   , how_goals_can_be_achieved = %s
                                   , any_concerns = %s
                                   , teachers_can_do_additionally = %s
                                   , question = %s
                                   , answer = %s
                                   where email = %s and school_name = %s and created_date = %s
                                   '''
                values = (
                    request_json["assessment_results"]
                    , request_json["barriers_learning"]
                    , request_json["review_learning_style"]
                    , request_json["review_strength"]
                    , request_json["review_interest"]
                    , request_json["review_limiting_belief"]
                    , request_json["review_enabling_belief"]
                    , str(request_json["soft_name"])
                                        , str(request_json["soft_skill"])
                    , str(request_json["negotiate_goal"])
                    , str(request_json["how_goals_can_be_achieved"])
                    , str(request_json["any_concerns"])
                    , str(request_json["teachers_can_do_additionally"])
                    , request_json["question"]
                    , request_json["answer"]
                    , request_json["email"]
                    , request_json["school_name"]
                    , request_json['created_date'])

            
                cursor.execute(update_sql, values)
                conn.commit()
                select_sql ='''Select count(*) from tollow.'''+request_json['view']+'''_view_inform_iep
                                    where email = %s and school_name = %s
                                    and assessment_results = %s
                                    and barriers_learning = %s
                                    and review_learning_style = %s
                                    and review_strength = %s
                                    and review_interest = %s
                                    and review_limiting_belief = %s
                                    and review_enabling_belief = %s
                                    and soft_name = %s
                                    and soft_name = %s
                                    and negotiate_goal = %s
                                    and how_goals_can_be_achieved = %s
                                    and any_concerns = %s
                                    and teachers_can_do_additionally = %s
                                    and question = %s
                                    and answer = %s'''
                values = (          request_json['email']
                                    , request_json["school_name"]
                                    , request_json["assessment_results"]
                                    , request_json["barriers_learning"]
                                    , request_json["review_learning_style"]
                                    , request_json["review_strength"]
                                    , request_json["review_interest"]
                                    , request_json["review_limiting_belief"]
                                    , request_json["review_enabling_belief"]
                                    , str(request_json["soft_name"])
                                        , str(request_json["soft_skill"])
                                    , str(request_json["negotiate_goal"])
                                    , request_json["how_goals_can_be_achieved"]
                                    , request_json["any_concerns"]
                                    , request_json["teachers_can_do_additionally"]
                                    , request_json["question"]
                                    , request_json["answer"])
                cursor.execute(select_sql,values
                                
                                    )
                record = cursor.fetchone()
            

                if not record and record[0] == 0:
                    return create_json('internal error', "internal error")
            
                return create_json('success', "Know Your Student Updated.")
        
        except Exception as error:
            print(error)
        finally:
            conn.close()
   
class extractIEP(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['email'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")


        conn = mysql.connect()
        cursor = conn.cursor()
        mysql_query = '''Select * from tollow.know_your_student as kns where kns.email = %s '''
        cursor.execute(mysql_query,(request_json['email']))
       
        record = cursor.fetchone()
        if not record:
            return create_json('no records', "no records found")
       
        print (record)
        result = create_json('success', record)
       
        conn.close()
        return result

class reviewIEP(Resource):
    def post(self):
        request_json = request.get_json()

        mandate_param = ['user_id',
                         'email',
                         'school_name',
                         'revisit_goal',
                         'assessment_result',
                         'examples',
                         'achieve_goals',
                         'any_conserns',
                         'teachers_can_do_additionally'
                         ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            update_sql = '''UPDATE tollow.''' + request_json["view"] + '''_view_review_iep set
                                    revisit_goal = %s
                                   , assessment_result = %s
                                   , examples = %s
                                   , achieve_goals = %s
                                   , any_conserns = %s
                                   , teachers_can_do_additionally = %s
                                   where email = %s and school_name = %s'''
            values = (
                request_json["revisit_goal"]
                , request_json["assessment_result"]
                , request_json["examples"]
                , request_json["achieve_goals"]
                , request_json["any_conserns"]
                , request_json["teachers_can_do_additionally"]
                , request_json["email"]
                , request_json["school_name"])


            cursor.execute(update_sql, values)
            conn.commit()
            select_sql ='''Select count(*) from tollow.'''+request_json['view']+'''_view_review_iep
                                where email = %s and school_name = %s
                                and revisit_goal = %s
                                and assessment_result = %s
                                and examples = %s
                                and achieve_goals = %s
                                and any_conserns = %s
                                and teachers_can_do_additionally = %s'''

            values = (request_json['email']
                    , request_json["school_name"]
                    , request_json["assessment_result"]
                    , request_json["examples"]
                    , request_json["achieve_goals"]
                    , request_json["any_conserns"]
                    , request_json["teachers_can_do_additionally"]
            )
            cursor.execute(select_sql,values)

            record = cursor.fetchone()
           

            if not record and record[0] == 0:
                return create_json('internal error', "internal error")
           
            return create_json('success', "Know Your Student Registered")
       
        except Exception as error:
            print(error)
        finally:
            conn.close()
            
class ViewInformIEP(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school'
                        , 'view'
                        , 'created_date'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''select count(*) 
                                from tollow.user_info 
                                where email = %s and school_name = %s and role = 'Student' ''',(request_json['email'], request_json['school'])
                        )
                        
            students_check = cursor.fetchone()
            if students_check[0] == 1:
                cursor.execute('''select * 
                                    from tollow.'''+request_json['view']+'''_view_inform_iep 
                                    where email = %s and school_name = %s and created_date = %s ''',(
                                            request_json['email'], 
                                            request_json['school'],
                                            request_json['created_date'])
                        )
                record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                record_list=[]
                for record in record:
                    record_dict = {}
                    for key, val in record.items():
                          
                        if (key == 'created_date' or key == 'updated_date') and  type(val) != str :
                            record_dict[key] = val.strftime("%d-%m-%Y")                                
                        else:
                            record_dict[key] = val
                    record_list.append(record_dict)
                result = create_json('success', record_list)
                return result
        except Exception as error:
            print(error)





       
class teacherComments(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['school'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            mysql_query = '''Select user_id, first_name, last_name, teacher_email_id, comments, 
                            student_email_id,created_date from tollow.teacher_comment as comm 
                            where comm.school_name = %s and comm.student_email_id= %s'''


            cursor.execute(mysql_query,(request_json['school'], request_json['student_email_id']))
            LOGGER.info(mysql_query)
            record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        
            if not record:
                LOGGER.info("No records Found")
                return create_json('no records', "no records found")
            
        
            record_list=[]
            for record in record:
                record_dict = {}
                for key, val in record.items():
                    
                  
                            
                    if key == 'created_date' :
                        if type(val)!=str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = val
                            
                    else:
                        record_dict[key] = val
                record_list.append(record_dict)
            result = create_json('success', record_list)
            return result

        except Exception as error:
            print(error)

        finally:
            conn.close()

class mapStudentViews(Resource):
    def post(self):
        request_json = request.get_json()
        print(request_json)
        request_verification = param_verfication(request_json, ['school_name'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid requesta")

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            if request_json['active'].lower() != 'yes':
                 return create_json('invalid request', "invalid requestb")
            
            school_is_active = '''Select count(*) from tollow.user_info as info where info.email = %s and info.school_name = %s'''
            record = cursor.execute(school_is_active, (request_json['email'], request_json['school_name']))


            if not record and record[0] == 0:
                return create_json('no records', "no records found")
            
            mysql_query = '''Select soft_name, soft_skill, created_date from tollow.''' + request_json["view"] + '''_view_inform_iep as iep
                            where iep.school_name = %s and iep.email= %s  '''


            cursor.execute(mysql_query,(request_json['school_name'], request_json['email']))
            # LOGGER.info(mysql_query)
            record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            print(record)
            if not record:
                # LOGGER.info("No records Found")
                return create_json('no records', "no records found")
            
            record_list=[]
            for record in record:
                record_dict = {}
                for key, val in record.items():
                    if key == 'created_date':
                        if type(val)!=str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                    else:
                        record_dict[key] = val
                record_list.append(record_dict)
            
            result = create_json('success', record_list)
            return result

        except Exception as error:
            print(error, '123456')

        finally:
            conn.close()

        







class newStudentIEP(Resource):

    def post(self):

        request_json = request.get_json()

 

        request_verification = param_verfication(request_json, ['schools'

                                                               , 'iep'

                                                               , 'role'

                                                               , 'assessment_request'

                                                               , 'active'

                                                               ,'learning_coordinator'])

        if codes[request_verification] != '200':

            return create_json('invalid request', "invalid request")

        print(request_json)

        conn = mysql.connect()

        cursor = conn.cursor()

        mysql_query=('''Select count(*) from tollow.user_info as info, tollow.assessment_request as req where

                                info.iep = %s

                            and info.assessment_request = %s

                            and info.school_name = %s

                            and info.role = %s

                            and info.active = %s

                            and req.learning_coordinator = %s

                            ''',

                       (request_json['iep']

                        , request_json['assessment_request']

                        , request_json['schools']

                        , request_json['role']

                        , request_json['active']

                        , request_json['learning_coordinator']))

        print(mysql_query)

        LOGGER.debug(mysql_query)

        cursor.execute('''Select count(*) from tollow.user_info as info, tollow.assessment_request as req where

                                info.iep = %s

                            and info.assessment_request = %s

                            and info.school_name = %s

                            and info.role = %s

                            and info.active = %s

                            and req.learning_coordinator = %s

                            and info.user_id=req.user_id''',

                       (request_json['iep']

                        , request_json['assessment_request']

                        , request_json['schools']

                        , request_json['role']

                        , request_json['active']

                        , request_json['learning_coordinator']))

        record = cursor.fetchone()

        print (record)

        LOGGER.debug(mysql_query)

        if not record or record[0] == 0:

            return create_json('no records', "no records found")

        record_list = []

        record_list.append(record[0])

        result = create_json('success', record_list)

        return result

 

class studentAssessnment(Resource):

    def post(self):

        request_json = request.get_json()

 

        request_verification = param_verfication(request_json, ['schools'

                                                              , 'role'

                                                              , 'assessment_request'

                                                              , 'active'

                                                              ,'learning_coordinator'])

        if codes[request_verification] != '200':

            return create_json('invalid request', "invalid request")

 

        conn = mysql.connect()

        LOGGER.info("Mysql Connection Successful")

        cursor = conn.cursor()

        cursor.execute('''Select count(*) from tollow.user_info as info, tollow.assessment_request as req where

                                assessment_request = %s

                            and info.school_name = %s

                            and info.role = %s

                            and info.active = %s

                            and req.learning_coordinator = %s

                            and info.user_id=req.user_id''',

                       (  request_json['assessment_request']

                        , request_json['schools']

                        , request_json['role']

                        , request_json['active']

                        ,request_json['learning_coordinator']))

        record = cursor.fetchone()

        print (record)

        if not record or record[0] == 0:

            return create_json('no records', "no records found")

        record_list = []

        record_list.append(record[0])

        result = create_json('success', record_list)

        return result

   

   

class yearLevelData(Resource):

    def post(self):

        request_json = request.get_json()

 

        request_verification = param_verfication(request_json, ['class_year'])

       

        if codes[request_verification] != '200':

            return create_json('invalid request', "invalid request")

 

        conn = mysql.connect()

        # LOGGER.info("Mysql Connection Successful")

        cursor = conn.cursor()

       

        cursor.execute('''Select * from tollow.assessment_request where tollow.assessment_request.class_year=%s ''',request_json["class_year"])
        
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        print("iajx",request_json["class_year"],record)
        
        if not record or record[0] == 0:
            return create_json('no records', "no records found")
        record_list=[]
        for record in record:
            record_dict = {}
            for key, val in record.items():
                print(val,key == 'created_date' or key == 'review_date' or key == 'date_of_birth')
                if key == 'created_date' or key == 'review_date' or key == 'date_of_birth':
                    #print(val,type(val),type(val)!=str)
                    if type(val)!=str:
                        record_dict[key] = val.strftime("%d-%m-%Y")
                else:
                    record_dict[key] = val
            record_list.append(record_dict)

           

       

        print (record)

        result = create_json('success', record_list)

       

        conn.close()

        return result

 

class populateYearLevels(Resource):

    def post(self):

        conn = mysql.connect()

        LOGGER.info("Mysql Connection Successful")

        cursor = conn.cursor()

       

        cursor.execute(''' SELECT DISTINCT class_year from tollow.assessment_request; ''')

        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

       

        print (record)

        if not record or record[0] == 0:

            return create_json('no records', "no records found")

       

        record_list = []

        record_list.append(record[0])

        result = create_json('success', record)

        return result

       
class newStudentDetails(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['school','learning_coordinator'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")


        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select 
                            *
                        from tollow.assessment_request
                        where user_id In ( select user_id from 
                        tollow.user_info where school_name=%s)
                        and learning_coordinator=%s and iep<>"yes" ''',
                        (request_json['school']
                        ,request_json['learning_coordinator'])
                       )
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        

        cursor.execute('''SELECT new_student_duration
                            FROM school_setting
                            WHERE school_name = %s ''',(request_json['school']))      
            
        get_duration = cursor.fetchone()
        new_student_duration = get_duration[0]
        
        if not record or record[0] == 0:
            return create_json('no records', "no records found")
        record_list=[]
        for record in record:
            record_dict = {}
            for key, val in record.items():
                
                if key == 'created_date' :
                    #print(val,type(val),type(val)!=str)
                    if type(val)!=str:
                        now  = datetime.now().date()
                        duration = now - val
                        if(duration.days>new_student_duration):
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict = {}
                            break
                elif key == 'review_date' or key == 'date_of_birth':
                    if type(val)!=str:
                        record_dict[key] = val.strftime("%d-%m-%Y")
                    else:
                        record_dict[key] = val
                        
                else:
                    record_dict[key] = val
            record_list.append(record_dict)
        record_list=[i for i in record_list if i!={}]
        print(record,"record")
        print (record_list,"record_list")
        
        result = create_json('success', record_list)
        return result










class createLessonUnit(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'school'
                        , 'teacher_email'
                        , 'unit_plan'
                        , 'targeted_learing_outcomes'
                        , 'activity'
                        , 'assessment_task'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE email = %s and school_name = %s and role = 'Teacher' ''',(request_json['teacher_email'], request_json['school']))
        
            teacher_check = cursor.fetchone()
            if teacher_check[0] == 1:
                cursor.execute(''' INSERT INTO unit_plan(teacher_email, school_name, unit_plan, targeted_learing_outcomes, activity, assessment_task,continue_lesson,no_lesson)
                                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s) ''',(request_json['teacher_email']
                                                                    , request_json['school']
                                                                    , request_json['unit_plan']
                                                                    , request_json['targeted_learing_outcomes']
                                                                    , request_json['activity']
                                                                    , request_json['assessment_task']
                                                                    , request_json['continue_lesson']
                                                                    , request_json['no_lesson']))
                conn.commit()
                cursor.execute('''SELECT COUNT(*)
                                    FROM unit_plan
                                    WHERE teacher_email = %s and unit_plan = %s ''',(request_json['teacher_email'], request_json['unit_plan']))
                records = cursor.fetchone()
                if records[0] != 0:
                    return create_json('success', 'Lesson unit Created Successfully.')
                else:
                    return create_json('invalid request', "invalid request")

        except Exception as error:
            print(error)


class updateLessonUnit(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'unit_id'
                        , 'unit_plan'
                        , 'targeted_learing_outcomes'
                        , 'activity'
                        , 'assessment_task',
                        "no_lesson"
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''SELECT COUNT(*)
                                FROM unit_plan
                                WHERE unit_id = %s ''',(request_json['unit_id']))
        
            unit_id_check = cursor.fetchone()
            if unit_id_check[0] == 1:
                cursor.execute(''' UPDATE unit_plan
                                    SET unit_plan = %s, targeted_learing_outcomes = %s, activity = %s, assessment_task = %s, no_lesson=%s
                                    WHERE unit_id = %s ''',(request_json['unit_plan']
                                                            , request_json['targeted_learing_outcomes']
                                                            , request_json['activity']
                                                            , request_json['assessment_task']
                                                            , request_json["no_lesson"]
                                                            , request_json['unit_id'])
                                    )
                conn.commit()
                cursor.execute('''SELECT COUNT(*)
                                    FROM unit_plan
                                    WHERE unit_id = %s and unit_plan = %s ''',(request_json['unit_id'], request_json['unit_plan']))
                records = cursor.fetchone()
                if records[0] != 0:
                    return create_json('success', 'Lesson unit Updated Successfully.')
                else:
                    return create_json('invalid request', "invalid request")

        except Exception as error:
            print(error)


class viewLessonUnit(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'school'
                        , 'teacher_email'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''SELECT *
                                FROM unit_plan
                                WHERE school_name = %s AND teacher_email = %s ''',(request_json['school'], request_json['teacher_email']))
        
            #records = cursor.fetchall()
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            if records:
                record_list=[]
                for record in records:
                    record_dict = {}
                    for key, val in record.items():
                        
                    
                                
                        if key == 'created_date' or key == "continue_lesson":
                            if type(val)!=str:
                                record_dict[key] = val.strftime("%d-%m-%Y")
                            else:
                                record_dict[key] = val
                                
                        else:
                            record_dict[key] = val
                    record_list.append(record_dict)
                result = create_json('success', record_list)
                return result
            else:
                return create_json('invalid request', "invalid request")

        except Exception as error:
            print(error)

class deleteLessonUnit(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'unit_id']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            
            cursor.execute(''' DELETE 
                                FROM `unit_plan` 
                                WHERE unit_id = %s ''',(request_json['unit_id']))

            conn.commit()
            cursor.execute('''SELECT COUNT(*)
                                FROM unit_plan
                                WHERE unit_id = %s ''',(request_json['unit_id']))
        
            records = cursor.fetchone()
            print(records)
            if records[0] == 0:
                return create_json('success', 'Lesson unit Deleted Successfully.')
            else:
                return create_json('invalid request', "invalid request")

        except Exception as error:
            print(error)









class createModificationStudent(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'teacher_email'
                        , 'school_name'
                        , 'category_of_concerns'
                        , 'notes'
                        , 'created_date'
                        , 'request_assessment'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        print("4")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE email = %s and school_name = %s and role = 'Student' ''',(request_json['email'], request_json['school_name']))
            student_check = cursor.fetchone()
            
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE email = %s and school_name = %s and role = 'Teacher' ''',(request_json['teacher_email'], request_json['school_name']))
            teacher_check = cursor.fetchone()
            print("1")
            
            if student_check[0] == 1 and teacher_check[0] == 1:
                print(True)
                cursor.execute(''' INSERT INTO modification_for_student(email, teacher_email, school_name, category_of_concerns, notes,created_date)
                                    VALUES(%s,%s,%s,%s,%s,%s) ''',(request_json['email']
                                                                    , request_json['teacher_email']
                                                                    , request_json['school_name']
                                                                    , request_json['category_of_concerns']
                                                                    , request_json['notes']
                                                                    , request_json['created_date']))
                conn.commit()
                cursor.execute('''SELECT COUNT(*)
                                    FROM modification_for_student
                                    WHERE email = %s and notes = %s ''',(request_json['email'], request_json['notes']))
                
                records = cursor.fetchone()
                print("2")
                if request_json['request_assessment']=="true":
                    cursor.execute('''UPDATE user_info
                                    SET assessment_request = 'yes'
                                    WHERE email = %s AND school_name = %s ''',(request_json['email'],
                                                                         request_json['school_name']      
                                                            ))
                    conn.commit()
                    print("3")
                    return create_json('success', 'Modification For Student Created Successfully.')
                else:
                    return create_json('invalid request', "invalid request")

        except Exception as error:
            print(error)

####PLAYLOAD
# {
#     "email" : "Jonathan.Lee@test.com",
#     "teacher_email" : "Jacob.Foorde@test.com",
#     "school_name" : "School A",
#     "category_of_concerns" : "['Test2']", 
#     "notes" : "Notes ChS"
# }


class updateModificationStudent(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'modification_for_student_id'
                        , 'email'
                        , 'teacher_email'
                        , 'school_name'
                        , 'category_of_concerns'
                        , 'notes'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''SELECT COUNT(*)
                                FROM modification_for_student
                                WHERE modification_for_student_id = %s ''',(request_json['modification_for_student_id']))
        
            modification_for_student_id_check = cursor.fetchone()
            if modification_for_student_id_check[0] == 1:
                print(True)
                cursor.execute(''' UPDATE modification_for_student
                                    SET teacher_email = %s, category_of_concerns = %s, notes = %s
                                    WHERE modification_for_student_id = %s ''',(request_json['teacher_email']
                                                            , request_json['category_of_concerns']
                                                            , request_json['notes']
                                                            , request_json['modification_for_student_id']))
                conn.commit()
                cursor.execute('''SELECT COUNT(*)
                                    FROM modification_for_student
                                    WHERE modification_for_student_id = %s and notes = %s ''',(request_json['modification_for_student_id'], request_json['notes']))
                records = cursor.fetchone()
                if records[0] != 0:
                    return create_json('success', 'Modification For Student Updated Successfully.')
                else:
                    return create_json('invalid request', "invalid request")

        except Exception as error:
            print(error)
##### PLAYLOAD
# {
#     "modification_for_student_id" : 2,
#     "email" : "Jonathan.Lee@test.com",
#     "teacher_email" : "Jacob.Foorde@test.com",
#     "school_name" : "School A",
#     "category_of_concerns" : "['Testing Module', 'Test2']", 
#     "notes" : "TEsting Notes"
# }



class viewModificationStudent(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school_name'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''SELECT *
                                FROM modification_for_student
                                WHERE email = %s AND school_name = %s ''',(request_json['email'], request_json['school_name']))
        
            # records = cursor.fetchall()
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            record_dict = {}

            if records:
                list_of_record = []

                for record in records:
                    record_dict = {}
                    if record:
                        for key, val in record.items():
                            if key == 'created_date' and type(val) != str:
                                record_dict[key] = val.strftime("%d-%m-%Y")
                            else:
                                record_dict[key] = val
                        list_of_record.append(record_dict)
                result = create_json('success', list_of_record)   
                return result  
            else:
                return create_json('internal error', "Data is not Found.")

        except Exception as error:
            print(error)

##### PLAYLOAD
# {
#     "email" : "Jonathan.Lee@test.com",
#     "school_name" : "School A"
# }


class deleteModificationStudent(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'modification_for_student_id']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            
            cursor.execute(''' DELETE 
                                FROM `modification_for_student` 
                                WHERE modification_for_student_id = %s ''',(request_json['modification_for_student_id']))

            conn.commit()
            cursor.execute('''SELECT COUNT(*)
                                FROM modification_for_student
                                WHERE modification_for_student_id = %s ''',(request_json['modification_for_student_id']))
        
            records = cursor.fetchone()
            print(records)
            if records[0] == 0:
                return create_json('success', 'Modification For Student Deleted Successfully.')
            else:
                return create_json('invalid request', "invalid request")

        except Exception as error:
            print(error)

##### PLAYLOAD
# {
#     "modification_for_student_id" : 3
# }












class negotiateGoal(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school'
                        ]
        

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM student_view_inform_iep
                                WHERE email = %s AND school_name = %s ''',(request_json['email'], request_json['school']))      
            check_user = cursor.fetchone()
            if check_user[0] != 0:
                cursor.execute('''SELECT *
                                    FROM student_view_inform_iep
                                    WHERE email = %s ''',(request_json['email']))      
                records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                if records:
                    list_of_record = []

                    for record in records:
                        record_dict = {}
                        if record:
                            for key, val in record.items():
                                if key == 'created_date' or key == 'updated_date':
                                    if type(val) != str:
                                        record_dict[key] = val.strftime("%d-%m-%Y")
                                    else:
                                        record_dict[key] = val
                                else:
                                    record_dict[key] = val
                            list_of_record.append(record_dict)
                    result = create_json('success', list_of_record)   
                    return result 
                else:
                    return create_json('internal error', "Data is not Found.")
            else:
                return create_json('internal error', "Data is not Found.")
            
        except Exception as error:
            print(error)





class createReview(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name'
                        ,'review_name'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
        
            school_check = cursor.fetchone()
            cursor.execute('''SELECT COUNT(*)
                                FROM review
                                WHERE review_name = %s and school_name = %s  ''',(request_json['review_name'], request_json['school_name']))
            review_check = cursor.fetchone()            

            if school_check[0] == 1 and review_check[0] == 0:
                cursor.execute(''' INSERT INTO review(review_name, school_name)
                                    VALUES (%s, %s)''',  (request_json['review_name'], request_json["school_name"])
                                        )  
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from review
                                    where review_name = %s and school_name = %s''',(request_json['review_name'], request_json['school_name']))
                record = cursor.fetchone()
                if record[0] == 1:             
                    return create_json('success', "Review is Created.")
                else:
                    return create_json('internal error', "internal error")
            else:
                return create_json('internal error', "internal error")
          
        except Exception as error:
            print(error)

class editReview(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name'
                        ,'review_name'
                        ,'review_id'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
        
            school_check = cursor.fetchone()
            cursor.execute('''SELECT COUNT(*)
                                FROM review
                                WHERE review_id = %s  ''',(request_json['review_id']))
        
            review_name_check = cursor.fetchone()
            if school_check[0] == 1 and review_name_check[0] == 1:
                cursor.execute(''' update review 
                                    set review_name = %s
                                    where review_id = %s ''',  (request_json['review_name'], request_json['review_id'])
                                        )  
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from review
                                    where review_name = %s and review_id = %s''',(request_json['review_name'], request_json['review_id']))
                record = cursor.fetchone()
                if record[0] == 1:             
                    return create_json('success', "Review Name is Updated successfully.")
                else:
                    return create_json('internal error', "internal error")
            else:
                return create_json('internal error', "internal error")
        except Exception as error:
            print(error)

class viewReview(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT *
                                FROM review
                                WHERE school_name = %s ''',(request_json['school_name']))
        
            view_review = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  cursor.fetchall()]
            if view_review :
                return create_json('success', view_review)
            else:
                return create_json('internal error', "No records found")

        except Exception as error:
            print(error)

class deleteReview(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['review_name'
                        ,'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM review
                                WHERE review_name = %s and school_name = %s ''',(request_json['review_name'], request_json['school_name']))
        
            check_category_of_concern = cursor.fetchone()
            if check_category_of_concern[0] == 1:
                cursor.execute('''DELETE FROM review 
                                    WHERE review_name = %s ''',(request_json['review_name']))
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from review
                                    where review_name = %s ''',(request_json['review_name']))
                record = cursor.fetchone()
                if record[0] == 0:             
                    return create_json('success', "Review " + request_json['review_name'] + " is deleted.")
                else:
                    return create_json('internal error', "internal error")
            else:
                return create_json('internal error', "internal error")
        
            
        except Exception as error:
            print(error)










class getNewStudentDuration(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name']
        

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT *
                                FROM school_setting
                                WHERE school_name = %s ''',(request_json['school_name']))      
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            if records:
                return create_json('success', records)
            else:
                return create_json('internal error', "Data is not Found.")
            
        except Exception as error:
            print(error)

class updateNewStudentDuration(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'school_name', 'new_student_duration']
        

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM school_setting
                                WHERE school_name = %s ''',(request_json['school_name']))      
            
            school_check = cursor.fetchone()
            # print(school_check)
            if school_check[0] == 1:
                cursor.execute(''' UPDATE school_setting
                                    SET new_student_duration = %s
                                    WHERE school_name = %s ''',(request_json['new_student_duration'], request_json['school_name']))      
                conn.commit()
                cursor.execute(''' SELECT COUNT(*)
                                    FROM school_setting
                                    WHERE school_name = %s AND new_student_duration = %s ''',(request_json['school_name'], request_json['new_student_duration']))    
                records = cursor.fetchone()
                print(records)
                if records[0] == 1:    
                    return create_json('success', "New Student Duration is Updated Sucessfully.")
                else:
                    return create_json('internal error', "Data is not Found.")
                
        except Exception as error:
            print(error)









class userCount(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['schools','role'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")
        print(request_json)
        conn = mysql.connect()
        cursor = conn.cursor()
        
        cursor.execute('''Select count(*) from tollow.user_info as info where 
                             info.school_name = %s
                             and info.role = %s
                            ''',
                       (request_json['schools']
                       ,request_json['role']))
        record = cursor.fetchone()
        print (record)
        if not record or record[0] == 0:
            return create_json('no records', "no records found")
        record_list = []
        record_list.append(record[0])
        result = create_json('success', record_list)
        return result



class activeStudent(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['schools'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select count(*) from tollow.user_info as info where 
                            info.school_name = %s
                            and info.active = "yes" 
                            and info.role = "Student" ''',
                       ( request_json['schools']))
        record = cursor.fetchone()
        print (record)
        if not record or record[0] == 0:
            return create_json('no records', "no records found")
        record_list = []
        record_list.append(record[0])
        result = create_json('success', record_list)
        return result
        
class totalStudentDetails(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''Select first_name, last_name, email, date_of_birth, class_year,active,iep,assessment_request,school_name
                                from user_info
                                where school_name = %s and role = "Student" ''',( request_json['school']))
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
           
            list_of_record = []
            
            for record in records:
                record_dict = {}
                if record:
                    for key, val in record.items():
                        if type(val)!=str:
                            if key == 'date_of_birth':
                                record_dict[key] = val.strftime("%d-%m-%Y")
                            else:
                                record_dict[key] = val
                        else:
                             record_dict[key] = val
                    
                list_of_record.append(record_dict)
            print(list_of_record)
            result = create_json('success', list_of_record)   
            return result

        except Exception as error:
            print(error)

class activeStudentDetails(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''Select first_name, last_name, email, date_of_birth, class_year,active,iep,assessment_request,school_name
                                from user_info
                                where school_name = %s and active = "yes" and role = "Student" ''',( request_json['school']))
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            
            list_of_record = []
            print(records)
            for record in records:
                record_dict = {}
                if record:
                    for key, val in record.items():
                        if key == 'date_of_birth' and type(val)!=str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = val
                    
                    list_of_record.append(record_dict)
            result = create_json('success', list_of_record)   
            return result

        except Exception as error:
            print(error)




def param_verfication(request_json,request_list):
    """Function To Check the passing parameters"""
    # result = {}
    count = 0
    for param in request_list :
        count+=1
        if param in request_json and request_json[param] :
            pass
        else :
            return 'invalid request'
    return 'success'
 
 
 
 
 
 


class curriculumDisplay(Resource):
    def post(self):
        request_json = request.get_json()

        if request_json and 'curriculum' not in request_json:
            return create_json('invalid request', "invalid request")

        if request_json['curriculum'].upper() != 'ALL':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select curriculum_name from tollow.curriculum ''')
        record = cursor.fetchall()
        if not record:
            return create_json('no records', "no records found")
        record_list = []
        for rec in record:
            rec = (str(rec).replace(',', ''))
            rec = (str(rec).replace('((', '('))
            rec = (str(rec).replace('))', ')'))

            rec = (str(rec).replace("('", ''))
            rec = (str(rec).replace("')", ''))
            
            record_list.append(rec)
        
        result = create_json('success', record_list)
        print(result)
        return result

class registerSchool(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name'
                        , 'address'
                        , 'city'
                        , 'state'
                        , 'country'
                        , 'pincode'
                        , 'contact_details'
                        , 'share_data'
                        , 'retention'
                        , 'curriculum_name'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            mandate_param.append('creation_date')
            mandata_param_value.append(str(datetime.now()))
            query_value = ', '.join(['%s'] * len(mandata_param_value))

            columns = ', '.join(mandate_param)
            insert_sql = ''' INSERT INTO tollow.school_info (%s) VALUES (%s) ''' % (columns, query_value)
            cursor.execute(insert_sql,mandata_param_value)
            conn.commit()

            cursor.execute("Select count(*) from tollow.school_info where school_name = %s", request_json['school_name'])
            record = cursor.fetchone()

            if not record and record[0] == 0:

                return create_json('internal error', "internal error")
            return create_json('success', "SchoolRegistered")
        except Exception as error:
            print(error)


class addCurriculumcategory(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [
                  'category_name'
                , 'sub_category_name'
                , 'curricullum_name'
                , 'school_name'
                ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''select curriculum_id from tollow.curriculum where curriculum_name = %s'''
                           ,request_json['curricullum_name'])
            record = cursor.fetchall()
            if not record or record[0] == 0:
                return create_json('invalid request', "no records found")

            del request_json['curricullum_name']
            mandate_param.remove('curricullum_name')
            mandate_param.append('curricullum_id')
            request_json['curricullum_id'] = record[0][0]

            mandata_param_value = []
            for element in mandate_param:
                mandata_param_value.append(request_json[element])
            mandate_param.append('creation_date')
            mandata_param_value.append(str(datetime.now()))
            query_value = ', '.join(['%s'] * len(mandata_param_value))
            columns = ', '.join(mandate_param)

            insert_sql = ''' INSERT INTO tollow.curriculum_category_mapping (%s) VALUES (%s) ''' % (columns, query_value)
            cursor.execute(insert_sql, mandata_param_value)
            conn.commit()

            cursor.execute('''Select count(*) from tollow.curriculum_category_mapping where school_name = %s 
                                                                                     and curricullum_id= %s''',
                            (request_json['school_name'], request_json['curricullum_id']))
            record = cursor.fetchall()
            if not record and record[0] == 0:
                return create_json('internal error', "internal error")

            return create_json('success', "Catalogue Added")
        except Exception as error:
            print(error)



def param_verfication(request_json,request_list):
    """Function To Check the passing parameters"""
    # result = {}
    count = 0
    for param in request_list :
        count+=1
        if param in request_json and request_json[param] :
            pass
        else :
            return 'invalid request'
    return 'success'













class createSoftSkill(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name'
                        ,'soft_skill'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
        
            school_check = cursor.fetchone()
            cursor.execute('''SELECT COUNT(*)
                                FROM soft_skill
                                WHERE soft_skill = %s and school_name = %s  ''',(request_json['soft_skill'], request_json['school_name']))
            soft_skill_check = cursor.fetchone()            

            if school_check[0] == 1 and soft_skill_check[0] == 0:
                cursor.execute(''' INSERT INTO soft_skill(soft_skill, school_name)
                                    VALUES (%s, %s)''',  (request_json['soft_skill'], request_json["school_name"])
                                        )  
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from soft_skill
                                    where soft_skill = %s and school_name = %s''',(request_json['soft_skill'], request_json['school_name']))
                record = cursor.fetchone()
                if record[0] == 1:             
                    return create_json('success', "Soft Skill is Created.")
                else:
                    return create_json('internal error', "internal error")
            else:
                return create_json('internal error', "internal error")
          
        except Exception as error:
            print(error)

class editSoftSkill(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name'
                        ,'soft_skill'
                        ,'skill_id'
                        ]
        print(request_json)
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
        
            school_check = cursor.fetchone()
            cursor.execute('''SELECT COUNT(*)
                                FROM soft_skill
                                WHERE skill_id  = %s ''',(request_json['skill_id']))
        
            soft_skill_check = cursor.fetchone()
            if school_check[0] == 1 and soft_skill_check[0] == 1:
                cursor.execute(''' update soft_skill 
                                    set soft_skill = %s
                                    where skill_id = %s ''',  (request_json['soft_skill'], request_json['skill_id'])
                                        )  
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from soft_skill
                                    where soft_skill = %s and skill_id  = %s''',(request_json['soft_skill'], request_json['skill_id']))
                record = cursor.fetchone()
                if record[0] == 1:             
                    return create_json('success', "Soft Skill is Updated successfully.")
                else:
                    return create_json('internal error', "internal error")
            else:
                return create_json('internal error', "internal error")
        except Exception as error:
            print(error)

class viewSoftSkill(Resource):
    def post(self):
        
        

        
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            

            cursor.execute('''SELECT *
                                FROM soft_skill
                                 ''')
        
            view_soft_skill = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  cursor.fetchall()]
            if view_soft_skill :
                return create_json('success', view_soft_skill)
            else:
                return create_json('internal error', "No records found")

        except Exception as error:
            print(error)

class deleteSoftSkill(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['soft_skill'
                        ,'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM soft_skill
                                WHERE soft_skill = %s and school_name = %s ''',(request_json['soft_skill'], request_json['school_name']))
        
            check_category_of_concern = cursor.fetchone()
            if check_category_of_concern[0] == 1:
                cursor.execute('''DELETE FROM soft_skill 
                                    WHERE soft_skill = %s ''',(request_json['soft_skill']))
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from soft_skill
                                    where soft_skill = %s ''',(request_json['soft_skill']))
                record = cursor.fetchone()
                if record[0] == 0:             
                    return create_json('success', "Soft Skill " + request_json['soft_skill'] + " is deleted.")
                else:
                    return create_json('internal error', "internal error")
            else:
                return create_json('internal error', "internal error")
        
            
        except Exception as error:
            print(error)









class CreateKeyOutcome(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school_name'
                        , 'notes_and_comments' 
                        , 'support_need' 
                        , 'we_currently_see' 
                        , 'strategies_adjustment' 
                        , 'success_looks_like' 
                        , 'frequency' 
                        , 'level_of_adjustments' 
                        , 'new_strategy' 
                        , 'outcome_column_number' 
                        , 'lc_email' 
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            ##### Check student
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE role = 'Student' and email = %s and school_name = %s ''',(request_json['email'], request_json['school_name']))
        
            student_check = cursor.fetchone()
            ##### Check Coordinator
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE role = 'Coordinator' and email = %s and school_name = %s ''',(request_json['lc_email'], request_json['school_name']))
        
            coordinator_check = cursor.fetchone()
            if coordinator_check[0] == 1 and student_check[0] == 1:
                cursor.execute('''INSERT INTO step3_key_outcome(email, school_name, notes_and_comments, support_need, we_currently_see, strategies_adjustment, success_looks_like, frequency, level_of_adjustments, new_strategy, outcome_column_number, lc_email)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s) ''',
                                    (request_json['email'], 
                                    request_json['school_name'],
                                    str(request_json['notes_and_comments']),
                                    str(request_json['support_need']),
                                    str(request_json['we_currently_see']),
                                    str(request_json['strategies_adjustment']),
                                    str(request_json['success_looks_like']),
                                    str(request_json['frequency']),
                                    str(request_json['level_of_adjustments']),
                                    str(request_json['new_strategy']),
                                    request_json['outcome_column_number'],
                                    request_json['lc_email'])
                                )
                conn.commit()
                cursor.execute('''Select count(*)
                                    from step3_key_outcome 
                                    where email = %s and outcome_column_number = %s ''',(request_json['email'], request_json['outcome_column_number']))
                record = cursor.fetchone()
                #### Get the key outcome id
                cursor.execute('''Select MAX(key_outcome_id)
                                    from step3_key_outcome 
                                    where email = %s and outcome_column_number = %s ''',(request_json['email'], request_json['outcome_column_number']))
                key_outcome_id = cursor.fetchone()

                data = ("Key Outcome Created", key_outcome_id[0])
                if record[0] == 1:             
                    return create_json('success', key_outcome_id[0])
                else:
                    return create_json('internal error', "internal error") 
        except Exception as error:
            print(error)











class viewKeyOutcome(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'key_outcome_id' ]
        print(request_json)
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            ##### Check student
            record_list = []
            list_of_record = []
            # for key in request_json['key_outcome_id']:
            #     print(key)
                
            cursor.execute('''SELECT *
                                FROM step3_key_outcome
                                WHERE key_outcome_id = %s ''',(request_json['key_outcome_id']))
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            #print(records)
            

            for record in records:
                record_dict = {}
                if record:
                    for key, val in record.items():
                        if key == 'created_date' and type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = eval(str(val)) if (val and str(val)[0]=="[") else val
                    list_of_record.append(record_dict)
         
            if list_of_record:
                return create_json('success', list_of_record)    
            else:
                return create_json('internal error', "DATA NOT FOUND.")
               
        except Exception as error:
            print(error)

class updateKeyOutcome(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'key_outcome_id'
                        , 'email'
                        , 'school_name'
                        , 'notes_and_comments' 
                        , 'support_need' 
                        , 'we_currently_see' 
                        , 'strategies_adjustment' 
                        , 'success_looks_like' 
                        , 'frequency' 
                        , 'level_of_adjustments' 
                        , 'new_strategy' 
                        , 'outcome_column_number' 
                        , 'lc_email' 
                        , 'tag_teachers'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            ##### Check student
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE role = 'Student' and email = %s and school_name = %s ''',(request_json['email'], request_json['school_name']))
        
            student_check = cursor.fetchone()
            ##### Check Coordinator
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE role = 'Coordinator' and email = %s and school_name = %s ''',(request_json['lc_email'], request_json['school_name']))
        
            coordinator_check = cursor.fetchone()
            if coordinator_check[0] == 1 and student_check[0] == 1:
                cursor.execute('''UPDATE step3_key_outcome
                                    SET notes_and_comments = %s, support_need = %s, 
                                        we_currently_see = %s, 
                                        strategies_adjustment = %s, 
                                        success_looks_like = %s, frequency = %s, level_of_adjustments = %s, new_strategy = %s, outcome_column_number = %s, tag_teachers = %s
                                    WHERE key_outcome_id = %s ''',
                                    (str(request_json['notes_and_comments']),
                                    str(request_json['support_need']),
                                    str(request_json['we_currently_see']),
                                    str(request_json['strategies_adjustment']),
                                    str(request_json['success_looks_like']),
                                    str(request_json['frequency']),
                                    str(request_json['level_of_adjustments']),
                                    str(request_json['new_strategy']),
                                    request_json['outcome_column_number'],
                                    str(request_json['tag_teachers']),
                                    request_json['key_outcome_id']
                                    )
                                )
                conn.commit()
                cursor.execute('''Select count(*)
                                    from step3_key_outcome 
                                    where email = %s and outcome_column_number = %s ''',(request_json['email'], request_json['outcome_column_number']))
                record = cursor.fetchone()
                #### Get the key outcome id
                cursor.execute('''Select key_outcome_id
                                    from step3_key_outcome 
                                    where email = %s and outcome_column_number = %s ''',(request_json['email'], request_json['outcome_column_number']))
                key_outcome_id = cursor.fetchone()

                data = ("Key Outcome Updated Successfully", key_outcome_id[0])
                if record[0] == 1:             
                    return create_json('success', data)
                else:
                    return create_json('internal error', "internal error") 
        except Exception as error:
            print(error)



class StratergiesAdjustments_Create(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'schl_admin_email'
                        , 'school_name'
                        , 'title'
                        , 'subtitle'
                        
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''select COUNT(*)
                                from tollow.user_info 
                                where email = %s and school_name = %s and role = 'Coordinator' ''',(request_json['schl_admin_email'], request_json['school_name'])
                            )
            school_admin = cursor.fetchone()
            if school_admin[0] == 1:
                cursor.execute('''SELECT COUNT(*)
                                    FROM tollow.strategies_adjustments
                                    WHERE school_name = %s AND title= %s  ''',(request_json['school_name'], request_json['title'])
                            )
                title_check = cursor.fetchone()
                if title_check[0] == 0:
                    cursor.execute(''' INSERT INTO strategies_adjustments(title, subtitle, school_name)
                                        VALUES (%s,  %s, %s)''',  (request_json["title"], request_json['subtitle'], request_json['school_name'])
                                    ) 
                    conn.commit()
                    cursor.execute('''Select count(*) 
                                        from tollow.strategies_adjustments 
                                        where school_name = %s and title = %s''',(request_json['school_name'], request_json['title']))
                    subject = cursor.fetchone()
                    if subject[0] == 1:             
                        return create_json('success', "Strategies Added Successfully.")
                    else:
                        return create_json('internal error', "internal error")
                elif title_check[0] == 1:
                    return create_json('internal error', "This Title is Already Exists.")

        except Exception as error:
            print(error)


class updateStratergiesAdjustments(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'adjustment_id'
                        , 'title'
                        , 'subtitle'
                        , 'efforts'
                        , 'efficiency'
                        ]
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:

            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            
            cursor.execute('''SELECT COUNT(*)
                                FROM strategies_adjustments
                                WHERE adjustment_id = %s ''',(request_json['adjustment_id'])
                            )
            get_id = cursor.fetchone()
            if get_id[0] == 1:
                cursor.execute(''' UPDATE strategies_adjustments
                                    SET title = %s, subtitle = %s, efforts = %s, efficiency = %s
                                    WHERE adjustment_id = %s ''',  (request_json["title"]
                                                                    , request_json["subtitle"]
                                                                    , request_json["efforts"]
                                                                    , request_json["efficiency"]
                                                                    ,request_json['adjustment_id']
                                                                    )
                                    )
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from strategies_adjustments 
                                    where title = %s and subtitle = %s and efforts = %s and efficiency= %s''',
                                                                    (request_json["title"]
                                                                    , request_json["subtitle"]
                                                                    , request_json["efforts"]
                                                                    , request_json["efficiency"]
                                                                   ))
                record = cursor.fetchone()
                if record[0] == 1:
                    return create_json('internal error', "Stratergies Adjustments Updated Successfully.")
                else:
                    return create_json('internal error', "internal error") 
            else:
                return create_json('internal error', "internal error")
        except Exception as error:
            print(error)


class ViewStratergiesAdjustments(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                from tollow.strategies_adjustments
                                where school_name = %s  ''',(request_json['school_name'])
                            )
            school_name = cursor.fetchone()
            if school_name[0] != 0:
                cursor.execute('''SELECT *
                                    from tollow.strategies_adjustments
                                    where school_name = %s ''',(request_json['school_name'])
                                )
                subjects =[dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  cursor.fetchall()]
                
                cursor.execute('''SELECT *
                                    from tollow.strategies_adjustments
                                    where school_name in (SELECT source from share_data where destination = %s) ''',(request_json['school_name'])
                                )
                share_data=[dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  cursor.fetchall()]
                subjects=subjects+share_data
                print(subjects,share_data)
                return create_json('success', subjects)
            else:
                return create_json('internal error', "internal error")
        except Exception as error:
            print(error)




class deleteStratergiesAdjustments(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['title'
                        ,'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM strategies_adjustments
                                WHERE title = %s and school_name = %s ''',(request_json['title'], request_json['school_name']))
        
            check_strategies_adjustments = cursor.fetchone()
            if check_strategies_adjustments[0] == 1:
                cursor.execute('''DELETE FROM strategies_adjustments 
                                    WHERE title = %s and school_name = %s ''',(request_json['title'], request_json['school_name']))
                conn.commit()
                cursor.execute('''Select count(*) 
                                    from strategies_adjustments
                                    WHERE title = %s and school_name = %s ''',(request_json['title'], request_json['school_name']))
                record = cursor.fetchone()
                if record[0] == 0:             
                    return create_json('success', "Your Record is deleted.")
                else:
                    return create_json('internal error', "internal error")
            else:
                return create_json('internal error', "internal error")
        
            
        except Exception as error:
            print(error)
















class iepStudentDetails(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['school_name','email','role'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        mysql_query = '''Select
                            first_name
                          , last_name
                          , date_of_birth
                          , user_id
                          , class_year
                          , created_date
                        from tollow.user_info as info  where info.school_name = %s and info.role=%s and info.active="yes" and info.email= %s'''
        cursor.execute(mysql_query,(request_json['school_name'],request_json['role'],request_json['email'])) 
        LOGGER.info(mysql_query)         
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

        if not record or record[0] == 0:
            return create_json('no records found', "no records found")

        record_list = list(record)

        result = create_json('success', record_list)
        conn.close()
        return result

class impInfo(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['email_id'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        mysql_query = '''Select
                            ndis_status
                          , nccd_status
                          , disability_category
                          , diagnostics
                          , outside_agencies
                          , current_referrals
                        from tollow.assessment_request as req  where req.email_id = %s'''
        cursor.execute(mysql_query,(request_json['email_id'])) 
        LOGGER.info(mysql_query)         
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

        if not record or record[0] == 0:
            return create_json('no records found', "no records found")

        record_list = list(record)

        result = create_json('success', record_list)
        conn.close()
        return result

class personalInfo(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['email_id'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        mysql_query = '''Select
                            review_strength
                          , review_interest
                          , review_limiting_belief
                          , review_enabling_belief
                          , review_learning_style
                        from tollow.student_view_inform_iep as iep  where iep.email_id = %s"'''
        cursor.execute(mysql_query,(request_json['email_id'])) 
        LOGGER.info(mysql_query)         
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

        if not record or record[0] == 0:
            return create_json('no records found', "no records found")

        record_list = list(record)

        result = create_json('success', record_list)
        conn.close()
        return result





class iep_step_1_studentDetails(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['school_name'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        mysql_query = '''Select
                            first_name, last_name
                          , date_of_birth
                          , user_id
                          , class_year
                          , creation_date
                        from tollow.user_info as info  where info.email = %s and info.school_name = %s and info.role="Student"'''
        cursor.execute(mysql_query,(request_json['email'], request_json['school_name'])) 
        LOGGER.info(mysql_query)         
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
    
        if record  == []:
            return create_json('no records', "no records found")
        list_of_record = []
        
        for record in record:
            record_dict = {}
            if record:
                for key, val in record.items():
                    if key == 'creation_date' or key == "date_of_birth":
                        record_dict[key] = val.strftime("%d-%m-%Y")
                    else:
                        record_dict[key] = val
                
                list_of_record.append(record_dict)
                
        print(list_of_record)
        result = create_json('success', list_of_record)   
        
        conn.close()
        return result

class iep_step_1_impInfo(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['email'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        mysql_query = '''Select
                            ndis_status
                          , nccd_status
                          , disability_category
                          , diagnostics
                          , outside_agencies
                          , current_referrals
                        from tollow.assessment_request as req  where req.email = %s'''
        cursor.execute(mysql_query,(request_json['email'])) 
        LOGGER.info(mysql_query)         
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

        if record  == []:
            return create_json('no records', "no records found")

        record_list = list(record)

        result = create_json('success', record_list)
        conn.close()
        return result

class iep_step_1_personalInfo(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['email'])
      
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        mysql_query = '''Select
                            review_strength, review_interest
                          , review_limiting_belief, review_enabling_belief
                          , review_learning_style
                        from tollow.student_view_inform_iep as iep  where iep.email = %s and school_name = %s'''
        cursor.execute(mysql_query,(request_json['email'], request_json['school_name'])) 
        LOGGER.info(mysql_query)         
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        print(record)
        if  record==[]:
            return create_json('no records', "no records found")

        record_list = record

        result = create_json('success', record_list)
        conn.close()
        return result

class iepID(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['email'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        mysql_query = '''Select
                            personal_info_iep_id
                        from tollow.student_profile_personal_info as info  
                        where info.email = %s and info.school_name = %s 
                        '''
        cursor.execute(mysql_query,(request_json['email'], 
                                    request_json['school_name'])) 
        LOGGER.info(mysql_query)         
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

        if record == []:
            return create_json('no records', "no records found")

        record_list = list(record)

        result = create_json('success', record_list)
        conn.close()
        return result
    







class roleDisplay(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['schools', 'role', 'active'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        if request_json['role']=="Student":
            cursor.execute('''Select first_name,last_name,email,learning_coordinator,teacher,class_year
                            from tollow.assessment_request
                            where user_id in (select user_id from tollow.user_info where role="Student" and school_name=%s) ''', ( request_json['schools']))
        else:
            cursor.execute('''Select first_name,last_name,email
                            from tollow.user_info 
                            where role = %s and school_name = %s and active = %s ''', ( request_json['role'], request_json['schools'], request_json['active']))
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in
                  cursor.fetchall()]

        if not record or record[0] == 0:
            return create_json('no records', "no records found")
        record_list = list(record)

        result = create_json('success', record_list)
        return result

class StudentTeacherAssign(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'students'
                        , 'role'
                        , 'school'
                        , 'teacher'
                        , 'coordinator'
                        ]

        for element in mandate_param:
            if element not in request_json:
                print(element,request_json)
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            students = request_json['students']
            default = False
            for student in students:
                cursor.execute('''select count(*) 
                                    from tollow.user_info 
                                    where email = %s and role = %s and school_name = %s''',(student, request_json['role'], request_json['school'])
                            )
                        
                students = cursor.fetchone()
                if students[0] == 1:
                    ### Code for Coordinator
                    cursor.execute('''select count(*)
                                from tollow.user_info
                                WHERE role= 'Coordinator' and email= %s and school_name= %s ''',(request_json['coordinator'], request_json['school'] )
                           )
                    coordinat = cursor.fetchone()
                    if coordinat[0] == 1:
                        default = True
                        cursor.execute(''' update tollow.assessment_request 
                                            set learning_coordinator = %s 
                                            where email = %s ''',  (request_json["coordinator"],  student)
                                    )
                        conn.commit()
                        cursor.execute('''Select count(*) 
                                            from tollow.assessment_request 
                                            where email = %s and learning_coordinator = %s''',(student, request_json['coordinator']))
                        record = cursor.fetchone()
                        print(record,'Record')
                        if record[0] == 0:
                            print('Check coordinator')
                            return create_json('internal error', "internal error")    
                    
                    ### Code for Teacher
                    # cursor.execute('''select count(*)
                    #                     from tollow.user_info
                    #                     WHERE role= 'Teacher' and email= %s and school_name= %s ''',(request_json['teacher'], request_json['school'] )
                    #         )
                    # teach = cursor.fetchone()
                    # if teach[0] == 1:
                    #     default = True
                    cursor.execute(''' update tollow.assessment_request 
                                        set teacher = %s 
                                        where email = %s ''',  (str(request_json["teacher"]),  student)
                                )
                    conn.commit()
                    cursor.execute('''Select count(*) 
                                        from tollow.assessment_request 
                                        where email = %s and teacher = %s''',(student, str(request_json['teacher'])))
                    record = cursor.fetchone()
                    if record[0] == 0:
                        print("Check teacher")
                        return create_json('internal error', "internal error")    
            if default :
                return create_json('success', "Updated Student assignment")
            else:
                return create_json('internal error', "internal error")    
        except Exception as error:
            print(error)








class studentViewReviewStatus(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            
            cursor.execute('''SELECT COUNT(*)
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
            school_check = cursor.fetchone()
            
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE email = %s and school_name = %s and role = 'Student' ''',(request_json['email'], request_json['school_name']))
            student_check = cursor.fetchone()
            
            if student_check[0] == 1 and school_check[0] == 1:
                cursor.execute('''SELECT review_status, review_date, created_date
                                    FROM student_view_review_iep
                                    WHERE email = %s and school_name = %s ''',(request_json['email'], request_json['school_name']))
                review = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

                cursor.execute('''SELECT class_year
                                    FROM assessment_request
                                    WHERE email = %s ''',(request_json['email']))
                class_year = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        
                list_of_record = []
                for record in review:
                    record_dict = {}
                    if record:
                        for key, val in record.items():
                            if (key == 'created_date' or key == 'review_date') and type(val) != str:
                                record_dict[key] = val.strftime("%d-%m-%Y")
                            else:
                                record_dict[key] = val
                        list_of_record.append(record_dict|class_year[0])
                
                result = create_json('success', list_of_record)   
                return result
            else:
                return create_json('internal error', "internal error") 
        except Exception as error:
            print(error)

####PLAYLOAD
# {
#     "email" : "David.Chao@test.com",
#     "school_name" : "School A"
# }






class SubjectCreate(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'school'
                        , 'schl_admin_email'
                        , 'subject_name'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''select COUNT(*)
                                from tollow.user_info 
                                where email = %s and school_name = %s and role = 'School Admin' ''',(request_json['schl_admin_email'], request_json['school'])
                            )
            school_admin = cursor.fetchone()
            if school_admin[0] == 1:
                cursor.execute('''SELECT COUNT(*)
                                    FROM tollow.subject_requiring_adjustment
                                    WHERE school_name = %s AND subject_name= %s  ''',(request_json['school'], request_json['subject_name'])
                            )
                subject_check = cursor.fetchone()
                if subject_check[0] == 0:
                    cursor.execute(''' INSERT INTO subject_requiring_adjustment(school_name, subject_name)
                                        VALUES (%s, %s)''',  (request_json["school"], request_json['subject_name'])
                                    ) 
                    conn.commit()
                    cursor.execute('''Select count(*) 
                                        from tollow.subject_requiring_adjustment 
                                        where school_name = %s and subject_name = %s''',(request_json['school'], request_json['subject_name']))
                    subject = cursor.fetchone()
                    if subject[0] == 1:             
                        return create_json('success', "Subject Added Successfully.")
                    else:
                        return create_json('internal error', "internal error")

                elif subject_check[0] == 1:
                    return create_json('internal error', "This Subject is Already Exists.")

        except Exception as error:
            print(error)


class ViewSubject(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                from subject_requiring_adjustment
                                where school_name = %s  ''',(request_json['school'])
                            )
            school = cursor.fetchone()
            if school[0] != 0:
                cursor.execute('''SELECT subject_name
                                    from subject_requiring_adjustment
                                    where school_name = %s ''',(request_json['school'])
                                )
                subjects = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                return create_json('success', subjects)
            else:
                return create_json('internal error', "internal error")
        except Exception as error:
            print(error)








class schoolsCount(Resource):
    def post(self):
        request_json = request.get_json()

        if request_json and 'schools' not in request_json:
            return create_json('invalid request', "invalid request")

        if request_json['schools'].upper() != 'ALL':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select count(*) from tollow.school_info where registration_page=%s and active=%s''',
                       ('yes','yes'))
        record = cursor.fetchone()
        if not record or record[0] == 0:
            return create_json('no records', "no records found")
        record_list = []
        for rec in record:
            rec = (str(rec).replace(',', ''))
            rec = (str(rec).replace('((', '('))
            rec = (str(rec).replace('))', ')'))
            record_list.append(rec)
        result = create_json('success', record_list)
        return result

class usersCount(Resource):
    def post(self):
        request_json = request.get_json()

        if request_json and 'users' not in request_json:
            return create_json('invalid request', "invalid request")
        conn = mysql.connect()
        cursor = conn.cursor()
        if request_json['users'].upper() == 'ALL':
            cursor.execute('''Select count(*) from tollow.user_info where active=%s''',
                       ('yes'))
        elif request_json['users'].upper() != 'ALL':
            cursor.execute('''Select count(*) from tollow.user_info where active=%s
                               and role=%s''',
                       ('yes',request_json['users']))
        
        
        record = cursor.fetchone()
        if not record or record[0] == 0:
            return create_json('no records', "no records found")
        record_list = []
        for rec in record:
            rec = (str(rec).replace(',', ''))
            rec = (str(rec).replace('((', '('))
            rec = (str(rec).replace('))', ')'))
            record_list.append(rec)
        result = create_json('success', record_list)
        return result



class schoolsDetails(Resource):
    def post(self):
        request_json = request.get_json()

        if request_json and 'schools' not in request_json:
            return create_json('invalid request as input', "invalid request")

        if request_json['schools'].upper() != 'ALL':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select 
                            school_name
                          , address
                          , city
                          , state
                          , country
                          , pincode
                          , contact_details
                          , active
                          , registration_page
                          , share_data
                          , retention 
                        from tollow.school_info ''',
                       )
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

        if not record or record[0] == 0:
            return create_json('no records', "no records found")
        record_list = list(record)

        result = create_json('success', record_list)
        return result

class usersDetails(Resource):
    def post(self):
        request_json = request.get_json()

        if request_json and 'users' not in request_json:
            return create_json('invalid request', "invalid request")

        if request_json['users'].upper() != 'ALL':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select first_name
                                , last_name
                                , email 
                                , role
                                , school_name
                                , contact_number
                                , iep
                                , class_year
                                , assessment_request
                                , active 
                                from tollow.user_info''',
                       )
        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        if not record or record[0] == 0:
            return create_json('no records', "no records found")

        result = create_json('success', record)
        return result

class deleteUser(Resource):
    def post(self):

        request_json = request.get_json()
        if request_json and 'users' not in request_json:
            return create_json('invalid request', "invalid request")

        deleteusers = []
        deleteusers = request_json['users'].split(',')
        conn = mysql.connect()
        cursor = conn.cursor()

        for deluser in deleteusers:
            cursor.execute('''Delete from tollow.user_info where email = %s''', deluser)
            conn.commit()
            cursor.execute('''Select count(*) from tollow.user_info where email = %s''', deluser)
            record = cursor.fetchall()
            flag = 0
            if record or record[0] == 0:
                flag = 0
            else:
                flag = 1
                return create_json('internal error', "deletion process issue")
        result = create_json('success', 'record deleted')
        return result














class TeacherAssessmentRequest(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['email'
                        , 'school']

        teacher = '%'+request_json['email']+'%'
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE role = 'Teacher' and email = %s and school_name = %s ''',(request_json['email'], request_json['school']))
        
            teacher_check = cursor.fetchone()
            if teacher_check[0] == 1:
                cursor.execute('''SELECT *
                                    FROM user_info
                                    WHERE email in (SELECT email FROM assessment_request where teacher like %s)  ''',(teacher))
                
                records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                print(records)
                
                list_of_record=[]
                for record in records:
                    record_dict = {}
                    if record:
                        for key, val in record.items():
                            if (key == 'updation_date' or key == 'creation_date' or key == 'date_of_birth') and type(val) != str:  
                                record_dict[key] = val.strftime("%d-%m-%Y")
                            else:
                                record_dict[key] = val
                        
                        # record_list = [(record_dict)]
                    list_of_record.append(record_dict)
                print(list_of_record)
                result = create_json('success', list_of_record)   
                return result
            else:
                return create_json('internal error', "internal error")

        except Exception as error:
            print(error)














class TeacherCommentsUpdateInsert(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school'
                        , 'student_email_id'
                        , 'comments'
                        , 'record_more_evidence'
                        , 'assessment_related_targeted_outcome'
                        , 'assessment_result'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            ### Get First and last name of teacher
            cursor.execute('''select first_name, last_name 
                                from user_info 
                                where email = %s and role = 'Teacher' and school_name = %s''',(request_json['email'], request_json['school'])
                            )
            teacher_data = cursor.fetchone()
            first_name = teacher_data[0]
            last_name = teacher_data[1]
            
            ### Get Email for teacher
            cursor.execute('''select count(*) 
                                from tollow.user_info 
                                where email = %s and role = 'Teacher' and school_name = %s''',(request_json['email'], request_json['school'])
                            )
            teacher = cursor.fetchone()

            ### Get Email for Student
            if teacher[0] == 1:
                cursor.execute('''select count(*)
                                    from tollow.user_info
                                    WHERE role= 'Student' and email= %s and school_name= %s ''',(request_json['student_email_id'], request_json['school'] )
                           )
                student = cursor.fetchone()
                
                #### Find the comment
                if student[0] == 1:
                    cursor.execute('''SELECT COUNT(*)
                                        FROM teacher_comment
                                        where teacher_email_id = %s and student_email_id = %s ''',(request_json['email'], request_json['student_email_id'] )
                           )
                    check_value = cursor.fetchone()
                    print(check_value)
                    ###### Update the present comment
                    if check_value[0] == 1:
                        cursor.execute(''' update teacher_comment 
                                            set comments = %s , record_more_evidence = %s, assessment_related_targeted_outcome = %s, assessment_result = %s
                                            where teacher_email_id = %s and student_email_id = %s  ''',  (
                                                request_json['comments'], 
                                                request_json['record_more_evidence'], 
                                                request_json['assessment_related_targeted_outcome'], 
                                                request_json['assessment_result'], 
                                                request_json['email'],  
                                                request_json['student_email_id'])
                                        )  
                        conn.commit()
                        cursor.execute('''Select count(*) 
                                            from tollow.teacher_comment 
                                            where teacher_email_id = %s and comments = %s''',(request_json['email'], request_json['comments']))
                        record = cursor.fetchone()
                        if record[0] == 1:             
                            return create_json('success', "Comment Update Successfully.")
                        else:
                            return create_json('internal error', "internal error")


                    ###### Generate new Comment
                    elif check_value[0] == 0:
                        cursor.execute(''' INSERT INTO teacher_comment(teacher_email_id, school_name, first_name, last_name, comments, record_more_evidence, assessment_related_targeted_outcome, assessment_result, student_email_id)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''',  (
                                                request_json["email"], 
                                                request_json["school"], 
                                                first_name, last_name, 
                                                request_json['comments'], 
                                                request_json['record_more_evidence'], 
                                                request_json['assessment_related_targeted_outcome'], 
                                                request_json['assessment_result'], 
                                                request_json['student_email_id'])
                                        )  
                        conn.commit()
                        print(True)
                        cursor.execute('''Select count(*) 
                                            from tollow.teacher_comment 
                                            where teacher_email_id = %s and comments = %s''',(request_json['email'], request_json['comments']))
                        record = cursor.fetchone()
                        if record[0] == 1:             
                            return create_json('success', "Comment Add Successfully.")
                        else:
                            return create_json('internal error', "internal error") 
        
        except Exception as error:
            print(error)





class authenticateuser(Resource):
    def post(self):
        request_json = request.get_json()

        if request_json and 'username' not in request_json:
            return {'Status': 'Invalid Request for username'}
        if request_json and 'password' not in request_json:
            return {'Status': 'Invalid Request for password'}

        if not request_json['username']:
            return {'Status': 'Invalid User Name & Password'}
        if not request_json['password']:
            return {'Status': 'Invalid User Name & Password'}

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select count(*) from tollow.user_info where email=%s && password=%s ''', (request_json['username'], request_json['password']))
        record = cursor.fetchone()

        if record[0] == 0:
            return {'Status': 'Invalid User Name & Password'}
        elif record[0] != 0:
            return {'Status': 'Login Successful'}
        elif not record[0]:
            return {"Status": 'Invalid Request'}

class validateUser(Resource):
    def post(self):
        request_json = request.get_json()

        if request_json and 'username' not in request_json:
            return {'Status' : 'Invalid Request'}

        if not request_json['username']:
            return {'Status' : 'Invalid User Name'}

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select count(*) from tollow.user_info where email=%s ''',
                       (request_json['username']))
        record = cursor.fetchone()

        if record[0] == 0:
            return {'Status': 'Successful'}
        elif record[0] != 0:
            return {'Status': 'Duplicate'}
        elif not record[0]:
            return {'Status': 'Invalid Entry'}

class rolesDisplay(Resource):
    def post(self):
        request_json = request.get_json()

        if request_json and 'roles' not in request_json:
            return {'Status' : 'Invalid Request'}

        if request_json['roles'].upper() != 'ALL':
            return {'Status' : 'Invalid Request'}

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select role_name from tollow.user_role where registration_page=%s ''', ('yes'))
        record = cursor.fetchall()
        if not record:
            return create_json('invalid request', "no records found")
        record_list = []
        for rec in record:
            print({"rec": rec})
            rec = (str(rec).replace(',', ''))
            rec = (str(rec).replace('((', '('))
            rec = (str(rec).replace('))', ')'))

            rec = (str(rec).replace("('", ''))
            rec = (str(rec).replace("')", ''))

            record_list.append(rec)
        result = create_json('success', record_list)
        return result

class schoolsDisplay(Resource):
    def post(self):
        request_json = request.get_json()

        if request_json and 'schools' not in request_json:
            return create_json('invalid request', "invalid request")

        if request_json['schools'].upper() != 'ALL':
            return create_json('invalid request', "invalid request")

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select school_name from tollow.school_info where registration_page=%s and active=%s''',
                       ('yes','yes'))
        record = cursor.fetchall()
        if not record:
            return create_json('no records', "no records found")
        record_list = []
        for rec in record:
            rec = (str(rec).replace(',', ''))
            rec = (str(rec).replace('((', '('))
            rec = (str(rec).replace('))', ')'))

            rec = (str(rec).replace("('", ''))
            rec = (str(rec).replace("')", ''))
            
            record_list.append(rec)
        result = create_json('success', record_list)
        return result


class authorizeUser(Resource):
    def post(self):
        request_json = request.get_json()

        if request_json and 'username' not in request_json:
            return create_json('invalid request', "invalid request")

        if not request_json['username']:
            return create_json('invalid request', "values not found")

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select first_name, last_name, email, role, school_name,active,iep from tollow.user_info where email=%s ''',
                       request_json['username'])
        record = [dict(line) for line in [zip([column[0] for column in cursor.description], row) for row in cursor.fetchall()]]
        if not record:
            return create_json('no records', "no records found")
        result = create_json('success', record)
        return result

class registerUser(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['first_name', 'last_name' , 'email', 'password', 'role', 'school_name', 'contact_number', 'class_year', 'date_of_birth', 'address']
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request mandatory param")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            mandate_param.append('creation_date')
            mandata_param_value.append(str(datetime.now()))
            query_value = ', '.join(['%s'] * len(mandata_param_value))

            columns = ', '.join(mandate_param)
            
            insert_sql = ''' INSERT INTO tollow.user_info (%s) VALUES (%s) ''' % (columns, query_value)
            cursor.execute(insert_sql,mandata_param_value)
            conn.commit()

            cursor.execute("Select count(*) from tollow.user_info where email = %s", request_json['email'])
            record = cursor.fetchone()
            print(record)
            if not record and record[0] == 0:
                print ("hello")
                return create_json('internal error', "internal error")
            return create_json('success', "UserRegistered")
        except Exception as error:
            print(error)


class userUpdate(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['email', 'school', 'active', 'iep', 'assessment_request']
        print(request_json)
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                mandata_param_value.append(request_json[element])

            cursor.execute(
                '''select count(*) from tollow.user_info where email = %s and school_name = %s''',
                (request_json['email'], request_json['school'])
                )

            record = cursor.fetchone()
            print(record)
            print (request_json["active"])
            if not record and record[0] == 0:
                return create_json('no records', "no records found")
            update_query = '''update tollow.user_info 
                                SET   active = %s, iep = %s
                                    , assessment_request = %s 
                                where email = %s and school_name = %s'''
            values = ( request_json["active"], request_json["iep"], request_json["assessment_request"], request_json["email"], request_json["school"])
            cursor.execute(update_query, values)
            conn.commit()

            cursor.execute('''Select count(*) from tollow.user_info where email = %s and school_name = %s''',(request_json['email'], request_json['school']))
            record = cursor.fetchall()
            print ("Updated ")
            print (record)

            if not record and record[0] == 0:
                return create_json('internal error', "internal error")

            return create_json('success', "Updated Student assignment")
        except Exception as error:
            print(error)









class viewAllReview(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name', 'learning_coordinator']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute(''' SELECT COUNT(*) 
                                FROM `user_info` 
                                WHERE school_name = %s AND email = %s AND role = 'Coordinator' ''',(request_json['school_name'], request_json['learning_coordinator']))
            check_coordinator = cursor.fetchone()
            if check_coordinator[0] == 1:
                cursor.execute(''' SELECT DISTINCT email 
                                    FROM `student_view_review_iep` 
                                    WHERE school_name = %s ''',(request_json['school_name']))
                student_record = cursor.fetchall()
                print(student_record)
                list_of_record = []

                if student_record:

                    for students in student_record:
                        student = students[0]
                        # print(student)

                        cursor.execute(''' SELECT * 
                                            FROM `assessment_request` 
                                            WHERE email = %s and learning_coordinator = %s ''',(student, request_json['learning_coordinator']))
                        records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                        record_dict = {}

                        for record in records:
                            if record:
                                for key, val in record.items():
                                    if (key == 'review_date' or key == 'created_date' or key == 'date_of_birth') and type(val) != str:  
                                        record_dict[key] = val.strftime("%d-%m-%Y")
                                    else:
                                        record_dict[key] = val
                                
                                # record_list = [(record_dict)]
                                list_of_record.append(record_dict)
                    print(list_of_record)
                    result = create_json('success', list_of_record)   
                    return result


        except Exception as error:
            print(error)






class viewCategoryOfConcerns(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'class_year'
                        , 'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            
            cursor.execute('''SELECT COUNT(*)
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
            school_check = cursor.fetchone()
            
            if school_check[0] == 1:
                cursor.execute('''SELECT COUNT(*)
                                    FROM category_of_concerns
                                    WHERE school_name = %s and class_year = %s ''',(request_json['school_name'], request_json['class_year']))
                data_count = cursor.fetchone()
            
                if data_count[0] != 0:
                    cursor.execute('''SELECT *
                                        FROM category_of_concerns
                                        WHERE school_name = %s and class_year = %s ''',(request_json['school_name'], request_json['class_year']))

                    records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                    print(records)
                    if records:
                        return create_json('success', records)
                else:
                    return create_json('internal error', "DATA NOT FOUND.")
            else:
                    return create_json('internal error', "DATA NOT FOUND.") 
        except Exception as error:
            print(error)

####PLAYLOAD
# {
#     "email" : "David.Chao@test.com",
#     "school_name" : "School A"
# }

















class viewUpcomingOverdueReview(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['review_status', 'school_name', 'learning_coordinator']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute(''' SELECT COUNT(*) 
                                FROM `user_info` 
                                WHERE school_name = %s AND email = %s AND role = 'Coordinator' ''',(request_json['school_name'], request_json['learning_coordinator']))
            check_coordinator = cursor.fetchone()
            if check_coordinator[0] == 1:
                cursor.execute(''' SELECT DISTINCT email 
                                    FROM `student_view_review_iep` 
                                    WHERE school_name = %s and review_status  = %s ''',(request_json['school_name'], request_json['review_status']))
                student_record = cursor.fetchall()
                print(student_record)
                list_of_record = []

                if student_record:

                    for students in student_record:
                        student = students[0]
                        # print(student)

                        cursor.execute(''' SELECT * 
                                            FROM `assessment_request` 
                                            WHERE email = %s and learning_coordinator = %s ''',(student, request_json['learning_coordinator']))
                        records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                        record_dict = {}

                        for record in records:
                            if record:
                                for key, val in record.items():
                                    if (key == 'review_date' or key == 'created_date' or key == 'date_of_birth') and type(val) != str:  
                                        record_dict[key] = val.strftime("%d-%m-%Y")
                                    else:
                                        record_dict[key] = val
                                
                                # record_list = [(record_dict)]
                                list_of_record.append(record_dict)
                    print(list_of_record)
                    result = create_json('success', list_of_record)   
                    return result


        except Exception as error:
            print(error)




class viewPastFormalAssessmentFiles(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            
            cursor.execute('''SELECT COUNT(*)
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
            school_check = cursor.fetchone()
            
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE email = %s and school_name = %s ''',(request_json['email'], request_json['school_name']))
            student_check = cursor.fetchone()

            if school_check[0] == 1 and student_check[0] == 1 : 
                cursor.execute('''SELECT *
                                    FROM past_formal_assessment_files   
                                    WHERE school_name = %s and email = %s ''',(request_json['school_name'], request_json['email']))
            
                records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                list_of_record = []

                for record in records:
                    record_dict = {}
                    if record:
                        for key, val in record.items():
                            if key == 'uploaded_date' and type(val) != str:
                                record_dict[key] = val.strftime("%d-%m-%Y")
                            else:
                                record_dict[key] = val
                        list_of_record.append(record_dict)
                result = create_json('success', list_of_record)   
                return result
            else:
                return create_json('internal error', "DATA NOT FOUND.")
               
        except Exception as error:
            print(error)

####PLAYLOAD
# {
#     "email" : "Masako.Tse@test.com",
#     "school_name" : "School B"
# }











class viewPastIepFile(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            
            cursor.execute('''SELECT COUNT(*)
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
            school_check = cursor.fetchone()
            
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE email = %s and school_name = %s ''',(request_json['email'], request_json['school_name']))
            student_check = cursor.fetchone()

            if school_check[0] == 1 and student_check[0] == 1 : 
                cursor.execute('''SELECT *
                                    FROM past_iep_files
                                    WHERE school_name = %s and email = %s ''',(request_json['school_name'], request_json['email']))
            
                records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                list_of_record = []

                for record in records:
                    record_dict = {}
                    if record:
                        for key, val in record.items():
                            if key == 'uploaded_date' and type(val) != str:
                                record_dict[key] = val.strftime("%d-%m-%Y")
                            else:
                                record_dict[key] = val
                        list_of_record.append(record_dict)
                result = create_json('success', list_of_record)   
                return result
            else:
                return create_json('internal error', "DATA NOT FOUND.")
               
        except Exception as error:
            print(error)

####PLAYLOAD
# {
#     "email" : "Masako.Tse@test.com",
#     "school_name" : "School B"
# }




class createFormalAssessment(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['email'
                        ,'school_name'
                        ,'assessment_type'
                        ,'assessment_kind'
                        ,'next_steps' ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE school_name = %s and email = %s and role = 'Student' ''',(request_json['school_name'], request_json['email']))
            check_student = cursor.fetchone()
            print(check_student)
            if check_student[0] == 1:
                cursor.execute('''INSERT INTO formal_assessment(email, school_name, assessment_type, assessment_kind, next_steps)
                                    VALUES (%s, %s, %s, %s, %s) ''',
                                        (request_json['email'], 
                                            request_json['school_name'],
                                            request_json['assessment_type'],
                                            request_json['assessment_kind'],
                                            request_json['next_steps']))
                conn.commit()
                print(True)
                cursor.execute(''' SELECT COUNT(*)
                                    FROM formal_assessment
                                    WHERE email = %s and school_name = %s and assessment_type = %s and assessment_kind = %s and next_steps = %s ''',(
                                        request_json['email'], 
                                        request_json['school_name'],
                                        request_json['assessment_type'],
                                        request_json['assessment_kind'],
                                        request_json['next_steps']))

                records = cursor.fetchone()
                if records[0] != 0:
                    return create_json('success', "Formal Assessment Created Successfully.")
                else:
                    return create_json('internal error', "internal error")

        except Exception as error:
            print(error)
#### PLAYLOAD
# {
#     "email": "Ashley.Williams@test.com" , 
#     "school_name" : "School A",
#     "assessment_type" : "assessment_type",
#     "assessment_kind" : "assessment_kind",
#     "next_steps" : "next_steps"
# }

class viewFormalAssessment(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['email'
                        ,'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT *
                                FROM formal_assessment
                                WHERE school_name = %s and email = %s ''',(request_json['school_name'], request_json['email']))
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            
            # records = cursor.fetchall()
            print(records)
            if records:
                return create_json('success', records)
            else:
                return create_json('internal error', "internal error")

        except Exception as error:
            print(error)

##### PLAYLOAD

# {
#     "email": "Ashley.Williams@test.com" , 
#     "school_name" : "School A"
# }


class deleteFormalAssessment(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['assessment_id']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''DELETE 
                                FROM `formal_assessment` 
                                WHERE assessment_id = %s ''',(request_json['assessment_id']))
            conn.commit()
            cursor.execute('''SELECT COUNT(*)
                                FROM formal_assessment
                                WHERE assessment_id = %s ''',(request_json['assessment_id']))
            records = cursor.fetchone()
            if records[0] == 0:
                return create_json('success', "Formal Assessment Deleted Successfully.")
            else:
                return create_json('internal error', "internal error")

        except Exception as error:
            print(error)


#### PLAYLOAD
# {
#     "assessment_id": 2
# }

class updateFormalAssessment(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['assessment_id'
                        ,'email'
                        ,'school_name'
                        ,'assessment_type'
                        ,'assessment_kind'
                        ,'next_steps' ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM formal_assessment
                                WHERE assessment_id = %s ''',(request_json['assessment_id']))
            check_student = cursor.fetchone()
            print(check_student)
            if check_student[0] == 1:
                cursor.execute('''UPDATE `formal_assessment` 
                                    SET `email`=%s , `school_name`=%s, `assessment_type`=%s, `assessment_kind`=%s, `next_steps`=%s 
                                    WHERE assessment_id = %s ''',
                                        (request_json['email'], 
                                            request_json['school_name'],
                                            request_json['assessment_type'],
                                            request_json['assessment_kind'],
                                            request_json['next_steps'],
                                            request_json['assessment_id']))
                conn.commit()
                print(True)
                cursor.execute(''' SELECT COUNT(*)
                                    FROM formal_assessment
                                    WHERE email = %s and school_name = %s and assessment_type = %s and assessment_kind = %s and next_steps = %s ''',(
                                        request_json['email'], 
                                        request_json['school_name'],
                                        request_json['assessment_type'],
                                        request_json['assessment_kind'],
                                        request_json['next_steps']))

                records = cursor.fetchone()
                if records[0] != 0:
                    return create_json('success', "Formal Assessment Updated Successfully.")
                else:
                    return create_json('internal error', "internal error")

        except Exception as error:
            print(error)

#### PLAYLOAD
# {
#     "assessment_id" : 4,
#     "email": "Ashley.Williams@test.com" , 
#     "school_name" : "School A",
#     "assessment_type" : "Updated ",
#     "assessment_kind" : "Updated",
#     "next_steps" : "Updated"
# }


class studentProfile(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school'
                        ]
        

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE email = %s AND school_name = %s ''',(request_json['email'], request_json['school']))      
            check_user = cursor.fetchone()
            if check_user[0] == 1:
                cursor.execute('''SELECT *
                                    FROM assessment_request
                                    WHERE email = %s ''',(request_json['email']))      
                records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                print(records,'Cehril Gandhi')
                if records:
                    list_of_record = []

                    for record in records:
                        record_dict = {}
                        if record:
                            for key, val in record.items():
                                if key == 'date_of_birth' or key == 'created_date' or key == 'review_date' and type(val) != str:
                                    record_dict[key] = val.strftime("%d-%m-%Y")
                                else:
                                    record_dict[key] = val
                            list_of_record.append(record_dict)
                    result = create_json('success', list_of_record) 
                    return result 
                else:
                    return create_json('internal error', "Data is not Found.")
            else:
                return create_json('internal error', "Data is not Found.")
            
        except Exception as error:
            print(error)






class teacherAssignStudentDetails(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['teacher_email']

        teacher = '%'+request_json['teacher_email']+'%'


        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE email LIKE %s and role = 'Teacher' ''',(teacher))

            teacher_check = cursor.fetchone()

            cursor.execute('''SELECT COUNT(*)
                                    FROM assessment_request
                                    WHERE teacher LIKE %s ''',(teacher))
            teacher_check_assessment = cursor.fetchone()

            if teacher_check[0] == 1 and teacher_check_assessment[0] != 0 :
                cursor.execute('''SELECT email
                                    FROM assessment_request
                                    WHERE teacher LIKE %s ''',(teacher))
                assign_students = cursor.fetchall()
                student_list = []
                print(assign_students)
                record_list=[]
                for student in assign_students:
                    student_ = student[0]
                    cursor.execute('''SELECT infoiep.email, infoiep.barriers_learning, infoiep.created_date as date,
                                                 infoiep.review_strength, infoiep.review_interest,
                                                 user.first_name,user.last_name
                                    FROM student_view_inform_iep as infoiep, user_info as user
                                    WHERE infoiep.email = %s and user.email=%s ORDER BY date DESC LIMIT 1''',(student_,student_))
                    student_details = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                    print(student_details,"check")
                    
                    for record in student_details:
                        record_dict = {}
                        for key, val in record.items():
                            if key == 'date' or key=='updated_date':
                                if type(val) != str:
                                    record_dict[key] = val.strftime("%d-%m-%Y")
                                else:
                                    record_dict[key] = val
                            else:
                                record_dict[key] = val
                        record_list.append(record_dict)
                if record_list:
                    return create_json('success', record_list)
                else:
                    return create_json('internal error', "DATA NOT FOUND.")
            else:
                return create_json('internal error', "DATA NOT FOUND.")

        except Exception as error:
            print(error)




class barGraphCounts(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'learning_coordinator_email'
                        , 'school_name' 
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE email = %s and school_name = %s and role = 'Coordinator' ''',(request_json['learning_coordinator_email'], request_json['school_name']))
            learing_coordinator_check = cursor.fetchone()
            # print(learing_coordinator_check)
            if learing_coordinator_check != 0 :
                cursor.execute('''SELECT email, class_year
                                    FROM assessment_request
                                    WHERE learning_coordinator = %s ''',(request_json['learning_coordinator_email']))
                student_list = cursor.fetchall()

                cursor.execute('''SELECT DISTINCT class_year
                                    FROM assessment_request
                                    WHERE learning_coordinator = %s ''',(request_json['learning_coordinator_email']))
                class_year_list = cursor.fetchall()

                class_year_list1 = []
                for class_year in class_year_list:
                    class_year_list1.append(class_year[0])

                dict2 = {}
                class_dict = {}
                list3 = []

                for class_ in class_year_list:
                    level_of_adjustments_list = []
                    list1 = []
                    dict1 = {}

                    cursor.execute('''SELECT level_of_adjustments
                                         FROM step3_key_outcome
                                         WHERE class_year = %s and lc_email = %s ''',(class_[0], request_json['learning_coordinator_email']))
                    level_of_adjustments = cursor.fetchall()

                    for level in level_of_adjustments:
                        temp = eval(level[0])
                        for val in temp:
                            level_of_adjustments_list.append(val)
                    
                    odtp_count = 0
                    supplementary_count = 0
                    extensive_count = 0
                    substantial_count = 0

                    for data in level_of_adjustments_list:
                        print(data)
                        if data == 'QDTP':        
                            odtp_count += 1
                        elif data == 'Substantial':
                            substantial_count += 1
                        elif data == 'Supplementary':
                            supplementary_count += 1
                        elif data == 'Extensive':
                            extensive_count += 1

                    
                    example = odtp_count, supplementary_count, extensive_count, substantial_count
                    print(example)
                    
                    for exa in example:
                        list1.append(exa)
                
                    list3.append(list1)

                dict1["class_year"] = class_year_list1
                dict1["bar_data"] = list3
                result = create_json('success', json.dumps(dict1))
            return result

        except Exception as error:
            print(error)


class updateModificationStudentStatus(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'modification_for_student_id'
                        , 'status']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request22")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''SELECT COUNT(*)
                                FROM modification_for_student
                                WHERE modification_for_student_id = %s ''',(request_json['modification_for_student_id']))
        
            modification_for_student_id_check = cursor.fetchone()
            if modification_for_student_id_check[0] == 1:
                cursor.execute(''' UPDATE modification_for_student
                                    SET status = %s
                                    WHERE modification_for_student_id = %s ''',
                                                            (request_json['status']
                                                            , request_json['modification_for_student_id']))
                conn.commit()
                cursor.execute('''SELECT COUNT(*)
                                    FROM modification_for_student
                                    WHERE modification_for_student_id = %s and status = %s ''',(request_json['modification_for_student_id'], request_json['status']))
                records = cursor.fetchone()
                if records[0] != 0:
                    
                    return create_json('success', 'Modification For Student Status Updated Successfully.')
                else:
                    return create_json('invalid request', "invalid request1")

        except Exception as error:
            print(error)



class modificationForStudentData(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name', 'teacher_email']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE school_name = %s and email = %s and role = 'Teacher' ''',(request_json['school_name'], request_json['teacher_email']))
            teacher_check = cursor.fetchone()
            if teacher_check[0] == 1:
                cursor.execute('''SELECT DISTINCT email 
                                FROM modification_for_student
                                WHERE teacher_email = %s ''',(request_json['teacher_email']))
                get_email = cursor.fetchall()
                # print(get_email)
                list_of_record = []

                for email in get_email:
                    cursor.execute('''SELECT MAX(modification_for_student_id)  
                                FROM modification_for_student
                                WHERE email = %s ''',(email[0]))
                    get_id = cursor.fetchall()

                    cursor.execute('''SELECT first_name, last_name, user_id,class_year
                                FROM assessment_request
                                WHERE email = %s ''',(email[0]))
                    # get_fname = cursor.fetchall()
                    get_fname = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                    for fname in get_fname:
                        pass
                    print(type(fname))

                    for id_data in get_id:
                        # print(get_fname)

                        cursor.execute('''SELECT *  
                                            FROM modification_for_student
                                            WHERE modification_for_student_id = %s ''',(id_data[0]))
                        data = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                        for get_data1 in data:
                            pass

                        get_data1.update(fname)
                        get_data = [get_data1]

                        list_of_data = []
                        record_dict = {}

                        for record in get_data:
                            if record:
                                for key, val in record.items():
                                    if (key == 'created_date' or key == 'review_date' or key == 'date_of_birth') and type(val) != str:
                                        record_dict[key] = val.strftime("%d-%m-%Y")
                                    else:
                                        record_dict[key] = val
                                list_of_record.append(record_dict)
                return create_json('success', list_of_record)   
            else:
                return create_json('internal error', "DATA NOT FOUND.")
        except Exception as error:
            print(error)

########PLAYLOAD
# {
#     "school_name" : "School A",
#     "teacher_email" : "Mira.Gupta@test.com" 
# }
class viewAllReviewCount(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name', 'learning_coordinator']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute(''' SELECT COUNT(*) 
                                FROM `user_info` 
                                WHERE school_name = %s AND email = %s AND role = 'Coordinator' ''',(request_json['school_name'], request_json['learning_coordinator']))
            check_coordinator = cursor.fetchone()
            if check_coordinator[0] == 1:
                cursor.execute(''' SELECT DISTINCT email 
                                    FROM `student_view_review_iep` 
                                    WHERE school_name = %s ''',(request_json['school_name']))
                student_record = cursor.fetchall()
                print(student_record)
                list_of_record = []

                if student_record:
                    cursor.execute(''' SELECT COUNT(*)
                                        FROM `assessment_request` 
                                        WHERE email IN (SELECT DISTINCT email 
                                                        FROM `student_view_review_iep` 
                                                        WHERE school_name = %s) and learning_coordinator = %s ''',(request_json['school_name'], request_json['learning_coordinator']))
                    # records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                    records = cursor.fetchone()
                    result = create_json('success', records[0])   
                
                return result

        except Exception as error:
            print(error)





class viewUpcomingOverdueReviewCount(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['review_status', 'school_name', 'learning_coordinator']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute(''' SELECT COUNT(*) 
                                FROM `user_info` 
                                WHERE school_name = %s AND email = %s AND role = 'Coordinator' ''',(request_json['school_name'], request_json['learning_coordinator']))
            check_coordinator = cursor.fetchone()
            if check_coordinator[0] == 1:
                cursor.execute(''' SELECT DISTINCT email 
                                    FROM `student_view_review_iep` 
                                    WHERE school_name = %s and review_status  = %s ''',(request_json['school_name'], request_json['review_status']))
                student_record = cursor.fetchall()
                print(student_record)
                list_of_record = []

                if student_record:
                    cursor.execute(''' SELECT COUNT(*)
                                        FROM `assessment_request` 
                                        WHERE email IN (SELECT DISTINCT email 
                                            FROM `student_view_review_iep` 
                                            WHERE school_name = %s and review_status  = %s) and learning_coordinator = %s ''',(request_json['school_name'], request_json['review_status'], request_json['learning_coordinator']))
                    records =  cursor.fetchone()
                    result =  create_json('success', records[0])   

                return result
        except Exception as error:
            print(error)





class getSubcategoryOfSoftskill(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['soft_skill']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            list_of_subcategory = []
            cursor.execute('''SELECT DISTINCT subcategory
                                FROM soft_skill
                                WHERE soft_skill = %s ''',(request_json['soft_skill']))
            get_subcategory = cursor.fetchall()
            for subcategory in get_subcategory:
                list_of_subcategory.append(subcategory[0])   
            
            if list_of_subcategory:
                return create_json('success', list_of_subcategory)
            else:
                return create_json('internal error', "DATA NOT FOUND.")

        except Exception as error:
            print(error)

########PLAYLOAD
# {
#     "soft_skill" : "SELF-AWARENESS"
# }


class getRootCauseOfSoftskill(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['subcategory']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            list_of_root_cause = []
            cursor.execute('''SELECT DISTINCT root_cause
                                FROM soft_skill
                                WHERE subcategory = %s ''',(request_json['subcategory']))
            get_root_cause = cursor.fetchall()
            for root_cause in get_root_cause:
                list_of_root_cause.append(root_cause[0])   
            
            if list_of_root_cause:
                return create_json('success', list_of_root_cause)
            else:
                return create_json('internal error', "DATA NOT FOUND.")

        except Exception as error:
            print(error)





class viewLayer1(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name', 'student_email']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT curriculum_name
                                FROM school_info
                                WHERE school_name = %s ''',(request_json['school_name']))
            curriculum_name = cursor.fetchone()
            
            cursor.execute('''SELECT class_year
                                FROM assessment_request
                                WHERE email = %s ''',(request_json['student_email']))
            class_year = cursor.fetchone()

            cursor.execute('''SELECT COUNT(*)
                                FROM category_of_concerns
                                WHERE (class_year = %s and curriculum_name = %s) or class_year='All Year' ''',(class_year[0], curriculum_name[0]))
            school_check = cursor.fetchone()
            final_dictionary = {}
            if school_check[0] != 0:
                cursor.execute('''SELECT DISTINCT (category_of_concerns)
                                    FROM category_of_concerns
                                    WHERE (class_year = %s and curriculum_name = %s) or class_year='All Year' ''',(class_year[0], curriculum_name[0]))
                category_of_concerns_data = cursor.fetchall()
                final_list = []

                for category_of_concerns in category_of_concerns_data:
                    category_of_concerns = category_of_concerns[0]
                    
                    category_dictionary = {}

                    cursor.execute('''SELECT DISTINCT subcategory_of_concerns
                                        FROM category_of_concerns
                                        WHERE category_of_concerns = %s ''',(category_of_concerns))
                    subcategory_of_con = cursor.fetchall()
                    
                    category_dictionary["value"] = category_of_concerns
                    category_dictionary["label"] = category_of_concerns
                    # final_dictionary.update(category_dictionary)
                    

                    subcategory_dictionary = {}
                    updated_subcategory_list = []
                    
                    for subcategory in subcategory_of_con:
                        updated_subcategory_dictionary = {}

                        cursor.execute('''SELECT DISTINCT layer1
                                        FROM category_of_concerns
                                        WHERE subcategory_of_concerns = %s ''',(subcategory[0]))
                        layer1_data = cursor.fetchall()
                        
                        subcategory_dictionary["value"] = subcategory[0]
                        subcategory_dictionary["label"] = subcategory[0]

                        layer1_dictionary = {}
                        updated_layer1_list = []

                        for layer_1 in layer1_data:
                            updated_layer1_dictionary = {}
                            cursor.execute('''SELECT DISTINCT layer2
                                        FROM category_of_concerns
                                        WHERE layer1 = %s ''',(layer_1[0]))
                            layer2_data = cursor.fetchall()

                            layer1_dictionary["value"] = layer_1[0]
                            layer1_dictionary["label"] = layer_1[0]

                           
                            updated_layer2_list = []

                            for layer_2 in layer2_data:
                                layer2_dictionary = {}

                                layer2_dictionary["value"] = layer_2[0]
                                layer2_dictionary["label"] = layer_2[0]
                                updated_layer2_list.append(layer2_dictionary)
                            # print(updated_layer2_list)

                            layer1_dictionary["children"] = updated_layer2_list
                            updated_layer1_dictionary.update(layer1_dictionary)
                            updated_layer1_list.append(updated_layer1_dictionary)

                        subcategory_dictionary["children"] = updated_layer1_list
                        updated_subcategory_dictionary.update(subcategory_dictionary)
                        updated_subcategory_list.append(updated_subcategory_dictionary)

                    category_dictionary["children"] = updated_subcategory_list

                    final_dictionary.update(category_dictionary)
                    final_list.append(json.dumps(final_dictionary))
                print(final_list)
                return create_json('success', final_list)
            else:
                return create_json('internal error', "DATA NOT FOUND.")
        except Exception as error:
            print(error)



class insertShareSchool(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['source', 'destinations'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        source = request_json['source']
        destinations = request_json['destinations']

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('''Select share_data from school_info where school_name=%s''',(source))
        share_data_check = cursor.fetchone()
        
        if share_data_check[0] == 'yes':
            
            for destination in destinations:
                cursor.execute('''Insert into share_data(source, destination)
                                VALUES (%s, %s)
                                ''', (source, destination)
                            )
                conn.commit()
                cursor.execute('''Select COUNT(*) from share_data where source=%s and destination=%s''',(source, destination))

                record = cursor.fetchone()
                print(record)
                if not record or record[0] == 0:
                    return create_json('no records', "data not inserted")
        
        result = create_json('success', 'data insertion successful')
        return result

class viewShareSchool(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['source'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        source = request_json['source']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute('''Select * from share_data where source=%s''',(source))

        record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        print(record)
        if not record or record[0] == 0:
            return create_json('no records', "no records found")
        result = create_json('success', record)
        return result

class deleteShareSchool(Resource):
    def post(self):
        request_json = request.get_json()

        request_verification = param_verfication(request_json, ['source', 'destination'])
        if codes[request_verification] != '200':
            return create_json('invalid request', "invalid request")

        source = request_json['source']
        destination = request_json['destination']

        conn = mysql.connect()
        cursor = conn.cursor()

        cursor.execute('''Delete from share_data where source=%s and destination=%s''',(source, destination))
        conn.commit()
        cursor.execute('''Select COUNT(*) from share_data where source=%s and destination=%s''',(source, destination))

        record = cursor.fetchone()
        print(record)

        if not record or record[0] == 0:
            return create_json('success', "record deleted")
        result = create_json('database error', "bad request")
        return result





class CreateTeacherStrategyRating(Resource):
    def post(self):
        request_json_list = request.get_json()
        mandate_param = [ 'teacher'
                        , 'student'
                        , 'strategy_id' 
                        , 'effort' 
                        , 'efficiency']
        for request_json in request_json_list:
            for element in mandate_param:
                if element not in request_json:
                    return create_json('invalid request', "invalid request11")
            try:
                conn = mysql.connect()
                cursor = conn.cursor()

                mandata_param_value = []
                for element in mandate_param:
                    mandata_param_value.append(request_json[element])
                cursor.execute('''INSERT INTO teacher_strategy_rating(teacher, student, strategy_id, effort, efficiency)
                                    VALUES (%s, %s, %s, %s, %s) ''',
                                    (request_json['teacher'],
                                    request_json['student'],
                                    request_json['strategy_id'],
                                    request_json['effort'],
                                    request_json['efficiency']))
                conn.commit()
                cursor.execute('''Select count(*)
                                    from strategies_adjustments
                                    where adjustment_id = %s''',(request_json['strategy_id'],))
                id_check = cursor.fetchone()
                if id_check[0] == 0:
                    cursor.execute('''SELECT strategy_id, effort, efficiency FROM teacher_strategy_rating WHERE strategy_id=%s''',
                                (request_json['strategy_id']))
                    val = cursor.fetchone()
                    print(val)
                    a = val[0]
                    b = val[1]
                    c = val[2]
                    cursor.execute('''INSERT INTO strategies_adjustments(adjustment_id, effort, efficiency)
                    VALUES (%s,%s,%s)''', (a,b,c))
                    conn.commit()
                else:
                    cursor.execute('''SELECT avg(effort), avg(efficiency) from teacher_strategy_rating where strategy_id=%s''',
                                (request_json['strategy_id']))
                    value = cursor.fetchone()
                    print(value)
                    V1 = round(value[0])
                    V2= round(value[1])
                    print(V1, V2)
                    cursor.execute('''UPDATE tollow.strategies_adjustments SET effort="%s", efficiency=%s WHERE adjustment_id = "%s" ;''',
                                (V1, V2, request_json['strategy_id']))
                    conn.commit()
                cursor.execute('''Select count(*)
                                    from teacher_strategy_rating
                                    where teacher = %s and student = %s and strategy_id = %s and effort = %s and efficiency = %s ''',
                                    (request_json['teacher'], request_json['student'],request_json['strategy_id'],
                                    request_json['effort'], request_json['efficiency']))
                record = cursor.fetchone()
                
                if record[0] != 0:  
                    continue           
                    
                else:
                    return create_json('internal error', "internal error12") 
            
            except Exception as error:
                print(error)
        return create_json('success', "Teacher Strategy Rating Created successfully.")

class CreateTargetedOutcome(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'student'
                        , 'teacher'
                        , 'school_name' 
                        , 'assessment_related_to_targeted_outcome' 
                        , 'assessment_result', 'category_of_concern', 'percent', 'creation_date']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            ##### Check student

            cursor.execute('''Select count(*)
                                from assessment_related_to_targeted_outcome 
                                where teacher = %s and student = %s and creation_date = %s ''',(request_json['teacher'], request_json['student'],request_json['creation_date']))
            record_check = cursor.fetchone()
            
            if record_check[0] == 0:
                cursor.execute('''INSERT INTO assessment_related_to_targeted_outcome(student, teacher, school_name, assessment_related_to_targeted_outcome, assessment_result, category_of_concern, percent)
                                    VALUES (%s, %s, %s, %s, %s, %s, %s) ''',
                                    (request_json['student'], 
                                    request_json['teacher'],
                                    request_json['school_name'],
                                    request_json['assessment_related_to_targeted_outcome'],
                                    request_json['assessment_result'],
                                    request_json['category_of_concern'],
                                    request_json['percent'])
                                )
                conn.commit()
                cursor.execute('''Select count(*)
                                    from assessment_related_to_targeted_outcome 
                                    where teacher = %s and student = %s and assessment_related_to_targeted_outcome = %s and school_name = %s and assessment_result = %s and category_of_concern = %s and percent = %s''',(request_json['teacher'], request_json['student'],request_json['assessment_related_to_targeted_outcome'],request_json['school_name'], request_json['assessment_result'],request_json['category_of_concern'],request_json['percent']))
                record = cursor.fetchone()
                
                if record[0] != 0:             
                    return create_json('success', "Targeted Outcome Created successfully.")
                else:
                    return create_json('internal error', "internal error")
            
            else:    
                cursor.execute('''UPDATE assessment_related_to_targeted_outcome
                                    SET assessment_related_to_targeted_outcome = %s, assessment_result = %s, category_of_concern = %s, percent = %s
                                    Where student = %s AND teacher = %s AND creation_date = %s  ''',
                                    (request_json['assessment_related_to_targeted_outcome'],
                                    request_json['assessment_result'],
                                    request_json['category_of_concern'],
                                    request_json['percent'],
                                    request_json['student'], 
                                    request_json['teacher'],
                                    request_json['creation_date'])
                                )
                conn.commit()
                cursor.execute('''Select count(*)
                                    from assessment_related_to_targeted_outcome 
                                    where teacher = %s and student = %s and assessment_related_to_targeted_outcome = %s and school_name = %s and assessment_result = %s and category_of_concern = %s and percent = %s''',(request_json['teacher'], request_json['student'],request_json['assessment_related_to_targeted_outcome'],request_json['school_name'], request_json['assessment_result'], request_json['category_of_concern'],request_json['percent']))
                record = cursor.fetchone()
                
                if record[0] != 0:             
                    return create_json('success', "Targeted Outcome Updated successfully.")
                else:
                    return create_json('internal error', "internal error") 
        except Exception as error:
            print(error)

class FindStrategiesAdjustments(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element]) 
            cursor.execute('''SELECT strategies_adjustment
                                FROM step3_key_outcome
                                WHERE email = %s ''',(request_json['email']))
            strategies_adjustment_id = cursor.fetchall()
            # email = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            values = []
            list_of_strategies_adjustment = []
            for strategies_adjustment in strategies_adjustment_id:
                temp=eval(strategies_adjustment[0])
                temp=[j for i in temp for j in i]
                for id in temp:
                    list_of_strategies_adjustment.append(id)

           
            values = list(set(list_of_strategies_adjustment))
            
            
            final_list = []
            for strategies_adjustment_values in values:
                cursor.execute('''SELECT adjustment_id,title, subtitle 
                                    FROM `strategies_adjustments` 
                                    WHERE adjustment_id = %s ''',(strategies_adjustment_values))
                # strategies_adjustment_final_values = cursor.fetchall()
                strategies_adjustment_final_values = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                final_list.append(strategies_adjustment_final_values[0])
                print(strategies_adjustment_values,strategies_adjustment_final_values[0])
            return create_json('success', final_list)   
        except Exception as error:
            print(error)

class CreateRecordEvidence(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'teacher'
                        , 'student'
                        , 'school_name' 
                        , 'record_evidence', 'creation_date' ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            ##### Check student
            
            cursor.execute('''Select count(*)
                                from record_evidence 
                                where teacher = %s and student = %s and  creation_date = %s ''',(request_json['teacher'], request_json['student'],request_json['creation_date']))
            record_check = cursor.fetchone()
            if record_check[0] == 0:
                cursor.execute('''INSERT INTO record_evidence(teacher, student, school_name, record_evidence)
                                    VALUES (%s, %s, %s, %s) ''',
                                    (request_json['teacher'], 
                                    request_json['student'],
                                    request_json['school_name'],
                                    request_json['record_evidence'])
                                )
                conn.commit()
                cursor.execute('''Select count(*)
                                    from record_evidence 
                                    where teacher = %s and student = %s and school_name = %s and record_evidence = %s ''',(request_json['teacher'], request_json['student'],request_json['school_name'],request_json['record_evidence']))
                record = cursor.fetchone()

                if record[0] != 0:             
                    return create_json('success', "Record Evidence Created successfully.")
                else:
                    return create_json('internal error', "internal error")
            
            else:
                cursor.execute('''UPDATE record_evidence
                                    SET  record_evidence = %s
                                    where teacher= %s AND student = %s AND creation_date = %s''',
                                    (request_json['record_evidence'],
                                        request_json['teacher'], 
                                        request_json['student'],
                                        request_json['creation_date'])
                                )
                conn.commit()
                cursor.execute('''Select count(*)
                                    from record_evidence 
                                    where teacher = %s and student = %s and school_name = %s and record_evidence = %s ''',(request_json['teacher'], request_json['student'],request_json['school_name'],request_json['record_evidence']))
                record = cursor.fetchone()
            
                if record[0] != 0:             
                    return create_json('success', "Record Evidence updated successfully.")
                else:
                    return create_json('internal error', "internal error") 
                    
        except Exception as error:
            print(error)


class TeacherViewKeyOutcome(Resource):
    def post(self):
        request_json = request.get_json()
        param = [
            'tag_teachers',
            'email',
        ]
        for p in param:
            if p not in request_json:
                return create_json('invalid request', "invalid request")

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            teacher = '%'+request_json['tag_teachers']+'%'
            cursor.execute('''SELECT *
                                FROM step3_key_outcome
                                WHERE email = %s and tag_teachers LIKE %s''',(request_json['email'], teacher))
            record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            record_list=[]
            if not record or record[0] == 0:
                return create_json('no records', "no records found")
            for record in record:
                record_dict={}
                if record:
                    for key, val in record.items():
                        if (key == 'created_date' or key == 'review_date' or key == 'date_of_birth') and type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = eval(str(val)) if (val and str(val)[0]=="[") else val
                    record_list.append(record_dict)
            result = create_json('success', record_list)
            return result
        except Exception as e:
            print(e)

class LessonModification(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'student'
                        , 'teacher'
                        , 'school_name'
                        , 'lesson_modifications'
                        ]
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        other_students = request_json['other_students']
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO lesson_modifications(student, teacher, school_name, lesson_modification)
                                VALUES (%s, %s, %s, %s)''',
                                (request_json['student'],
                                request_json['teacher'],
                                request_json['school_name'],
                                request_json['lesson_modifications'],
                                )
                            )
            conn.commit()
            if len(other_students) != 0:
                print('ok')
                for students in other_students:
                    cursor.execute('''INSERT INTO lesson_modifications(student, teacher, school_name, lesson_modification)
                                VALUES (%s, %s, %s, %s)''',
                                (students,
                                request_json['teacher'],
                                request_json['school_name'],
                                request_json['lesson_modifications'],
                                )
                            )
                    conn.commit()
            cursor.execute('''Select count(*)
                                from lesson_modifications
                                where student = %s and teacher = %s and school_name=%s and lesson_modification=%s '''
                                ,(request_json['student'],
                                request_json['teacher'],
                                request_json['school_name'],
                                request_json['lesson_modifications'],
                                ))

            record = cursor.fetchone()
            if record[0] != 0:
                return create_json('success', 'record created')
            else:
                return create_json('internal error', "insertion failed")
        except Exception as error:
            print(error)

class UILogs(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'page'
                        , 'status'
                        ]
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''INSERT INTO ui_logs(page, status)
                                VALUES (%s, %s)''',
                                (request_json['page'],
                                request_json['status'],
                                )
                            )
            conn.commit()
            cursor.execute('''Select count(*)
                                from ui_logs
                                where page = %s and status = %s ''',(request_json['page'], request_json['status'],))
            record = cursor.fetchone()
            #### Get the key outcome id
            if record[0] != 0:
                return create_json('success', 'record created')
            else:
                return create_json('internal error', "insertion failed")
        except Exception as error:
            return {"error":error}
  
  
 
 
class ListingOfLessonPlan(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['school_name'
                        ,'email']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                    mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT *
                                FROM lesson_plan
                                WHERE school_name = %s  and email = %s ''',(request_json["school_name"], request_json["email"]))
            # logger.info("SQL query successful")
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            list_of_record = []
            if not records:
                # logger.info("no records found")
                return create_json('no records', "no records")

            for record in records:
                record_dict = {}
                if record:
                    for key, val in record.items():
                        if (key == 'date' or key == 'creation_date') and type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = val
                    list_of_record.append(record_dict)
            result = create_json('success', list_of_record)
            # logger.info("records returned")
            return result
            
        except Exception as error:
            # logger.error("exception occured")
            print(error)
            
            
class updateLessonPlan(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'lesson_id'
                        , 'email'
                        , 'school_name'
                        , 'topic'
                        , 'key_learning_outcomes'
                        , 'date'
                        , 'prior_knowledge'
                        , 'how_will_new_concepts_be_modelled_and_expalined'
                        , 'how_will_concepts_be_practiced_or_knowledge_applied'
                        , 'activities'
                        , 'homework'
                        , 'assessment'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            ##### Check Student
            cursor.execute('''SELECT COUNT(*)
                                FROM lesson_plan
                                WHERE lesson_id = %s ''',(request_json['lesson_id']))
        
            lesson_id_check = cursor.fetchone()
            if lesson_id_check[0] == 1:
                cursor.execute('''UPDATE lesson_plan
                                   SET email = %s, 
                                        school_name = %s, 
                                        topic = %s, 
                                        key_learning_outcomes = %s, 
                                        date = %s, 
                                        prior_knowledge = %s, 
                                        how_will_new_concepts_be_modelled_and_expalined = %s, 
                                        how_will_concepts_be_practiced_or_knowledge_applied = %s, 
                                        activities = %s, 
                                        homework = %s, 
                                        assessment = %s    
                                    where lesson_id = %s ''',
                                    (request_json['email'], 
                                    request_json['school_name'],
                                    request_json['topic'],
                                    request_json['key_learning_outcomes'],
                                    request_json['date'],
                                    request_json['prior_knowledge'],
                                    request_json['how_will_new_concepts_be_modelled_and_expalined'],
                                    request_json['how_will_concepts_be_practiced_or_knowledge_applied'],
                                    request_json['activities'],
                                    request_json['homework'],
                                    request_json['assessment'], 
                                    request_json['lesson_id'])
                                )
                conn.commit()
                print(True)
                cursor.execute('''SELECT COUNT(*)
                                    FROM lesson_plan
                                    WHERE email = %s AND school_name = %s AND topic = %s AND key_learning_outcomes = %s AND date = %s AND prior_knowledge = %s AND how_will_new_concepts_be_modelled_and_expalined = %s AND how_will_concepts_be_practiced_or_knowledge_applied = %s AND activities = %s AND homework = %s AND assessment = %s''',
                                    (request_json['email'], 
                                    request_json['school_name'],
                                    request_json['topic'],
                                    request_json['key_learning_outcomes'],
                                    request_json['date'],
                                    request_json['prior_knowledge'],
                                    request_json['how_will_new_concepts_be_modelled_and_expalined'],
                                    request_json['how_will_concepts_be_practiced_or_knowledge_applied'],
                                    request_json['activities'],
                                    request_json['homework'],
                                    request_json['assessment']))
                record = cursor.fetchone()
                print(record)
                if record[0] != 0:             
                    return create_json('success', "Lesson Plan is Updated Successfully.")
                else:   
                    return create_json('internal error', "internal error") 
                 
        except Exception as error:
            print(error)          

 
class viewLessonPlan(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['lesson_id'
                       ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT *
                                FROM lesson_plan
                                WHERE lesson_id = %s  ''',(request_json["lesson_id"]))
            # logger.info("SQL query successful")
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchone()]
            list_of_record = []
            if not records:
                
                # logger.info("no records found")
                return create_json('no records', "no records")

            for record in records:
                record_dict = {}
                if record:
                    for key, val in record.items():
                        if (key == 'date' or key == 'creation_date') and type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = val
                    list_of_record.append(record_dict)
            result = create_json('success', list_of_record)
            # logger.info("records returned")
            return result
            
        except Exception as error:
            # logger.error("exception occured")
            print(error)
 
 
 
class CreateLessonPlan(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email'
                        , 'school_name'
                        , 'topic'
                        , 'key_learning_outcomes'
                        , 'date'
                        , 'prior_knowledge'
                        , 'how_will_new_concepts_be_modelled_and_expalined'
                        , 'how_will_concepts_be_practiced_or_knowledge_applied'
                        , 'activities'
                        , 'homework'
                        , 'assessment'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            ##### Check Student
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE role = 'Teacher' and email = %s and school_name = %s ''',(request_json['email'], request_json['school_name']))
        
            Teacher_check = cursor.fetchone()
            #print(student_check)
            
            if Teacher_check[0] == 1:
                
                cursor.execute('''INSERT INTO lesson_plan(email, school_name, topic, key_learning_outcomes, date, prior_knowledge, how_will_new_concepts_be_modelled_and_expalined, how_will_concepts_be_practiced_or_knowledge_applied, activities, homework, assessment )    
                                VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ''',
                                    (request_json['email'], 
                                    request_json['school_name'],
                                    request_json['topic'],
                                    request_json['key_learning_outcomes'],
                                    request_json['date'],
                                    request_json['prior_knowledge'],
                                    request_json['how_will_new_concepts_be_modelled_and_expalined'],
                                    request_json['how_will_concepts_be_practiced_or_knowledge_applied'],
                                    request_json['activities'],
                                    request_json['homework'],
                                    request_json['assessment'])
                                )
                conn.commit()
                print(True)
                cursor.execute('''SELECT COUNT(*)
                                    FROM lesson_plan
                                    WHERE email = %s AND school_name = %s AND topic = %s AND key_learning_outcomes = %s AND date = %s AND prior_knowledge = %s AND how_will_new_concepts_be_modelled_and_expalined = %s AND how_will_concepts_be_practiced_or_knowledge_applied = %s AND activities = %s AND homework = %s AND assessment = %s''',
                                    (request_json['email'], 
                                    request_json['school_name'],
                                    request_json['topic'],
                                    request_json['key_learning_outcomes'],
                                    request_json['date'],
                                    request_json['prior_knowledge'],
                                    request_json['how_will_new_concepts_be_modelled_and_expalined'],
                                    request_json['how_will_concepts_be_practiced_or_knowledge_applied'],
                                    request_json['activities'],
                                    request_json['homework'],
                                    request_json['assessment']))
                record = cursor.fetchone()
                print(record)
                if record[0] != 0:             
                    return create_json('success', "Lesson Plan is Created Successfully.")
                else:   
                    return create_json('internal error', "internal error") 
                 
        except Exception as error:
            print(error)
 
 
class targetedOutcome(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['teacher'
                        , 'school_name'
                        ]
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        teacher = request_json['teacher']
        school_name = request_json['school_name']
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''Select COUNT(*)
                                from user_info as i
                                where i.email = %s and i.school_name=%s and i.role="Teacher"'''
                                ,(teacher,
                                school_name,))
            teacher_check = cursor.fetchone()
            if teacher_check[0]>0:
                cursor.execute('''Select DISTINCT student
                                    from assessment_related_to_targeted_outcome
                                    where teacher = %s and school_name=%s'''
                                    ,(teacher,
                                    school_name,))
                record = cursor.fetchall()
                list1 = []
                for i in range(len(record)):
                    cursor.execute('''Select CONCAT(first_name," ", last_name)
                                    from user_info
                                    where email = %s'''
                                    ,(record[i][0],))
                    student_name = cursor.fetchone()
                    cursor.execute('''Select creation_date, assessment_result
                                    from assessment_related_to_targeted_outcome
                                    where student = %s'''
                                    ,(record[i][0],))
                    rec =  cursor.fetchall()
                    date_list = []
                    value_list = []
                    for date, value in rec:
                        if type(date) != str:
                            date = date.strftime("%d-%m-%Y")
                        date_list.append(date)
                        value_list.append(value)
                    values = {
                        "student": student_name[0],
                        "date_list": date_list,
                        "values": value_list
                    }
                    list1.append(values)
                result = create_json('success', list1)
                return result
            return create_json('no records', "no records")
        except Exception as error:
                print(error)
 
 
 
 
class ListRecordEvidence(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'teacher'
                        , 'school_name' ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''select record.student, record.teacher, record.record_evidence, record.file, record.creation_date, user.first_name,user.last_name
                                From record_evidence as record, user_info as user 
                                where record.teacher= %s and record.school_name = %s and record.student=user.email''',(request_json['teacher'], request_json['school_name'])
                            )
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            list_of_record = []
            if not records:
                
                # logger.info("no records found")
                return create_json('no records', "no records")

            for record in records:
                record_dict = {}
                if record:
                    for key, val in record.items():
                        if key == 'creation_date' and type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = val
                    list_of_record.append(record_dict)
            result = create_json('success', list_of_record)
            # logger.info("records returned")
            return result
        except Exception as error:
            print(error)
 
 
class createUnitPlan(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['unit_topic',
                        'key_learning_outcomes',
                        'start_date',
                        'end_date',
                        'model_explain_new_concepts',
                        'practice_concepts_apply_knowledge',
                        'lesson_activity_1',
                        'lesson_activity_2',
                        'homework',
                        'assessment',
                        'teacher_email',
                        'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''SELECT COUNT(*)
                                FROM user_info
                                WHERE email = %s and school_name = %s and role = 'Teacher' ''',(request_json['teacher_email'], request_json['school_name']))

            teacher_check = cursor.fetchone()
            if teacher_check[0] == 1:
                cursor.execute(''' INSERT INTO unit_plan (unit_topic,key_learning_outcomes,start_date,end_date,model_explain_new_concepts,practice_concepts_apply_knowledge,lesson_activity_1,lesson_activity_2,homework,assessment,teacher_email,school_name) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) '''
                                                                      ,(request_json['unit_topic']
                                                                      , request_json['key_learning_outcomes']
                                                                      , request_json['start_date']
                                                                      , request_json['end_date']
                                                                      , request_json['model_explain_new_concepts']
                                                                      , request_json['practice_concepts_apply_knowledge']
                                                                      , request_json['lesson_activity_1']
                                                                      , request_json['lesson_activity_2']
                                                                      , request_json['homework']
                                                                      , request_json['assessment']
                                                                      , request_json['teacher_email']
                                                                      , request_json['school_name']))
                conn.commit()
                cursor.execute('''SELECT COUNT(*)
                                    FROM unit_plan
                                    WHERE teacher_email = %s and school_name = %s and unit_topic=%s''',
                                    (request_json['teacher_email']
                                     , request_json['school_name']
                                     , request_json['unit_topic']))
                records = cursor.fetchone()
                if records[0] != 0:
                    return create_json('success', 'Unit Plan Created Successfully.')
                else:
                    return create_json('invalid request', "invalid request")

        except Exception as error:
            print(error)


class updateUnitPlan(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['id',
                        'unit_topic',
                        'key_learning_outcomes',
                        'start_date',
                        'end_date',
                        'model_explain_new_concepts',
                        'practice_concepts_apply_knowledge',
                        'lesson_activity_1',
                        'lesson_activity_2',
                        'homework',
                        'assessment',
                        'teacher_email',
                        'school_name']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''SELECT COUNT(*)
                                FROM unit_plan
                                WHERE id = %s ''',(request_json['id']))

            unit_id_check = cursor.fetchone()
            if unit_id_check[0] == 1:
                cursor.execute(''' UPDATE unit_plan
                                    SET unit_topic=%s, key_learning_outcomes=%s,
                                    start_date=%s, end_date=%s, model_explain_new_concepts=%s,
                                    practice_concepts_apply_knowledge=%s, lesson_activity_1=%s,
                                    lesson_activity_2=%s, homework=%s, assessment=%s,
                                    teacher_email=%s, school_name=%s
                                    WHERE id = %s ''',(request_json['unit_topic']
                                                    , request_json['key_learning_outcomes']
                                                    , request_json['start_date']
                                                    , request_json['end_date']
                                                    , request_json['model_explain_new_concepts']
                                                    , request_json['practice_concepts_apply_knowledge']
                                                    , request_json['lesson_activity_1']
                                                    , request_json['lesson_activity_2']
                                                    , request_json['homework']
                                                    , request_json['assessment']
                                                    , request_json['teacher_email']
                                                    , request_json['school_name']
                                                    , request_json['id']))
                conn.commit()
                cursor.execute('''SELECT COUNT(*)
                                    FROM unit_plan
                                    WHERE id = %s and unit_topic = %s ''',(request_json['id'], request_json['unit_topic']))
                records = cursor.fetchone()
                if records[0] != 0:
                    return create_json('success', 'Lesson unit Updated Successfully.')
                else:
                    return create_json('invalid request', "invalid request")

        except Exception as error:
            print(error)


class viewUnitPlan(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'school'
                        , 'teacher_email'
                        ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''SELECT *
                                FROM unit_plan
                                WHERE school_name = %s AND teacher_email = %s ''',(request_json['school'], request_json['teacher_email']))

            # records = cursor.fetchall()
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            record_list=[]
            if not records or records[0] == 0:
                return create_json('no records', "no records found")
            for record in records:
                record_dict = {}
                for key, val in record.items():
                    if key == 'created_date' or key=='start_date' or key=='end_date':
                        record_dict[key] = val.strftime("%d-%m-%Y")
                        
                    else:
                        record_dict[key] = val
                record_list.append(record_dict)
            result = create_json('success', record_list)
            return result
        except Exception as error:
            print(error)

class deleteUnitPlan(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['id']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(''' DELETE
                                FROM `unit_plan`
                                WHERE id = %s ''',(request_json['id']))
            conn.commit()
            cursor.execute('''SELECT COUNT(*)
                                FROM unit_plan
                                WHERE id = %s ''',(request_json['id']))
            records = cursor.fetchone()
            print(records)
            if records[0] == 0:
                return create_json('success', 'Lesson unit Deleted Successfully.')
            else:
                return create_json('invalid request', "invalid request")

        except Exception as error:
            print(error)

class ViewAssessmentRelatedToTargetedOutcome(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'student'
                        , 'teacher'
                        , 'creation_date' ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''select id, student, teacher, school_name, assessment_related_to_targeted_outcome, assessment_result, category_of_concern, percent
                                From assessment_related_to_targeted_outcome 
                                where student= %s and teacher = %s and creation_date = %s ''',(request_json['student'], request_json['teacher'], request_json['creation_date'])
                            )
            record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            print(record)
            if record:
                return create_json('success', record)   
            else:
                 return create_json('internal error', "Data Not Found")
                
        except Exception as error:
            print(error)

class ViewLessonModifications(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'student'
                        , 'teacher'
                        , 'creation_date' ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''select id, student, teacher, school_name, lesson_modification
                                From lesson_modifications 
                                where student= %s and teacher = %s and creation_date = %s ''',(request_json['student'], request_json['teacher'], request_json['creation_date'])
                            )
            record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            print(record)
            if record:
                return create_json('success', record)   
            else:
                 return create_json('internal error', "Data Not Found")
                
        except Exception as error:
            print(error)
            
class viewRecordEvidence(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'student'
                        , 'teacher'
                        , 'creation_date' ]

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            cursor.execute('''select id, student, teacher, school_name, record_evidence, file
                                From record_evidence 
                                where student= %s and teacher = %s and creation_date = %s ''',(request_json['student'], request_json['teacher'], request_json['creation_date'])
                            )
            record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            print(record)
            if record:
                return create_json('success', record)   
            else:
                 return create_json('internal error', "Data Not Found")
                
        except Exception as error:
            print(error)
 
 
 
class CreateGeneralChat(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'sender'
                        , 'student'
                        , 'chat']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
            ##### Check Student
        
            #print(student_check)
                
            cursor.execute('''INSERT INTO general_chat(sender, student, chat, status)    
                            VALUES( %s, %s, %s, 'Not Seen') ''',
                                (request_json['sender'], 
                                request_json['student'],
                                request_json['chat']))
            conn.commit()
            print(True)
            cursor.execute('''SELECT COUNT(*)
                                FROM general_chat
                                WHERE sender = %s AND student = %s AND chat = %s AND status = "Not Seen" ''',
                                (request_json['sender'], 
                                request_json['student'],
                                request_json['chat']))
            record = cursor.fetchone()
            print(record)
            if record[0] != 0:             
                return create_json('success', "General Chat is Created Successfully.")
            else:   
                return create_json('internal error', "internal error") 
                
        except Exception as error:
            print(error)


class UpdateGeneralChat(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'chat_id'
                        , 'receiver'
                        , 'status']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
                
            cursor.execute('''UPDATE general_chat
                            SET receiver = %s, status = %s
                            Where chat_id = %s ''',
                                (request_json['receiver'], 
                                request_json['status'],
                                request_json['chat_id']))
            conn.commit()

            cursor.execute('''SELECT COUNT(*)
                                FROM general_chat
                                WHERE chat_id = %s AND receiver = %s AND status = %s ''',
                                (request_json['chat_id'], 
                                request_json['receiver'],
                                request_json['status']))
            record = cursor.fetchone()
            print(record)
            if record[0] != 0:             
                return create_json('success', "General Chat is Updated Successfully.")
            else:   
                return create_json('internal error', "internal error") 
                
        except Exception as error:
            print(error)

class ViewGeneralChatByTeacher(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['teacher']
        
        teacher = '%'+request_json['teacher']+'%'


        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
                

            cursor.execute('''SELECT email
                                FROM assessment_request
                                WHERE teacher LIKE %s ''',
                                (teacher))
            emails = cursor.fetchall()
            record_list = []

            for email in emails:
                email = email[0]
                record_dict = {}

                cursor.execute('''SELECT gen.chat_id, gen.sender, gen.receiver, gen.student, gen.chat, gen.status,gen.creation_date,user.first_name,user.last_name
                                FROM general_chat as gen,user_info as user
                                WHERE gen.student = %s and user.email=gen.sender''',(email))
                record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                
                list_of_record=[]
                for record in record:
                    record_dict1 = {}
                    if record:
                        for key, val in record.items():
                            if key == 'creation_date' and type(val) != str:
                                record_dict1[key] = val.strftime("%d-%m-%Y")
                            else:
                                record_dict1[key] = val
                        list_of_record.append(record_dict1)
                if record:
                    record_dict['student'] = email
                    record_dict['chat_record'] = list_of_record   
                       

                    record_list.append(record_dict)
            print(record_list)
            
            if record_list:             
                return create_json('success', record_list)
            else:   
                return create_json('internal error', "internal error") 
        except Exception as error:
            print(error)


class ViewGeneralChatByCoordinator(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['learning_coordinator']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
                

            cursor.execute('''SELECT email
                                FROM assessment_request
                                WHERE learning_coordinator = %s ''',
                                (request_json['learning_coordinator']))
            emails = cursor.fetchall()
            record_list = []
            

            for email in emails:
                email = email[0]
                record_dict = {}
                cursor.execute('''SELECT gen.chat_id, gen.sender, gen.receiver, gen.student, gen.chat, gen.status,gen.creation_date,user.first_name,user.last_name
                                FROM general_chat as gen,user_info as user
                                WHERE gen.student = %s and user.email=gen.sender''',(email))
                record = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
                list_of_record=[]
                for record in record:
                    record_dict1 = {}
                    if record:
                        for key, val in record.items():
                            if key == 'creation_date' and type(val) != str:
                                record_dict1[key] = val.strftime("%d-%m-%Y")
                            else:
                                record_dict1[key] = val
                        list_of_record.append(record_dict1)
                if record:
                    record_dict['student'] = email
                    record_dict['chat_record'] = list_of_record    

                    record_list.append(record_dict)
            print(record_list)

            # print(record_dict)
            if record_list:             
                return create_json('success', record_list)
            else:   
                return create_json('internal error', "internal error") 

        except Exception as error:
            print(error)

class CountOfGeneralChatByCoordinator(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['learning_coordinator']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])
                

            cursor.execute('''SELECT email
                                FROM assessment_request
                                WHERE learning_coordinator = %s ''',
                                (request_json['learning_coordinator']))
            emails = cursor.fetchall()
            record_list = []
            record_dict = {}
            for email in emails:
                email = email[0]

                cursor.execute('''SELECT COUNT(*)
                                FROM general_chat
                                WHERE student = %s and status = "Not Seen" ''',(email))
                record = cursor.fetchone()
                if record[0] == 1:
                    record_list.append(int(record[0]))
            
            record_dict['count'] = sum(record_list)
            print("Count",sum(record_list))
            if record_dict:             
                return create_json('success', sum(record_list))
            else:   
                return create_json('internal error', "internal error") 
        except Exception as error:
            print(error)
 
 
 
class listingforviewinformiep(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['email'
                        , 'view'
                        ]
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        email = request_json['email']
        
        view = request_json['view']
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''Select *
                                from {}_view_inform_iep as i
                                where i.email = %s '''.format(view)
                                ,(email,
                                ))
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            record_list=[]
            if not records or records[0] == 0:
                return create_json('no records', "no records found")
            for record in records:
                record_dict = {}
                for key, val in record.items():
                    if key == 'created_date' or key=='updated_date':
                        if type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = val
                    else:
                        record_dict[key] = val
                record_list.append({"date":record_dict['created_date'],"records":record_dict})
            
            result = create_json('success', record_list)
            return result
        except Exception as error:
                return error



class getgoalstep3(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['email']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            cursor.execute('''SELECT goal
                                FROM iep_step_3
                                WHERE email = %s ''',(request_json['email']))

            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]

            if records:
                return create_json('success', records)
            else:
                return create_json('internal error', "internal error12")
        except Exception as error:
            print(error)


class GetIEPStep3DataByEmail(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'email']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT  step3.iep_id_3, step3.transitions, step3.assesment_adjustment, step3.examination_adjustments, step3.duration_start_date,
                                    step3.duration_end_date,step3.adjustment_review_schedule,step3.student_discussion_schedule, 
                                    step3.career_discussion_schedule, step3.tag_teachers, step3.lc_email, step3.created_date, step3.goal, step2.iep_id
                                FROM iep_step_3 as step3, iep_step_2 as step2
                                WHERE step3.created_date = step2.created_date and step3.email = %s and step2.email =  %s ''',(request_json['email'], request_json['email']))
    
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            print("review",records,request_json['email'])
            record_list=[]
            for record in records:
                record_dict={}
                if record:
                    for key, val in record.items():
                        if (key == 'duration_start_date' or key == 'duration_end_date' or key == 'created_date') and type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = eval(str(val)) if (val and str(val)[0]=="[") else val
                    record_list.append(record_dict)
            result = create_json('success', record_list)
            return result

        except Exception as error:
            print(error)

class viewIEPStep2data(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['iep_id']
        print(request_json,"param")
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT *
                                FROM iep_step_2
                                WHERE iep_id = %s ''',(request_json['iep_id']))
            # logger.info("SQL query successful")
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            list_of_record = []
            if not records:
                # logger.info("no records found")
                return create_json('no records', "no records")

            for record in records:
                record_dict = {}
                if record:
                    for key, val in record.items():
                        if key == 'created_date' and type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = val
                    list_of_record.append(record_dict)
            result = create_json('success', list_of_record)
            # logger.info("records returned")
            return result
            
        except Exception as error:
            # logger.error("exception occured")
            print(error)
            
            
class viewIEPStep3data(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['iep_id_3']

        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT *
                                FROM iep_step_3
                                WHERE iep_id_3 = %s ''',(request_json['iep_id_3']))
            # logger.info("SQL query successful")
            records = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
            list_of_record = []
            if not records:
                # logger.info("no records found")
                return create_json('no records', "no records")

            for record in records:
                record_dict = {}
                if record:
                    for key, val in record.items():
                        if (key == 'created_date' or key == 'duration_start_date' or key == 'duration_end_date') and type(val) != str:
                            record_dict[key] = val.strftime("%d-%m-%Y")
                        else:
                            record_dict[key] = val
                    list_of_record.append(record_dict)
            result = create_json('success', list_of_record)
            # logger.info("records returned")
            return result
            
        except Exception as error:
            # logger.error("exception occured")
            print(error)
class Student_targetedOutcome(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = ['student']
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request11")
        student = request_json['student']
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('''Select COUNT(*)
                                from user_info as i
                                where i.email = %s and  i.role="Student" '''
                                ,(student))
            student_check = cursor.fetchone()
            if student_check[0]== 1:
                cursor.execute('''Select DISTINCT category_of_concern
                                    from assessment_related_to_targeted_outcome
                                    where student = %s '''
                                    ,(student))
                record_of_category_of_concern = cursor.fetchall()

                list1 = []
                for category_of_concern in record_of_category_of_concern:

                    cursor.execute('''Select creation_date, assessment_result
                                    from assessment_related_to_targeted_outcome
                                    where student = %s and category_of_concern = %s'''
                                    ,(student,category_of_concern[0]))
                    rec =  cursor.fetchall()
                    print(rec)
                    date_list = []
                    value_list = []
                    for date, value in rec:
                        if type(date) != str:
                            date = date.strftime("%d-%m-%Y")
                        date_list.append(date)
                        value_list.append(value)
                    values = {
                        "category_of_concern": category_of_concern[0],
                        "date_list": date_list,
                        "values": value_list
                    }
                    list1.append(values)
                result = create_json('success', list1)
                return result
            return create_json('no records', "no records")
        except Exception as error:
                print(error)
                

class softSkillList(Resource):
    def post(self):
        
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            

            cursor.execute('''SELECT DISTINCT (soft_skill)
                                FROM soft_skill''')
            soft_skill_data = cursor.fetchall()
            final_list = []
            for soft_skill in soft_skill_data:
                soft_skill = soft_skill[0]

                soft_skill_dictionary = {}

                cursor.execute('''SELECT DISTINCT subcategory
                                    FROM soft_skill
                                    WHERE soft_skill = %s ''',(soft_skill))
                subcategories = cursor.fetchall()
                
                
                soft_skill_dictionary["value"] = soft_skill
                soft_skill_dictionary["label"] = soft_skill

                updated_subcategory_list = []
                
                for subcategory in subcategories:

                    subcategory_dictionary = {}

                    cursor.execute('''SELECT DISTINCT root_cause
                                    FROM soft_skill
                                    WHERE soft_skill= %s and subcategory = %s ''',(soft_skill,subcategory[0]))
                    root_cause_data = cursor.fetchall()
                    
                    subcategory_dictionary["value"] = subcategory[0]
                    subcategory_dictionary["label"] = subcategory[0]
        
                    updated_root_cause = []
                    for root_cause in root_cause_data:
                        root_cause_dictionary = {}

                        root_cause_dictionary["value"] = root_cause[0]
                        root_cause_dictionary["label"] = root_cause[0]
                        updated_root_cause.append(root_cause_dictionary)

                    subcategory_dictionary["Children"] = updated_root_cause
                    updated_subcategory_list.append(subcategory_dictionary)
                
                soft_skill_dictionary["Children"] = updated_subcategory_list
                
                final_list.append(soft_skill_dictionary)   
            return create_json('success', final_list)
            
        except Exception as error:
            print(error)      
            
            
                 
class findEmailByParent(Resource):
    def post(self):
        request_json = request.get_json()
        mandate_param = [ 'parent'
                        ]
        
        
        for element in mandate_param:
            if element not in request_json:
                return create_json('invalid request', "invalid request")
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            mandata_param_value = []
            for element in mandate_param:
                  mandata_param_value.append(request_json[element])

            cursor.execute('''SELECT email
                            FROM assessment_request
                            WHERE parent = %s ''',(request_json['parent']))
        
            email = cursor.fetchall()
            email = email[0][0]
            return create_json('success', email)
                
        except Exception as error:
            print(error)

          
 #new
api.add_resource(CreateLessonPlan, '/create_lesson_plan/')
api.add_resource(ListingOfLessonPlan, '/listing_of_lesson_plan/')
api.add_resource(updateLessonPlan, '/update_lesson_plan/')
api.add_resource(viewLessonPlan, '/view_lesson_plan/')
api.add_resource(targetedOutcome, '/targetedOutcome/')
api.add_resource(ListRecordEvidence, '/list_record_evidence/')
api.add_resource(createUnitPlan, '/create_unit_plan/')
api.add_resource(updateUnitPlan, '/update_unit_plan/')
api.add_resource(viewUnitPlan, '/view_unit_plan/')
api.add_resource(deleteUnitPlan, '/delete_unit_plan/')
api.add_resource(ViewAssessmentRelatedToTargetedOutcome, '/view_assessment_related_to_targeted_outcome/')
api.add_resource(ViewLessonModifications, '/view_lesson_modifications/')
api.add_resource(viewRecordEvidence, '/view_record_evidence/')
api.add_resource(CreateGeneralChat, '/create_general_chat/')
api.add_resource(UpdateGeneralChat, '/update_general_chat/')
api.add_resource(ViewGeneralChatByTeacher, '/view_general_chat_by_teacher/')
api.add_resource(ViewGeneralChatByCoordinator, '/view_general_chat_by_coordinator/')
api.add_resource(CountOfGeneralChatByCoordinator, '/count_of_general_chat_by_coordinator/')
api.add_resource(listingforviewinformiep, '/listingforviewinformiep/')
api.add_resource(getgoalstep3, '/getgoalstep3/')
api.add_resource(GetIEPStep3DataByEmail, '/get_iep_step3_data/')
api.add_resource(viewIEPStep2data, '/view_iep_step_2/')
api.add_resource(viewIEPStep3data, '/view_iep_step_3/')

api.add_resource(Student_targetedOutcome, '/student_targeted_outcome/')
api.add_resource(softSkillList, '/soft_skill_list/')

api.add_resource(findEmailByParent, '/find_email_by_parent/')     
 #new
 
 
 
 
 
 
 #Cheril
  
api.add_resource(UILogs, '/ui_logs/')
api.add_resource(LessonModification, '/lesson_modifications/')
api.add_resource(TeacherViewKeyOutcome, '/teacher_view_key_outcome/')
api.add_resource(CreateRecordEvidence, '/create_record_evidence/')
api.add_resource(FindStrategiesAdjustments, '/find_strategies_adjustments/')
api.add_resource(CreateTargetedOutcome, '/create_targeted_outcome/')
api.add_resource(CreateTeacherStrategyRating, '/create_teacher_strategy_rating/')
api.add_resource(insertShareSchool, '/insertShareSchool/')
api.add_resource(viewShareSchool, '/viewShareSchool/')
api.add_resource(deleteShareSchool, '/deleteShareSchool/')
api.add_resource(viewLayer1, '/view_layer1/')
api.add_resource(getSubcategoryOfSoftskill, '/get_subcategory_of_soft_skill/')
api.add_resource(getRootCauseOfSoftskill, '/get_root_cause_of_soft_skill/')
api.add_resource(viewUpcomingOverdueReviewCount, '/view_upcoming_overdue_review_count/')
api.add_resource(viewAllReviewCount, '/view_all_review_count/')
api.add_resource(modificationForStudentData, '/modification_for_student_data/')
api.add_resource(updateModificationStudentStatus, '/update_modification_student_status/')
api.add_resource(barGraphCounts, '/bar_graph_counts/')
api.add_resource(teacherAssignStudentDetails, '/teacher_assign_student_details/')
api.add_resource(studentProfile, '/student_profile/')
api.add_resource(createFormalAssessment, '/create_formal_assessment/')
api.add_resource(viewFormalAssessment, '/view_formal_assessment/')
api.add_resource(deleteFormalAssessment, '/delete_formal_assessment/')
api.add_resource(updateFormalAssessment, '/update_formal_assessment/')
api.add_resource(viewPastIepFile, '/view_past_iep_file/')
api.add_resource(viewPastFormalAssessmentFiles, '/view_past_formal_assessment_files/')
api.add_resource(viewUpcomingOverdueReview, '/view_upcoming_overdue_review/')
api.add_resource(viewCategoryOfConcerns, '/view_category_of_concerns/')
api.add_resource(viewAllReview, '/view_all_review/')
api.add_resource(authenticateuser, '/authen/')
api.add_resource(validateUser, '/validate/')
api.add_resource(rolesDisplay, '/roles/')
api.add_resource(authorizeUser, '/accessuser/')
api.add_resource(schoolsDisplay, '/schools/')
api.add_resource(registerUser, '/userregistration/')
api.add_resource(userUpdate, '/userupdate/')
api.add_resource(TeacherCommentsUpdateInsert, '/teacher_comments_update_insert/')
api.add_resource(teacherComments, '/teachercomments/')
api.add_resource(TeacherAssessmentRequest, '/teacher_assessment_request/')
api.add_resource(schoolsCount, '/schoolscount/')
api.add_resource(schoolsDetails, '/schoolsdetails/')
api.add_resource(usersDetails, '/usersdetails/')
api.add_resource(usersCount, '/userscount/')
api.add_resource(deleteUser, '/deleteuser/')
api.add_resource(SubjectCreate, '/subject_create/')
api.add_resource(ViewSubject, '/view_subject/')
api.add_resource(studentViewReviewStatus, '/student_view_review_status/')
api.add_resource(roleDisplay, '/roledisplay/')
api.add_resource(StudentTeacherAssign, '/assignteachercoordinator/')
api.add_resource(iep_step_1_studentDetails, '/iep_step_1_studentdetails/')
api.add_resource(iep_step_1_impInfo, '/iep_step_1_importantinfo/')
api.add_resource(iep_step_1_personalInfo, '/iep_step_1_personalinfo/')
api.add_resource(iepID, '/iepid/')
api.add_resource(iepStudentDetails, '/iepstudentdetails/')
api.add_resource(impInfo, '/importantinfo/')
api.add_resource(personalInfo, '/personalinfo/')


#Zafar
api.add_resource(ViewStratergiesAdjustments, '/view_stratergies_adjustments/')
api.add_resource(StratergiesAdjustments_Create, '/create_stratergies_adjustments/')
api.add_resource(deleteStratergiesAdjustments, '/delete_stratergies_adjustments/')
api.add_resource(updateStratergiesAdjustments, '/update_stratergies_adjustments/')
api.add_resource(viewKeyOutcome, '/view_key_outcome/')
api.add_resource(updateKeyOutcome, '/update_key_outcome/')
api.add_resource(CreateKeyOutcome, '/create_key_outcome/')
api.add_resource(createSoftSkill, '/create_soft_skill/')
api.add_resource(editSoftSkill, '/edit_soft_skill/')
api.add_resource(viewSoftSkill, '/view_soft_skill/')
api.add_resource(deleteSoftSkill, '/delete_soft_skill/')
api.add_resource(registerSchool, '/registerschool/')
api.add_resource(addCurriculumcategory, '/addcategory/')
api.add_resource(curriculumDisplay, '/curriculumDisplay/')  
api.add_resource(totalStudentDetails, '/total_student_details/')
api.add_resource(activeStudentDetails, '/active_student_details/')
api.add_resource(userCount, '/userCount/')
api.add_resource(activeStudent, '/activeStudent/')
api.add_resource(getNewStudentDuration, '/get_new_student_duration/')
api.add_resource(updateNewStudentDuration, '/update_new_student_duration/')
api.add_resource(createReview, '/create_review/')
api.add_resource(editReview, '/edit_review/')
api.add_resource(viewReview, '/view_review/')
api.add_resource(deleteReview, '/delete_review/')
api.add_resource(negotiateGoal, '/negotiate_goal/')
api.add_resource(createModificationStudent, '/create_modification_student/')
api.add_resource(updateModificationStudent, '/update_modification_student/')
api.add_resource(viewModificationStudent, '/view_modification_student/')
api.add_resource(deleteModificationStudent, '/delete_modification_student/')
api.add_resource(createLessonUnit, '/create_unit_plan/')
api.add_resource(updateLessonUnit, '/update_unit_plan/')
api.add_resource(viewLessonUnit, '/view_unit_plan/')
api.add_resource(deleteLessonUnit, '/delete_unit_plan/')
api.add_resource(newStudentDetails, '/newstudentdetails/')
api.add_resource(newStudentIEP, '/studentiepcount/')
api.add_resource(studentAssessnment, '/studentassessmentcount/')
api.add_resource(populateYearLevels, '/populateyearlevels/')
api.add_resource(yearLevelData, '/yearleveldata/')
api.add_resource(mapStudentViews, '/mapstudentviews/')
api.add_resource(ViewInformIEP, '/view_info_iep/')
api.add_resource(teacherNames, '/teacherNames/')
api.add_resource(teacherTagging, '/teacherTagging/')
api.add_resource(studentvoiceupdate, '/studentvoiceupdate/')
api.add_resource(extractIEP, '/extractIEP/')
api.add_resource(reviewIEP, '/reviewIEP/')
api.add_resource(viewIEPStep3, '/view_iep_step3/')
api.add_resource(updateIEPStep3, '/update_iep_step3/')
api.add_resource(viewIEPStep2, '/view_iep_step2/')
api.add_resource(updateIEPStep2, '/update_iep_step2/')
api.add_resource(CreateIEPstep3, '/create_iep_step_3/')
api.add_resource(iepStep2, '/iepstep2_assessment_type/')
api.add_resource(roleDisplaySupportStaff, '/supportstaff/')
api.add_resource(preInformation, '/preinformation/')
api.add_resource(forgetPassword, '/forgetpassword/')
api.add_resource(createStudentViewReview, '/create_student_view_review/')
api.add_resource(createCategoryOfConcern, '/create_category_of_concern/')
api.add_resource(editCategoryOfConcern, '/edit_category_of_concern/')
api.add_resource(viewCategoryOfConcern, '/view_category_of_concern/')
api.add_resource(deleteCategoryOfConcern, '/delete_category_of_concern/')
api.add_resource(studentDetails, '/studentdetails/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
    app.run(debug=True)