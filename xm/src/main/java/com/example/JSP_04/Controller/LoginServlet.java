package com.example.JSP_04.Controller;


import com.example.JSP_04.Bean.UserBean;
import com.example.JSP_04.Dao.UserDataDAO;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.List;

@WebServlet(urlPatterns = "/LoginServlet")
public class LoginServlet extends HttpServlet {

    protected String username;
    protected String password;

    UserDataDAO userDataDAO = new UserDataDAO();

    boolean flag = true;


    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html; charset = utf-8");

        setUsername(req.getParameter("user").trim());
        setPassword(req.getParameter("password").trim());

        List<UserBean> userBeanList = userDataDAO.GetUserData();

        if (username.equals("")) {
            resp.getWriter().write("<script> alert('用户名不能为空！'); </script>");
        } else if (password.equals("")) {
            resp.getWriter().write("<script> alert('请输入密码！'); </script>");
        } else {
            for (UserBean userBean : userBeanList) {
                if (username.equals(userBean.getUsername())) {
                    if (password.equals(userBean.getPassword())) {
                        resp.getWriter().write("<script> alert('登录成功！'); window.top.location = 'main_page.jsp'; </script>");
                        req.getSession().setAttribute("name",userBean.getUsername());
                        resp.getWriter().flush();
                    } else {
                        resp.getWriter().write("<script> alert('密码错误！'); </script>");
                    }
                    flag = true;
                    break;
                }
                flag = false;
            }
            if (!flag) {
                resp.getWriter().write("<script> alert('用户不存在，请先注册！'); </script>");
            }
        }
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public void setPassword(String password) {
        this.password = password;
    }

}
