package com.example.JSP_04.Controller;

import jakarta.servlet.ServletException;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;

@WebServlet(urlPatterns = "/AutoFillServlet")
public class AutoFillServlet extends HttpServlet {

    protected String n_username;

    @Override
    protected void doPost(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        resp.setContentType("text/html; charset = utf-8");

        setN_username(req.getParameter("user").trim());
        resp.getWriter().write("<script> window.top.location = 'Register.jsp'; </script>");
        resp.getWriter().flush();
        req.getSession().setAttribute("auto", getN_username().trim());
    }

    public void setN_username(String n_username) {
        this.n_username = n_username;
    }

    public String getN_username() {
        return n_username.equals("") ? "" : n_username;
    }
}
