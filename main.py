#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import jinja2
import webapp2
from google.appengine.api import rdbms
from datetime import datetime
from pytz import timezone
import pytz

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

_INSTANCE_NAME="prinya-th-2013:prinya-db"

class MainHandler(webapp2.RequestHandler):
    def get(self):
    	
		templates = {

			# 'course' : cursor.fetchall(),
			# 'enroll' : cursor2.fetchall(),
			# 'status' : cursor3.fetchall(),

			}

		template = JINJA_ENVIRONMENT.get_template('course_active.html')
		self.response.write(template.render(templates))

class SearchHandler(webapp2.RequestHandler):
    def get(self):
		course_code=self.request.get('keyword');
		year=self.request.get('year');
			
		semester=self.request.get('semester');
		check_code=0
		check_fac=0
		check_dep=0
		check_year=0
		check_sem=0
		allcheck=0
		key_year=""
		key_sem=""
		code=""

		if year=="":
			check_year=0
		else:
			check_year=1
			key_year="year="+year

		if semester=="":
			check_sem=0
		else:
			check_sem=1
			key_sem="semester="+semester

		if course_code == "":
			check_code=0

		else:
			check_code=1
			code="course_code like '%"+course_code+"%' "




		data_faculity_id=self.request.get('faculity');
		data_faculity_id=str(data_faculity_id)
		data_faculity=""

		if data_faculity_id=="1":
			data_faculity = "faculity='Engineering'";
		elif data_faculity_id=="2":
			data_faculity = "faculity='Information Technology'";
		elif data_faculity_id=="3":
			data_faculity = "faculity='Business Administration'";
		elif data_faculity_id=="4":
			data_faculity = "faculity='Language'";

		if data_faculity_id =="":
			check_fac=0
		else:
			check_fac=1



		data_department=self.request.get('department');
		data_department=str(data_department)
		data_department_full=""

		if data_department=="1":
			data_department_full="department='Information Technology'"
		elif data_department=="2":
			data_department_full="department='Multimedia Technology'"
		elif data_department=="3":
			data_department_full="department='Business Information Technology'"
		elif data_department=="4":
			data_department_full="department='Accountancy'"
		elif data_department=="5":
			data_department_full="department='Industrial Management'"
		elif data_department=="6":
			data_department_full="department='International Business Management'"
		elif data_department=="7":
			data_department_full="department='Japanese Businees Administration'"
		elif data_department=="8":
			data_department_full="department='Computer Engineering'"
		elif data_department=="9":
			data_department_full="department='Production Engineering'"
		elif data_department=="10":
			data_department_full="department='Automotive Engineering'"
		elif data_department=="11":
			data_department_full="department='Electrical Engineering'"
		elif data_department=="12":
			data_department_full="department='Industrial Engineering'"
		elif data_department=="13":
			data_department_full="department='Language'"

		if data_department=="":
			check_dep=0
		else:
			check_dep=1



		where_code=" "
		a=" and "



		if check_code == 1:
			if check_code == 1:
				where_code+=code
			if check_year == 1:
				where_code+=a
				where_code+=key_year
			if check_sem == 1:
				where_code+=a
				where_code+=key_sem
			if check_fac == 1:
				where_code+=a
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_year == 1:
			if check_year == 1:
				where_code+=key_year
			if check_sem == 1:
				where_code+=a
				where_code+=key_sem
			if check_fac == 1:
				where_code+=a
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_sem == 1:
			if check_sem == 1:
				where_code+=key_sem
			if check_fac == 1:
				where_code+=a
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_fac == 1:
			if check_fac == 1:
				where_code+=data_faculity
			if check_dep==1:
				where_code+=a
				where_code+=data_department_full
		elif check_dep==1:
			if check_dep==1:
				where_code+=data_department_full
		else:
			where_code="course_id = 0"

		   	

		conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
		cursor = conn.cursor()
		sql="SELECT course_id,course_code,course_name FROM course where %s "%(where_code)
		cursor.execute(sql)
		conn.commit()


		# conn2=rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
		# cursor2 = conn2.cursor()
		# cursor2.execute('SELECT sum(capacity),sum(enroll),regiscourse_id FROM section group by regiscourse_id')
		# conn2.commit()





		templates = {

		'course' : cursor.fetchall(),
		# 'enroll' : cursor2.fetchall(),


		}

		template = JINJA_ENVIRONMENT.get_template('course_active.html')
		self.response.write(template.render(templates))

		# conn.close()
		# conn2.close()

class CourseEnrollHandler(webapp2.RequestHandler):
    def get(self):
		course_code = self.request.get('course_code');
		capacity=""
		# course_id = "BIS-101"

		conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
		cursor = conn.cursor()
		sql="SELECT * FROM course WHERE course_code = '%s'"%(course_code)
		cursor.execute(sql);

		conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
		cursor2 = conn2.cursor()
		sql2="SELECT co.course_code FROM course co,prerequsite_course pre\
		    WHERE prerequsite_id=co.course_id AND pre.course_id=\
		    (SELECT course_id FROM course WHERE course_code='%s')"%(course_code)
		cursor2.execute(sql2);
		pre_code=""
		for row in cursor2.fetchall():
		    pre_code=row[0]

		conn3 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
		cursor3 = conn3.cursor()
		sql3="SELECT sum(capacity),sum(enroll) FROM section se JOIN regiscourse re\
			ON se.regiscourse_id=re.regiscourse_id\
			join course co\
			ON co.course_id=re.course_id\
			WHERE course_code='%s'"%(course_code)
		cursor3.execute(sql3);
		enroll=""
		for capa in cursor3.fetchall():
			if capa[0]!="":
				capacity=capa[0]
			else:
				capacity=0
			if capa[1]!="":
				enroll=capa[1]
			else:
				enroll=0

		conn4 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
		cursor4 = conn4.cursor()
		sql4="SELECT section_number,CASE day WHEN '1' THEN 'Sunday'\
		    WHEN '2' THEN 'Monday'\
		    WHEN '3' THEN 'Tuesday'\
		    WHEN '4' THEN 'Wednesday'\
		    WHEN '5' THEN 'Thursday'\
		    WHEN '6' THEN 'Friday'\
		    WHEN '7' THEN 'Saturday'\
		    ELSE 'NONE' END,CONCAT(CONCAT(start_time,'-'),end_time),\
		    CASE teacher_id WHEN '1' THEN 'Tharnnapat'\
		    WHEN '2' THEN 'Teerapol'\
		    WHEN '3' THEN 'Vorachat'\
		    ELSE 'NONE' END,CONCAT(CONCAT(enroll,'/'),capacity),enroll,capacity,sec.section_id,sec.regiscourse_id  \
		from section sec JOIN section_time sct on sec.section_id=sct.section_id \
		where regiscourse_id=(select regiscourse_id from regiscourse \
			where course_id = (select course_id from course where course_code ='%s'))"%(course_code)
		cursor4.execute(sql4);



		credit=0
		conn5 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
		cursor5 = conn5.cursor()
		sql5="SELECT round(credit_lecture+(credit_lab/3),'0') FROM course WHERE course_code='%s'"%(course_code)
		cursor5.execute(sql5);
		for row2 in cursor5.fetchall():
		    credit=row2[0]
		if credit=="":
		    credit=0

		conn6 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
		cursor6 = conn6.cursor()
		sql6="SELECT re.section_id from registeredcourse re join section s on re.section_id=s.section_id join regiscourse r \
				on s.regiscourse_id=r.regiscourse_id join course c on r.course_id=c.course_id \
				where student_id=2 AND course_code='%s'"%(course_code)
		cursor6.execute(sql6);

		templates = {
			'course' : cursor.fetchall(),
			'capacity' : capacity,
		    'prerequisite_code' : pre_code,
		    'section' : cursor4.fetchall(),
		    'credit' : credit,
		    'enroll' : enroll,
		    'credit' : credit,
		    'course_code' : course_code,
		    'check' : cursor6.fetchall(),
		}
		get_template = JINJA_ENVIRONMENT.get_template('course_enroll.html')
		self.response.write(get_template.render(templates));
		conn.close();
		conn2.close();
		conn3.close();
		conn4.close();
		conn5.close();
		conn6.close();

class EnrollHandler(webapp2.RequestHandler):
    def get(self):
    	course_code = self.request.get('course_code');
    	conn = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    	cursor = conn.cursor()
        sql="SELECT round(sum(credit_lecture+(credit_lab/3)),'0')\
				from registeredcourse rec join course cou \
				ON cou.course_id=rec.regiscourse_id \
				join student stu \
				on stu.student_id=rec.student_id where rec.student_id='2'"
    	cursor.execute(sql);
    	
    	credit=0
    	for row in cursor.fetchall():
    		credit=row[0]

    	conn4 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
        cursor4 = conn4.cursor()
        sql4='SELECT maxcredit_per_semester from faculity f join student s on f.faculity_id=s.faculity_id where student_id=2'
        cursor4.execute(sql4)
        credit_total=0
        for row2 in cursor4.fetchall():
            credit_total=row2[0]

    	enroll = self.request.get('enroll');
    	enroll=int(enroll)
    	capacity = self.request.get('capacity');
    	capacity=int(capacity)
    	regiscourse_id = self.request.get('regiscourse_id');
    	regiscourse_id=int(regiscourse_id)
    	section_id = self.request.get('section_id');
    	section_id=int(section_id)

    	if credit>=credit_total:
    		self.redirect('/ErrorCredit')
    	elif enroll>=capacity:
    		self.redirect('/Error')
    	else :
    		conn2 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor2 = conn2.cursor()
        	sql2="INSERT INTO registeredcourse(student_id,regiscourse_id,section_id) values(2,'%d','%d')"%(regiscourse_id,section_id)
    		cursor2.execute(sql2);
    		conn2.commit()
    		
    		enroll=enroll+1
    		conn3 = rdbms.connect(instance=_INSTANCE_NAME, database='Prinya_Project')
    		cursor3 = conn3.cursor()
        	sql3="UPDATE section SET enroll='%d' WHERE section_id='%d' and regiscourse_id='%d'"%(enroll,section_id,regiscourse_id)
    		cursor3.execute(sql3);
    		conn3.commit()

    		conn2.close()
    		conn3.close()
    		self.redirect('http://crs-ice.appspot.com?course_code='+course_code)
    		

    	conn.close()
    	
class ErrorHandler(webapp2.RequestHandler):
    def get(self):
    	templates = {
            # 'course' : cursor.fetchall(),
        }
        get_template = JINJA_ENVIRONMENT.get_template('Error.html')
        self.response.write(get_template.render(templates));



class ErrorCreditHandler(webapp2.RequestHandler):
    def get(self):
    	templates = {
            # 'course' : cursor.fetchall(),
        }
        get_template = JINJA_ENVIRONMENT.get_template('ErrorCredit.html')
        self.response.write(get_template.render(templates));	
    	  	

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/Search', SearchHandler),
    ('/CourseEnroll', CourseEnrollHandler),
    ('/Enroll', EnrollHandler),
    ('/Error', ErrorHandler),
    ('/ErrorCredit', ErrorCreditHandler),
], debug=True)
