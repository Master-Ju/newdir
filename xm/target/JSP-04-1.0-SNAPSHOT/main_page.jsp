<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>主页</title>
		<link type="text/css" rel="stylesheet" href="css/firstPage.css">
	</head>
	<body>
		<h1 style="color: #ff639a">主页</h1>
		<div style="background-color: #ec02f6">
			<h2>欢迎用户：<i><%=request.getSession().getAttribute("name")%></i>,&nbsp;&nbsp;这是主页</h2>
		</div>
	</body>
</html>