package com.example.JSP_04.Dao;

import com.example.JSP_04.Bean.UserBean;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;

public class UserDataDAO {

    PreparedStatement prestmt;
    Connection con;
    Statement state;
    ResultSet rs;

    List<UserBean> result = new ArrayList<>();

    public List<UserBean> GetUserData() {
        try {
            con = ConnectionUtils.getConnection();
            state = con.createStatement();
            rs = state.executeQuery("SELECT * FROM `JSP-04`");
            while (rs.next()) {
                UserBean userBean = new UserBean();

                userBean.setUsername(rs.getString("Username"));
                userBean.setPassword(rs.getString("Password"));

                result.add(userBean);
            }

            rs.close();
            state.close();
            con.close();

        } catch (SQLException throwables) {
            throwables.printStackTrace();
        }
        return result;
    }

    public boolean insert(String u, String p) {
        try {
            con = ConnectionUtils.getConnection();
            prestmt = con.prepareStatement("INSERT INTO `JSP-04` VALUES(?, ?)");
            prestmt.setString(1, u);
            prestmt.setString(2, p);
            prestmt.executeUpdate();
            prestmt.close();
            con.close();
        } catch (SQLException throwables) {
            throwables.printStackTrace();
            return false;
        }
        return true;
    }
}
