package com.example.JSP_04.Controller;

import com.example.JSP_04.Dao.UserDataDAO;
import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

@WebServlet(urlPatterns = "/RegisterServlet")
public class RegisterServlet extends HttpServlet {

    private String n_username;
    private String n_Password;
    private String n_Password_check;

    UserDataDAO userDataDAO = new UserDataDAO();

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html; charset = utf-8");

        setN_username(req.getParameter("n_user").trim());
        setN_Password(req.getParameter("n_password").trim());
        setN_Password_check(req.getParameter("n_password_check"));
        System.out.println(getN_Password_check());
        if (getN_Password_check().equals(getN_Password())) {
            if (userDataDAO.insert(getN_username(), getN_Password())) {
                resp.getWriter().write("<script> alert('注册成功！'); </script>");
                resp.getWriter().write("<script> window.top.location = 'index.jsp'; </script>");
                resp.getWriter().flush();
                req.getSession().setAttribute("nu", getN_username());
            }else {
                resp.getWriter().write("<script> alert('注册失败！'); </script>");
            }
        } else {
            resp.getWriter().write("<script> alert('密码不一致'); </script>");
            resp.getWriter().write("<script> window.top.location = 'Register.jsp'; </script>");
        }
    }

    public void setN_username(String n_username) {
        this.n_username = n_username;
    }

    public void setN_Password(String n_Password) {
        this.n_Password = n_Password;
    }

    public String getN_username() {
        return n_username;
    }

    public String getN_Password() {
        return n_Password;
    }

    public String getN_Password_check() {
        return n_Password_check;
    }

    public void setN_Password_check(String n_Password_check) {
        this.n_Password_check = n_Password_check;
    }
}
