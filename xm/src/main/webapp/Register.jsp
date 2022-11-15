<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>注册</title>
		<link rel="stylesheet" type="text/css" href="css/firstPage.css">
		
	</head>
	<body>
		<h1>注册</h1>
		<div>
			<form action="RegisterServlet" method="post">
				<span>账户：</span>
				<label>
					<input class="user" id="n_user" type="text" name="n_user" value="<%=request.getSession().getAttribute("auto")%>" required = "required" autocomplete="off">
				</label>
				<br>
				<br>
				<span>密码：</span>
				<label>
					<input class="password" id="n_password" type="password" name="n_password" required = "required">
				</label>
				<br><br>
				<span>确认：</span>
				<label>
					<input class="password" id="n_password_check" type="password" name="n_password_check" required = "required">
				</label>
				<br>
				<br>
				<input type="submit" class="button" value="注册" id="Password">
			</form>
		</div>
	</body>
</html>