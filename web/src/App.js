import React from "react";
import {
  Layout,
  Input,
  Button,
  Space,
  Col,
  Row,
  Radio,
  Slider,
  Tooltip,
  Upload,
  Modal,
  Spin,
} from "antd";
import { BrowserRouter as Router } from "react-router-dom";
import { QuestionCircleOutlined, PlusOutlined } from "@ant-design/icons";

import MJHeader from "./pages/MJHeader";

import "./App.css";

const { Content, Footer } = Layout;
const { TextArea } = Input;
const { Group } = Radio;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      mode: "custom",
      textMatching: 7.5,
      imageProcessing: 50,
      imageUrl: null,
      mjLoading: true,
      mjImage: null,
      mjErr: null,
      modalVisible: false,
      exampleList: [
        "赛博朋克风格的城市",
        "用日漫风格画一个金发少女",
        "黑白线条画风格的长城",
      ],
      textValue: "",
    };
  }

  handleModeChange = (e) => {
    this.setState({ mode: e.target.value });
  };

  handleTextMatchingChange = (value) => {
    this.setState({ textMatching: value });
  };

  handleImageProcessingChange = (value) => {
    this.setState({ imageProcessing: value });
  };

  handleUpload = (info) => {
    console.log(info.file);
    // 处理文件上传逻辑

    // 获取上传的文件对象
    const file = info.file.originFileObj;

    // 创建临时的图片 URL
    const imageUrl = URL.createObjectURL(file);

    // 更新组件状态
    this.setState({ imageUrl });
  };

  handleBtnClick = () => {
    this.setState({ modalVisible: true });

    // 模拟请求图片生成
    setTimeout(() => {
      // 假设请求成功，获得图片 URL
      const mjImage = "https://example.com/image.jpg";

      this.setState({
        mjImage: mjImage,
        mjErr: null,
        mjLoading: false,
      });
    }, 1000);
  };

  handleModalCancel = () => {
    // 关闭弹窗
    this.setState({ modalVisible: false });
  };

  handleExampleButtonClick = (content) => {
    console.log("content-->", content);
    this.setState({
      textValue: content,
    });
  };

  handleTextAreaChange = (e) => {
    this.setState({ textValue: e.target.value });
  };

  render() {
    const {
      mode,
      textMatching,
      imageProcessing,
      imageUrl,
      mjLoading,
      mjImage,
      mjErr,
      modalVisible,
      exampleList,
      textValue,
    } = this.state;

    return (
      <Router>
        <div className="APP">
          <Layout>
            <MJHeader />
            <Content
              className="site-layout"
              style={{
                padding: "0 50px",
                backgroundColor: "#fff",
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
              }}
            >
              <div className="wrapper">
                <div className="top">
                  <h1>AI绘画</h1>
                  <h2>AI绘画生成器，一款快速生成图片的智能AI画图工具</h2>
                </div>
                <div className="box">
                  <div className="area-title">画面描述:</div>
                  <div className="text-box">
                    <div className="textarea">
                      <TextArea
                        style={{ fontSize: 18 }}
                        rows={5}
                        showCount
                        maxLength={300}
                        value={textValue}
                        placeholder="请输入文本对画面进行描述，如：用维米尔的《戴珍珠耳环的少女》风格画一只海獭"
                        onChange={this.handleTextAreaChange}
                      />
                    </div>
                  </div>
                  <div className="example">
                    <div className="example-title">试一试这些:</div>
                    <div className="example-list">
                      <Space wrap>
                        {exampleList.map((content, index) => (
                          <Button
                            key={index}
                            type="dashed"
                            onClick={() =>
                              this.handleExampleButtonClick(content)
                            }
                          >
                            {content}
                          </Button>
                        ))}
                      </Space>
                    </div>
                  </div>

                  <div className="setting">
                    <Row>
                      <Col span={16}>
                        <div className="setting-box">
                          <div className="model">
                            <h1>创作模式</h1>
                            <Group
                              onChange={this.handleModeChange}
                              value={mode}
                            >
                              <Space direction="vertical">
                                <Radio value="free">
                                  自由创作
                                  <Tooltip title="如勾选此项，AI将仅参考输入的画面描述自由发挥创作">
                                    <QuestionCircleOutlined
                                      style={{ marginLeft: "4px" }}
                                    />
                                  </Tooltip>
                                </Radio>
                                <Radio value="custom">自定义参数</Radio>
                              </Space>
                            </Group>

                            {mode === "custom" && (
                              <div className="custome">
                                <Row align="middle" justify="center">
                                  <Col span={1}></Col>
                                  <Col span={5}>文本匹配程度</Col>
                                  <Col span={14}>
                                    <Slider
                                      min={0}
                                      max={10}
                                      step={0.1}
                                      value={textMatching}
                                      onChange={this.handleTextMatchingChange}
                                    />
                                  </Col>
                                  <Col span={4} style={{ textAlign: "center" }}>
                                    <span>{textMatching}</span>
                                    <Tooltip
                                      title={`数值越大，描述文本和画面内容的匹配程度越高；
                                        数值越小，描述文本和画面内容的匹配程度越低；`}
                                    >
                                      <QuestionCircleOutlined
                                      // style={{ marginLeft: "12px" }}
                                      />
                                    </Tooltip>
                                  </Col>
                                </Row>
                                <Row align="middle" justify="center">
                                  <Col span={1}></Col>
                                  <Col span={5}>图像处理程度</Col>
                                  <Col span={14}>
                                    <Slider
                                      min={0}
                                      max={100}
                                      step={1}
                                      value={imageProcessing}
                                      onChange={
                                        this.handleImageProcessingChange
                                      }
                                    />
                                  </Col>
                                  <Col span={4} style={{ textAlign: "center" }}>
                                    <span>{imageProcessing}</span>
                                    <Tooltip
                                      title={`数值越大，效果图与您上传的参考图相似度越低；
                                        数值越小，效果图与您上传的参考图相似度越高；`}
                                    >
                                      <QuestionCircleOutlined
                                      // style={{ marginLeft: "4px" }}
                                      />
                                    </Tooltip>
                                  </Col>
                                </Row>
                              </div>
                            )}
                          </div>
                          <div className="scal">
                            <h1>画布比例</h1>
                            <Group
                              name="scal-group"
                              defaultValue={1}
                              size="middle"
                              style={{
                                display: "flex",
                                flexDirection: "row",
                                justifyContent: "space-around",
                              }}
                            >
                              <Radio
                                value={1}
                                style={{
                                  display: "flex",
                                  alignItems: "center",
                                  //  borderRadius: "4px 4px 4px 4px",
                                }}
                              >
                                <span className="span-box first-span">1:1</span>
                              </Radio>
                              <Radio
                                value={2}
                                style={{
                                  display: "flex",
                                  alignItems: "center",
                                }}
                              >
                                <span className="span-box second-span">
                                  16:9
                                </span>
                              </Radio>
                              <Radio
                                value={3}
                                style={{
                                  display: "flex",
                                  alignItems: "center",
                                }}
                              >
                                <span className="span-box third-span">
                                  9:16
                                </span>
                              </Radio>
                              <Radio
                                value={4}
                                style={{
                                  display: "flex",
                                  alignItems: "center",
                                }}
                              >
                                <span className="span-box fourth-span">
                                  4:3
                                </span>
                              </Radio>
                              <Radio
                                value={5}
                                style={{
                                  display: "flex",
                                  alignItems: "center",
                                }}
                              >
                                <span className="span-box firth-span">3:4</span>
                              </Radio>
                            </Group>
                          </div>
                        </div>
                      </Col>
                      <Col span={8}>
                        <div className="reference">
                          <h1>参考图</h1>
                          <div className="reference-file">
                            <Upload
                              onChange={this.handleUpload}
                              listType="picture-card"
                              showUploadList={false}
                              className="upload-file"
                            >
                              {imageUrl ? (
                                <img
                                  src={imageUrl}
                                  alt="上传的图片"
                                  style={{ width: "100%", height: "100%" }}
                                />
                              ) : (
                                <div>
                                  <PlusOutlined />
                                  <div style={{ marginTop: 8 }}>点击上传</div>
                                </div>
                              )}
                            </Upload>
                            <span>上传图片以供AI参考</span>
                          </div>
                        </div>
                      </Col>
                    </Row>
                  </div>

                  <div className="generate">
                    <Button
                      type="primary"
                      size={"large"}
                      onClick={this.handleBtnClick}
                    >
                      生成作品
                    </Button>

                    <Modal
                      open={modalVisible}
                      onCancel={this.handleModalCancel}
                      footer={null}
                    >
                      {mjLoading ? (
                        <Spin size="large" tip="正在加载..." />
                      ) : mjErr ? (
                        <div>请求异常，请重试。</div>
                      ) : mjImage ? (
                        <img
                          src={mjImage}
                          alt="生成的图片"
                          style={{ width: "100%" }}
                        />
                      ) : null}
                    </Modal>
                  </div>
                </div>
              </div>
            </Content>

            <Footer
              style={{
                textAlign: "center",
                backgroundColor: "#f2f6fb",
                position: "fixed",
                left: 0,
                bottom: 0,
                width: "100%",
              }}
            >
              Copyright © MJ-Drawing by Jonatan2016
            </Footer>
          </Layout>
        </div>
      </Router>
    );
  }
}

export default App;
