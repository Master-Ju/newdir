<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
	<title>JSP - Hello World</title>
	<link rel="stylesheet" type="text/css" href="css/firstPage.css">
</head>
<body>
<h1>
	<%= "Hello World!" %>
	<%= "登录"%>
</h1>
<br/>
<a href="hello-servlet">Hello Servlet</a>
<div>
	<form action="/com.example.JSP_04/Controller" method="post">
		<span>账户：</span>
		<label>
			<input class="user" id="n_user" type="text" required = "required">
		</label>
		<br>
		<br>
		<span>密码：</span>
		<label>
			<input class="password" id="n_password" name="user" type="password" required = "required">
		</label>
		<br><br>
		<input type="submit" class="button" name="password" value="注册" id="Password">
	</form>
</div>

</body>
</html>