import React from "react";
import { Layout, Menu } from "antd";
import { Link } from "react-router-dom";
import "./index.css";

const { Header } = Layout;

export default class MJHeader extends React.Component {
  render() {
    return (
      <Header
        style={{
          position: "sticky",
          top: 0,
          zIndex: 1,
          width: "100%",
          display: "flex",
          alignItems: "center",
          backgroundColor: "#fff",
          fontSize: "18px",
          color: "#333",
        }}
      >
        <div className="logo">Mj绘画大师</div>
        <Menu
          theme="light"
          mode="horizontal"
          defaultSelectedKeys={["2"]}
          className="mj-menu"
          // style={{ display: "flex", justifyContent: "center" }}
        >
          <Menu.Item style={{ margin: "0 50px" }}>
            <Link to="/">AI 创造</Link>
          </Menu.Item>
          <Menu.Item style={{ margin: "0 50px" }}>
            <Link to="/">AI 艺术馆</Link>
          </Menu.Item>
          <Menu.Item style={{ margin: "0 50px" }}>
            <Link to="/">创造指南</Link>
          </Menu.Item>
        </Menu>

        <div className="login-register">登录/注册</div>
      </Header>
    );
  }
}
