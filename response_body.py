# -*- coding: utf-8 -*-
"""
Created on Sat May  9 10:32:18 2020

@author: Administrator
"""
from json_convert import JSON_Convert
import Debug
class response(object):
	html_head ="""<html>
		<head>
		<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
		<title>{0}</title>
		</head>
		<body>"""
	html_end = """</body>
		</html>"""
	html_form = """
		<img src="https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1596114327361
		&di=ee8812de2a3ef6a1a6d72ae02053dec9&imgtype=0&
		src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com
		%2Fq_70%2Cc_zoom%2Cw_640%2Fimages%2F20180526%2F1d7717ba78dc4a02adbbff169cc1b305.jpg" /><br>
		<text>thing name:</text>
		<form action="" method="GET" >
        <input type="search" id="mysearch"><br>
		</form>
		<text>Server:</text><br>
		<select id="idState" style="width:150" name="state"
			selectedIndex = "$!{{state}}">
		<option value="0"> development</option>
		<option value="1"> staging</option>
		</select><br><br>
		<label>	Time Zone :GMT</label>
		<input type="text" id="mtimezone" placeholder="+0800" /><br>
        <input type="submit" value="提交" onclick="msearch()"><br>
		<script type="text/javascript">
		var searchInput= document.getElementById('mysearch');
		function jumpPage(){{
				var object = document.getElementById("idState");
				var midStateindex = object.selectedIndex;
				var timezone_locate = document.getElementById("mtimezone").value;
				if(timezone_locate.length==0 && timezone_locate.length<5){{
						timezone_locate="+0800";
				}}
				window.open(`http://{0}:8000/s?word=${{encodeURI(searchInput.value)}}/${{object.options[midStateindex].text}}/${{timezone_locate}}`);
		}}
		function msearch(){{
			//document.getElementById('mysearch').submit()
			searchInput.value = document.getElementById('mysearch').value;
			jumpPage();
		}}
		</script>
		"""
	html_img = """<img src="data:image/png;base64,{0}"/>
	"""
	html_srcimg = """ <img src=" https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1589959343068&di=ccebce4834ac7936cdb9735b352f8326&imgtype=0&src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20181226%2F8cd0794ecbc14a3281a1e7abac0be96f.gif " />"""
	html_holilay_txt = """<body>Happly holiday<br /></body> """
	def __init__(self,host="0.0.0.0"):
		self.base_init()
		print("__init__ host",host)
		self.host = host
	def base_init(self):
		self.response_start_line_f = "HTTP/1.1 404 Not Found\r\n"
		self.response_start_line_s = "HTTP/1.1 200 OK\r\n"
		self.response_headers = "Server: Spromise server\r\n"
	def get_index(self):
		print("host", self.host)
		response_date = self.html_head.format("SPROMISE")+self.html_form.format(self.host)+self.html_end
		response = self.response_start_line_s + self.response_headers + "\r\n" + response_date
		return bytes(response,"utf-8")
	def get_fail(self):
		Debug.DEBUG.print_err("get_fail")
		response = self.response_start_line_f + self.response_headers + "\r\n" + "thing id is not found!"
		return bytes(response,"utf-8")

class response_txt(response):
	defdevelopment = "development"
	server = ""
	def __init__(self,thing_id="0",server=defdevelopment,tz="+0800",host="0.0.0.0"):

		print("__init__ response_txt host",host)
		self.thing_id = thing_id
		self.base_init()
		self.host = host
		self.server = server
		self.tz = tz
	def get_holiday(self):
		response_date = self.html_head.format(self.thing_id)+self.html_holilay_txt+self.html_srcimg+self.html_end
		response = self.response_start_line_s + self.response_headers + "\r\n" + response_date
		return bytes(response,"utf-8")

	def get_response(self):
		print("This thing_id ",self.thing_id)
		if(self.thing_id=="ZouKeMing"):
			return self.get_holiday()
		json_convert = JSON_Convert()
		if(json_convert.init(self.server,self.tz,[self.thing_id,self.thing_id+".json"])):
			try:
				file = open(self.thing_id+".json","rb")
				file_data = file.read()
			except IOError:
				return self.get_fail()
			Debug.DEBUG.print_debug(self.thing_id+".json")

			file.close()
			response_body = file_data.decode("utf-8")
			#print("response_body ",len(response_body))
			Debug.DEBUG.print_debug("response_body")
			#print(response_body)
			response = self.response_start_line_s + self.response_headers + "\r\n" + response_body
			Debug.DEBUG.print_debug("return response")
			#print(response)
			return bytes(response,"utf-8")
		else:
			return self.get_fail()

class response_png(response_txt):
	pass
