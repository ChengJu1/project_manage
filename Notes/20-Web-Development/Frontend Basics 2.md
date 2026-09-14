# 网页前端基础-2
## 一、CSS
### 1.1 CSS定义
1. CSS全称Cascading Style Sheets，层叠样式表，文件后缀为`.css`，专门用于给HTML、XML结构化文档设置视觉样式。
2. 核心作用：控制页面文字颜色、字体大小、间距、布局、背景、圆角、动画等，实现结构与样式分离，方便统一维护页面。
3. 标准语法结构：`选择器 { 属性: 属性值; 属性2: 属性值2; }`
    示例：`h1 { color: red; font-size: 14px; }`
4. CSS注释写法：`/* 注释内容 */`，注释不会被浏览器解析执行，用于代码备注、临时屏蔽样式。
最简完整示例代码
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>CSS基础示例</title>
  	<!-- 注释内容 -->
  <style>
        /* 注释：修改所有h1文字为红色 */
        h1 {
          color: red;
          border: 2px solid blue
      }
    </style>
</head>
<body>
    <h1>测试标题</h1>
</body>
</html>
```

### 1.2 CSS选择器
1. 选择器作用：精准定位页面内HTML标签，为匹配到的元素批量赋予样式。
2. 基础三类选择器对照表
| 选择器类型 | 标识符号 | 书写示例 | 匹配范围 | 使用特点 |
| ---- | ---- | ---- | ---- | ---- |
| 标签选择器 | 无符号，直接写标签名 | `p { color: red; }` | 页面全部同名标签 | 作用范围广，适合全局统一基础样式 |
| class类选择器 | 英文小数点`.` | `.text-blue { color: blue; }` | 所有添加对应class属性的元素 | 可重复复用，项目开发最常用 |
| id选择器 | 井号`#` | `#header { font-size: 20px; }` | 页面唯一id匹配元素 | 同一个页面id仅能出现一次，不可重复 |
最简示例代码
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        p { color: #333; }
        .desc { font-size: 14px; }
        #title { font-weight: bold; }
    </style>
</head>
<body>
    <p id="title">标题文本</p>
    <p class="desc">普通描述文字</p>
    <p class="desc">第二段描述文字</p>
</body>
</html>
```

### 1.3 CSS引入方式
1. 内联样式（行内样式）
    - 书写位置：HTML标签的style属性内
    - 生效范围：仅当前单个标签
    - 优缺点：优先级最高，调试方便；无法复用、后期维护繁琐
    示例代码
```html
<p style="color: red; font-size: 16px;">红色段落文字</p>
```
2. 内部样式表
    - 书写位置：HTML页面head内部`<style>`标签中
    - 生效范围：当前整个HTML文档
    - 优缺点：单页面内样式可复用；多页面无法共享样式文件
    示例代码
```html
<head>
    <meta charset="UTF-8">
    <style>
        p { color: blue; }
    </style>
</head>
<body>
    <p>蓝色文字段落</p>
</body>
```
3. 外部样式表（项目推荐）
    - 书写位置：独立`.css`文件，通过`<link>`标签引入页面
    - 生效范围：所有引入该css文件的页面
    - 优缺点：结构样式完全分离、浏览器缓存加速页面加载、多页面共享样式；需要额外管理样式文件
    css文件style.css
```css
p {
    color: green;
}
```
html页面引入代码
```html
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <p>绿色文字段落</p>
</body>
```

### 1.4 CSS引入方式优先级
- 优先级从高到低：内联样式 > 内部样式表、外部样式表
最简验证示例
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <!-- 外部样式：文字灰色 -->
    <link rel="stylesheet" href="style.css">
    <style>
        /* 内部样式：文字蓝色 */
        p { color: blue; }
    </style>
</head>
<body>
    <!-- 内联样式：文字红色，最终生效红色 -->
    <p style="color: red;">优先级测试文字</p>
</body>
```

### 1.5 CSS选择器优先级
1. `!important` 权重最高，强制覆盖所有样式
2. 权重层级从高至低
    1. !important
    2. 行内style样式
    3. id选择器 #xxx
    4. class、属性、伪类选择器 .xxx / :hover
    5. 标签选择器 div/p/h1
    6. 通配符 *
    7. 继承样式（权重最低）
    优先级测试示例代码
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        * { color: gray; }
        p { color: green; }
        .text { color: blue; }
        #test { color: orange; }
        .text { color: red !important; }
    </style>
</head>
<body>
    <p id="test" class="text" style="color: #000;">优先级测试</p>
</body>
```

### 1.6 CSS伪类选择器
1. 基础语法：`选择器:伪类 { 样式属性: 值; }`
2. 核心特性：元素本身无变化，触发指定交互状态后样式才生效
3. 常用伪类列表
- `:hover`：鼠标悬浮在元素上方
- `:active`：鼠标按住元素未松开瞬间
- `:link`：未访问的链接
- `:visited`：已点击访问过的链接
- `:focus`：输入框获取光标焦点
完整示例代码
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        a:link { color: #333; }
        a:visited { color: purple; }
        a:hover { color: red; }
        a:active { color: orange; }
        input:focus { border: 2px solid blue; }
        button:hover { background: #eee; }
        button:active { transform: scale(0.95); }
    </style>
</head>
<body>
    <a href="#">测试链接</a>
    <input type="text" value="" placeholder="点击输入框看焦点效果">
    <button>按钮</button>
</body>
</html>
```

### 1.7 CSS设置背景色
1. 三种颜色书写格式
- 英文单词：直接使用颜色英文名称，适合简单基础色
- 十六进制#RRGGBB：6位十六进制数字，支持3位简写，项目最常用
- transparent：完全透明，继承父容器背景
2. 基础颜色对照表
红色：red / #ff0000
绿色：green / #00ff00
蓝色：blue / #0000ff
白色：white / #ffffff
黑色：black / #000000
透明：transparent
示例代码
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        .box1 { background-color: red; height: 30px; }
        .box2 { background-color: #3498db; height: 30px; }
        .box3 { background-color: transparent; border: 1px solid #000; height: 30px; }
    </style>
</head>
<body>
    <div class="box1">红色背景</div>
    <div class="box2">蓝色背景</div>
    <div class="box3">透明背景</div>
</body>
</html>
```

### 1.8 CSS文本样式
1. 常用文本属性说明
- color：文字颜色
- font-size：文字字号，单位px
- font-weight：字体粗细，normal正常/bold加粗
- text-align：水平对齐 left/center/right/justify
- text-indent：段落首行缩进，常用2em（空两格）
- line-height：行高，无单位数值代表字体倍数
- letter-spacing：字间距，px单位
完整示例代码
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        p {
            color: #333;
            font-size: 16px;
            font-weight: normal;
            line-height: 1.6;
            text-align: justify;
            text-indent: 2em;
            letter-spacing: 0.5px;
        }
    </style>
</head>
<body>
    <p>这是一段示例文本，通过CSS文本属性完成排版优化，首行自动缩进两个字符，行间距宽松便于阅读，文字均匀对齐。</p>
</body>
</html>
```

### 1.9 外边距和内边距

1. padding 内边距：元素内容与边框之间距离
2. margin 外边距：当前元素和其他相邻元素之间距离
3. 单方向单独设置
```css
.box {
    padding-top: 10px;
    padding-right: 20px;
    padding-bottom: 10px;
    padding-left: 20px;
    margin-top: 10px;
    margin-right: auto;
    margin-bottom: 10px;
    margin-left: auto;
}
```
4. 简写规则（顺时针：上 右 下 左）
- 1个值：四边统一间距 `padding:15px`
- 2个值：上下、左右 `padding:10px 20px`
- 4个值：上、右、下、左 `padding:10px 20px 10px 20px`
5. 核心特性
- 垂直方向margin会合并，取两者最大值作为间距，不会相加
- `margin:0 auto` 可让块级元素在父容器水平居中
示例代码
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        .box {
            width: 300px;
            padding: 20px;
            margin: 0 auto;
            border: 1px solid #ccc;
        }
    </style>
</head>
<body>
    <div class="box">居中盒子，内边距20px</div>
</body>
</html>
```

### 1.10 浮动float
1. 作用：让块级元素脱离标准文档流，实现横向并排布局
2. 属性取值
- float:left：向左浮动靠左排列
- float:right：向右浮动靠右排列
- float:none：默认，不浮动
3. 基础示例代码
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        .item {
            width: 100px;
            height: 100px;
            background: #3498db;
            float: left;
            margin: 5px;
        }
    </style>
</head>
<body>
    <div class="item">1</div>
    <div class="item">2</div>
    <div class="item">3</div>
</body>
</html>
```

### 1.11 边框border
1. 边框三大基础属性
- border-width：边框粗细，px单位
- border-style：线型 solid实线/dashed虚线/dotted点线，必须设置否则无边框
- border-color：边框颜色
2. border-radius：圆角，50%可将正方形转为圆形
3. 简写格式 `border: 宽度 线型 颜色;`
示例代码
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        .box {
            width: 150px;
            height: 150px;
            border: 3px solid #3498db;
            border-radius: 8px;
        }
        .circle {
            width: 100px;
            height: 100px;
            border: 2px solid red;
            border-radius: 50%;
        }
    </style>
</head>
<body>
    <div class="box">圆角矩形</div>
    <div class="circle">圆形</div>
</body>
</html>
```

### 1.12 rem&px
1. px：固定像素单位，尺寸不会跟随页面根字体变化
2. rem：相对单位，1rem等于html根标签font-size大小，适合移动端全局适配
示例代码
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        html {
            font-size: 24px;
        }
        .px-text { font-size: 18px; }
        .rem-text { font-size: 1.125rem; }
    </style>
</head>
<body>
    <p class="px-text">固定18px文字</p>
    <p class="rem-text">1.125rem，跟随html字体变化</p>
</body>
</html>
```

### 1.13 实践作业
### 作业需求
制作个人信息卡片
1. 使用HTML语义化标签搭建页面结构，包含图片、文本格式化标签
2. 使用CSS内部样式或外部样式表，实现结构与样式分离
3. 运用背景、字体、边距、边框圆角等基础CSS属性美化页面

## 二、Bootstrap基础
### 2.1 Bootstrap定义
1. Bootstrap是免费开源HTML/CSS/JS前端UI框架，遵循移动优先开发理念。
2. 内置大量封装完成的组件与栅格布局，快速制作响应式网页，自动适配手机、平板、电脑各类设备，兼容主流浏览器。
3. 当前主流稳定版本为Bootstrap5，移除jQuery依赖，轻量化易使用。

### 2.2 Bootstrap三大核心优势
1. 开发高效：导航栏、按钮、表格、卡片、表单等组件开箱即用，无需手写大量基础样式，减少重复代码。
2. 响应式适配：内置栅格系统，一套代码自动适配多尺寸屏幕，解决移动端兼容问题。
3. 灵活扩展：支持自定义主题色、间距、圆角等全局样式，模块化结构便于团队维护与二次开发。

### 2.3 相关官方学习地址
1. Bootstrap5中文文档：https://v5.bootcss.com/docs/getting-started/introduction/#quick-start
2. 菜鸟教程Bootstrap5教程：https://www.runoob.com/bootstrap5/bootstrap5-tutorial.html

### 2.4 Bootstrap引入方式
1. CDN在线引入（推荐测试、线上项目，无需下载文件）
```html
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
```
2. 本地引入（离线、无网络环境使用）
- 下载bootstrap压缩包，将css文件放入项目文件夹
```html
<link rel="stylesheet" href="bootstrap.min.css">
```

### 2.5 容器Container
1. 容器是Bootstrap布局基础，用于控制页面宽度、居中、留白
2. 容器分类
- `.container`：固定宽度，左右留白，日常开发最常用

- `.container-fluid`：全屏铺满，无左右留白

- 响应式断点容器：container-sm / md / lg / xl / xxl，达到对应屏幕宽度自动切换固定宽度

  示例代码：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">固定宽度容器</div>
    <div class="container-fluid mt-3">全屏容器</div>
</body>
</html>
```

### 2.6 文本对齐工具类
- `.text-start`：左对齐
- `.text-center`：居中对齐
- `.text-end`：右对齐
示例代码
```html
<div class="container mt-3">
    <p class="text-start">左对齐文字</p>
    <p class="text-center">居中文字</p>
    <p class="text-end">右对齐文字</p>
</div>
```

### 2.7 表格组件
1. 基础类`.table`统一表格样式
2. `.table-striped` 斑马条纹隔行变色
示例代码
```html
<div class="container mt-3">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>姓名</th>
                <th>年龄</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>张三</td>
                <td>25</td>
            </tr>
            <tr>
                <td>李四</td>
                <td>30</td>
            </tr>
        </tbody>
    </table>
</div>
```

### 2.8 按钮组件
1. 主题配色类
- btn-primary：主蓝色
- btn-success：绿色成功
- btn-warning：黄色警告
- btn-danger：红色危险
- btn-info：浅蓝信息
- btn-link：链接样式按钮
2. 尺寸控制
- btn-lg：大按钮
- btn-sm：小按钮
示例代码
```html
<div class="container mt-3">
    <button class="btn btn-primary">主按钮</button>
    <button class="btn btn-success">成功按钮</button>
    <button class="btn btn-danger btn-sm">小号危险按钮</button>
    <button class="btn btn-warning btn-lg">大号警告按钮</button>
</div>
```

### 2.9 输入框与输入组
1. `.form-control`统一美化表单控件（输入框、下拉、文本域）
2. `.input-group`实现前后缀组合输入框
示例代码
```html
<div class="container mt-3">
    <!-- 基础输入框 -->
    <input type="text" class="form-control mb-3" placeholder="请输入文字">
    <!-- 带前缀输入组 -->
    <div class="input-group mb-3">
        <span class="input-group-text">@</span>
        <input type="text" class="form-control" placeholder="用户名">
    </div>
    <!-- 下拉框 -->
    <select class="form-control">
        <option>选项1</option>
        <option>选项2</option>
    </select>
</div>
```

### 2.10 背景色工具类
1. 主题背景色
  bg-primary、bg-success、bg-warning、bg-danger
2. 浅色淡化背景
  bg-primary-subtle、bg-success-subtle
3. 通用底色
  bg-light浅灰、bg-dark深色、bg-white纯白、bg-transparent透明
    示例代码
```html
<div class="container mt-3">
    <div class="bg-primary text-white p-2">主色背景</div>
    <div class="bg-success-subtle p-2 mt-2">淡化绿色背景</div>
    <div class="bg-dark text-white p-2 mt-2">深色背景</div>
</div>
```

### 2.11 取色器使用说明
在线搜索关键词「在线屏幕取色器」，打开工具后可拾取屏幕任意位置颜色，直接获取十六进制色值，复制到CSS中使用。

### 2.12 各类产品端区分
1. C端（Consumer个人端）：面向普通消费者，抖音、淘宝、美团、手机APP、官网首页
2. B端（Business企业端）：企业后台、商家管理系统、OA、ERP、进销存管理平台
3. G端（Government政府端）：政务平台、税务、公安、智慧城市系统
4. F端（Family家庭端）：智能家居、家庭云盘、亲子设备页面
5. S端（Supplier供应商端）：工厂供货、渠道商家后台
6. P端（Platform平台端）：平台运营总后台，管理商户、用户、活动规则
7. D端（Developer开发者端）：开放平台、API开发者后台
8. M端：移动端H5、手机网页
9. 设备载体分类：PC电脑网页、移动端H5、微信小程序

### 2.13 课堂实践
### 电影推荐卡片页面
1. 页面结构
- 顶部导航栏：首页、电影推荐、排行榜
- 主体：电影卡片模块
- 页脚：版权文字© 2025 电影推荐平台
2. 卡片内容
- 左侧电影海报响应式图片
- 右侧：电影标题、导演、主演、上映年份、剧情简介、星级评分
- 底部两个按钮：查看详情、加入片单
完整示例代码
### 2.14 课后作业
### 作业需求
基于HTML搭配Bootstrap框架，复刻苹果中国官网顶部导航栏与iPhone产品展示界面，要求：
1. 使用Bootstrap容器、导航组件、栅格布局完成页面排版
2. 页面适配移动端，缩小浏览器窗口自动调整布局
3. 合理使用按钮、文本对齐、背景色工具类美化页面

## 相关知识

- [[Web Development Knowledge Map]]
- [[Frontend Basics 1]]：HTML 页面结构。
- [[Browser DevTools Notes]]：调试 CSS 和响应式布局。
- [[Backend Basics 1#五、静态文件|Flask 静态文件]]
