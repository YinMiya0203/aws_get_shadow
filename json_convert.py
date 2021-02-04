# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 09:17:04 2020

@author: Administrator
"""
import sys
import json
#import time
import datetime
import os
from datetime import timezone, timedelta
#import jsonpath
import pytz
class JSON_Convert(object):
	file_path = ""
	file_out = ""
	file_out_type = ""
	file_fd = 0
	profile = "DEVELOPMENT"
	#tz = pytz.timezone('Asia/Shanghai')
	timezone_offset = False
	timezone_hours = 0
	timezone_minutes = 0;
	def load_awsshadow(self):
		linux_cmd = "aws --profile {1} iot-data  get-thing-shadow --thing-name {0} {0}.json".format(self.file_path,self.profile)
		#linux_cmd = "ls"
		tmp = os.system(linux_cmd)
		print("tmp:",tmp)
		if(tmp != 0 ):
			print("linux_cmd: ",linux_cmd)
			return False
		else :
			self.file_path = self.file_path+".json"
			return True

	def init(self,pro,tz,argv):
		self.profile = pro
		if(type(argv)==type(list())):
			self.file_path = argv[0]
			self.file_out = argv[1]
			self.file_out_type = self.file_out.split(".")[1].upper()
			if( self.file_out_type!="JSON" and self.file_out_type!="JPG"):
				print("file_out %s type unkown"%self.file_out)
				return
			self.tzgmt = tz
			if(self.tzgmt[0] == '+'):
				self.timezone_offset = True
			self.timezone_hours = int(self.tzgmt[1:3])
			self.timezone_minutes = int(self.tzgmt[3:5])
			if( not self.timezone_offset):
				self.timezone_hours = 0-self.timezone_hours
				self.timezone_minutes = 0-self.timezone_minutes
			#print("timezone hours %d minutes %d"%(self.timezone_hours,self.timezone_minutes))
		elif(type(argv)==type(str())):
			self.file_path = argv

			if(len(argv)>2):
				self.tz = pytz.timezone(argv[2])

		if("json" in self.file_path):
			print("IS file ")
		else:
			print("please load aws shadow frist")
			if(self.load_awsshadow()!=True):
				return False

		print("file_path: %s out_type %s"%(self.file_path,self.file_out_type))
		f = open(self.file_path,encoding="utf-8")
		date_json = json.load(f)
		f.close()
		#ReadContext ctx = jsonpath.parse(date_json)
		self.file_fd = open(self.file_out,"w")
		#self.write_convert("{"+"\r\n")
		self.write_convert("{"+"\r\n")
		for key in date_json:
			if(key=="state"):
				self.json_txt(date_json[key],0,date_json["metadata"])
		self.file_fd.close()
		return True

#format
	def json_txt(self,dic_json,mlevel,timestamp_json):#格式化输出
		if isinstance(dic_json,dict):#字典
			mlevel +=1
			#print("Is dic")
			#value_dictflag = bool(1)
			#self.write_convert(","+"\r\n")
			#self.write_convert("{"+"\r\n")
			for key in dic_json:
				if isinstance(dic_json[key],dict):
					if(key == "delta"):
						break;
					self.write_convert('\t' *mlevel+'"'+key+'"'+':'+'{'+"\r")
					self.json_txt(dic_json[key],mlevel,timestamp_json[key])
					#value_dictflag = bool(1) #true
				else:
					if(key == "delta"):
						break;
					dic = {}
					dic[key] = dic_json[key]
					#value_dictflag = bool(0)	#false
					self.handle_dict(dic,mlevel,timestamp_json[key])
					#TBD get timestamp
			#end dic_json
			self.write_convert('\t' *(mlevel-1)+"}"+"\r")

		else:
			print("Invaild")

	def write_convert(self,textval,out_file=file_out):
		if(self.file_out_type == "JSON"):
			self.file_fd.write(textval)

#def handle_timestamp(self,dic,mlevel):


	def handle_dict(self,dic,mlevel,timestamp_json,out_fie=file_out):
		#print("level %d is"%mlevel,dic);
		tmp_str = "\r\n"
		for key,value in dic.items():##??
			if isinstance(value,int):
				tmp_str = '\t' *mlevel+'"'+key+'"'+':'+str(value)+","
			else:
				tmp_str = '\t' *mlevel+'"'+key+'"'+':'+'"'+value+'"'+","
				#print("key",key)
				#print("timestamp_json",timestamp_json)
				#formate_t = time.strftime("%Y-%m-%d %H:%M:%S", timestamp_json["timestamp"])
				#date --date='@1586397573' "+%Y-%m-%d:%H-%M-%S"
			time_int=int(timestamp_json["timestamp"])
			#formate_t = datetime.datetime.fromtimestamp(time_int,self.tz).strftime('%Y-%m-%d %H:%M:%S')
			formate_t = datetime.datetime.fromtimestamp(time_int,timezone(timedelta(hours=self.timezone_hours,
																		   minutes=self.timezone_minutes))).strftime('%Y-%m-%d %H:%M:%S')
				#formate_t = time.strftime('%Y-%m-%d %H:%M:%S',datetime.datetime.fromtimestamp(time_int,self.tz))
			tmp_str += "#" + formate_t

			self.write_convert(tmp_str+"\r")


def main(argv):
	if(len(argv) <2):
		print("usage: input output(*.json/*.jpg) <TZ>")
		return
	print("result",JSON_Convert(argv))

if __name__ == "__main__":
	main(sys.argv[1:])
