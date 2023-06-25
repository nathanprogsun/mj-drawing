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
  message,
} from "antd";
import { BrowserRouter as Router } from "react-router-dom";
import { QuestionCircleOutlined, PlusOutlined } from "@ant-design/icons";
import axios from "axios";
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
      textMatching: 0.5,
      imageProcessing: 1,
      imageUrl: null,
      mjLoading: true,
      mjImage: null,
      mjErr: null,
      modalVisible: false,
      exampleList: [
        "flying birds over the sea ",
        "vintage travel painting bohol china",
        "sketching cat looking at a dandelion flower with herbal colored",
      ],
      textValue: "",
      scale: "SCALE_1_1",
      triggerId: null,
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

  handleScaleChange = (e) => {
    this.setState({
      scale: e.target.value,
    });
  };

  handleUpload = async (info) => {
    const { status, response } = info.file;
    if (status === "done") {
      console.info(response);
      const code = response.code;
      if (code === 0) {
        const imageUrl = response.data.file_url;
        this.setState({ imageUrl });
        message.success("Upload success");
      } else {
        message.error(`Upload fail: ${response.message}`);
      }
    }
  };

  pollForResult = (triggerId) => {
    console.log("start pollForResult--->", triggerId);
    // 异常，请求并没有发送
    const interval = setInterval(() => {
      axios
        .get(`http://0.0.0.0:9999/api/v1/drawing/result/${triggerId}`)
        .then((resultResponse) => {
          const resp = resultResponse.data;
          console.log("(fetch result)resp-->", resp);

          if (resp.code === 0) {
            const { trigger_status, file_url, trigger_content } = resp.data;
            if (trigger_status === 2) {
              this.setState({
                mjImage: file_url,
                mjErr: null,
                mjLoading: false,
              });
              clearInterval(interval);
              message.info("Generate success");
            }
            if (trigger_status === -1) {
              this.setState({
                mjImage: null,
                mjErr: trigger_content,
              });
              clearInterval(interval);
              this.handleModalCancel();
            }
          }
        })
        .catch((resultError) => {
          console.error("fetch result->", resultError);
          clearInterval(interval);
          this.handleModalCancel();
        });
    }, 1000);
  };

  handleBtnClick = () => {
    console.info("mode->", this.state.mode);
    console.info("textMatching->", this.state.textMatching);
    console.info("imageProcessing->", this.state.imageProcessing);
    console.info("imageUrl->", this.state.imageUrl);
    console.info("textValue->", this.state.textValue);

    const modelType = this.state.mode === "custom" ? 1 : 0;

    const requestBody = {
      description: this.state.textValue,
      model: {
        model_type: modelType,
        text_match: this.state.textMatching,
        img_processing: this.state.imageProcessing,
      },
      scale_category: this.state.scale,
      reference_url: this.state.imageUrl,
    };

    axios
      .post(`http://0.0.0.0:9999/api/v1/drawing`, requestBody)
      .then((response) => {
        const resp = response.data;
        console.info("(drawing)resp->", resp);
        if (resp.code === 0) {
          const triggerId = resp.data.trigger_id;
          console.info("triggerId->", triggerId);
          this.setState({ triggerId: triggerId, modalVisible: true });
          console.info("triggerId(from state)-->", this.state.triggerId);
          this.pollForResult(triggerId);
        } else {
          message.error(response.message);
        }
      })
      .catch((error) => {
        console.log("(drawing)error--->", error.message);
        message.error(error.message);
      });
  };

  handleModalCancel = () => {
    this.setState({
      modalVisible: false,
      mjImage: null,
      mjErr: null,
      mjLoading: false,
    });
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
      triggerId,
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
                                      min={0.25}
                                      max={1}
                                      step={0.25}
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
                                      min={0.5}
                                      max={2}
                                      step={0.1}
                                      value={imageProcessing}
                                      onChange={
                                        this.handleImageProcessingChange
                                      }
                                    />
                                  </Col>
                                  <Col span={4} style={{ textAlign: "center" }}>
                                    <span>{imageProcessing}</span>
                                    <Tooltip
                                      title={`数值越大，效果图与您上传的参考图相似度越高；
                                        数值越小，效果图与您上传的参考图相似度越低；`}
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
                              defaultValue={this.state.scale}
                              size="middle"
                              onChange={this.handleScaleChange}
                              style={{
                                display: "flex",
                                flexDirection: "row",
                                justifyContent: "space-around",
                              }}
                            >
                              <Radio
                                value={"SCALE_1_1"}
                                style={{
                                  display: "flex",
                                  alignItems: "center",
                                  //  borderRadius: "4px 4px 4px 4px",
                                }}
                              >
                                <span className="span-box first-span">1:1</span>
                              </Radio>
                              <Radio
                                value={"SCALE_16_9"}
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
                                value={"SCALE_9_16"}
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
                                value={"SCALE_4_3"}
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
                                value={"SCALE_3_4"}
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
                              action={
                                "http://0.0.0.0:9999/api/v1/drawing/upload"
                              }
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
                      title={triggerId}
                      width={800}
                      height={800}
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
