<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html>
<head>
	<title>JSP - Hello World</title>
	<link rel="stylesheet" type="text/css" href="css/firstPage.css">
	<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
	<script type="text/javascript" src="js/Submit.js"></script>
</head>
<body>
<%!
	String nu;
	String res;
%>
<%
	nu = (String) request.getSession().getAttribute("nu");
	if (nu == null) {
	    res = "";
	}else {
	    res = nu;
	}
%>
<h1>登录</h1>
<br/>
<div>
	<form name="data" method="post" target="nm_iframe">
		<span>账户：</span>
		<label>
			<input class="user" id="n_user" name="user" type="text" value="<%=res%>" autocomplete="off">
		</label>
		<br>
		<br>
		<span>密码：</span>
		<label>
			<input class="password" id="n_password" name="password" type="password">
		</label>
		<br><br><br>
		<input style="margin-left: 30px" type="submit" class="button" value="登录" id="Login">
		<input style="margin-left: 15px" type="submit" class="button" value="注册" id="Register">
	</form>
	
	
	<iframe id="id_iframe" name="nm_iframe" style="display:none;"></iframe>
</div>

</body>
</html>