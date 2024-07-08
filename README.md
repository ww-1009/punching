# 企微个人打卡饱和度计算
本脚本实现个体打卡饱和度的统计计算

## 使用指南

![img1](https://raw.githubusercontent.com/ww-1009/punching/master/image/image1.jpg)

1、打开企业微信进入打卡统计页面，点击导出

![img2](https://raw.githubusercontent.com/ww-1009/punching/master/image/image2.jpg)

2、日期选择当月月初至统计日（该脚本目前只支持当月统计）

3、在脚本当前目录新建`input`文件夹，将得到的 .elsx 文件导入input文件夹中

4、运行脚本，统计数据将输出到`output`文件夹

注：当前脚本暂只生成arm64-linux的二进制文件，若有需要可自行编译
