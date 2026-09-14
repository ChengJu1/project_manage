# 网页前端基础-1
## 一、HTML
### 1.1 HTML 定义
超文本标记语言（HyperText Markup Language，HTML）是用于创建网页的标准标记语言，不属于编程语言，无逻辑运算能力，仅用来搭建网页结构。

HTML由各类标签组成，分为成对双标签与自闭合单标签，当前行业主流使用HTML5版本。

HTML5 相比旧版本核心新增内容：

- 新增大量语义化标签：`<nav>`、`<header>`、`<main>`、`<article>`、`<footer>` 等；

- 原生多媒体标签：音频、视频，不用插件播放音视频；

- 画布绘图：`<canvas>`、矢量图形 `<svg>`；

- 新增表单类型：`email`、`number`、`date` 等，自带原生校验；

- 新增本地存储、拖拽、地理定位、WebSocket 等网页 API；

- 简化文档声明 `<!DOCTYPE html>`，不再需要冗长的 DTD 声明。

区分概念：
- HTML：统称标记语言；
- HTML5：特指第五版规范，现在所有网页开发默认使用该标准；

### 1.2 HTML 模版基础标签
1. `<!DOCTYPE html>`：文档类型声明，必须写在文档首行，触发浏览器以HTML5标准模式渲染页面，省略会出现样式错乱。
2. `<html> … </html>`：页面根元素，所有页面内容标签都需要嵌套在该标签内，搭配lang属性可设置页面语言，`lang="zh-CN"`代表中文页面，利于搜索引擎优化与无障碍访问。
3. `<head> … </head>`：网页头部区域，存放不会直接展示在页面上的元数据，用于给浏览器、搜索引擎传递页面相关配置信息。
4. `<meta charset="utf-8">`：设置网页字符编码为UTF-8，兼容全球各类文字符号，避免中文、特殊符号乱码，需放置在head标签最靠前位置。
5. `<meta name="viewport" content="width=device-width, initial-scale=1.0">`：移动端适配核心配置，保证手机端页面不会出现异常缩放，移动端开发必备。
6. `<title>标题</title>`：定义网页标题，展示在浏览器标签栏，同时是搜索引擎抓取页面的核心标识。
7. `<link rel="icon" href="图标地址">`：设置浏览器标签页网页图标，推荐使用ico、png格式图标，常用免费图标资源为阿里巴巴矢量图标库（www.iconfont.cn）。
8. `<body> … </body>`：网页主体区域，页面所有可见文字、图片、表单、导航等内容全部放置于此。
9. `<h1>`：页面一级标题，单个页面仅允许使用一次，代表页面核心主题。
10. `<p>`：段落标签，属于块级元素，自带上下默认间距，用于存放连续文本内容。
11. 注释写法：`<!-- 注释内容 -->`，注释内容不会被浏览器渲染，仅开发者可见，不支持注释嵌套。
    最简完整模板示例代码：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>基础页面</title>
    <link rel="icon" href="favicon.ico">
</head>
<body>
    <h1>页面大标题</h1>
    <p>一段测试文本</p>
    <!-- 这是注释，不会显示 -->
</body>
</html>
```

### 1.3 HTML 文本相关标签
1. 文本标题分为六级：`<h1>`一级标题、`<h2>`二级标题、`<h3>`三级标题、`<h4>`四级标题、`<h5>`五级标题、`<h6>`六级标题，标签自带加粗样式，层级依次递减。
2. 文本段落：`<p>文本内容</p>`，仅能嵌套行内文本标签，不可嵌套块级容器。
3. 文字语义标签
    - `<strong>`：语义视觉均加粗，具备强调语义，搜索引擎会识别内容权重。
    - `<b>`：视觉加粗，仅改变文字样式，无语义属性。
    - `<em>`：语义斜体，代表轻微强调文本内容。
    - `<i>`：视觉斜体，仅修改文字倾斜样式，无特殊语义。
    - `<u>`：文本下划线，纯视觉样式，易与超链接混淆，日常开发少用。
    - `<del>`：文本删除线，用于标记作废、已删除内容。
    - `<ins>`：新增文本标记，用于标注新增、修改后的内容。
    - `<small>`：小号备注文字，适用于版权、补充说明类小字。
4. 网页字体尺寸常用单位
    - px（像素）：固定尺寸单位，多用于PC端页面、图片、边框尺寸设置。
    - rem（根字体单位）：相对单位，1rem等于html根标签设置的字体大小，适配移动端页面全局缩放。
```html
<h1>一级标题</h1>
<h2>二级标题</h2>
<p>普通段落 <strong>重点文字</strong> <em>倾斜文字</em> <del>删除文字</del> <ins>新增文字</ins> <small>小字备注</small></p>
```

### 1.4 `<div>`和`<p>`的区别
1. 语义区分：`<p>`专用于承载连续正文文本，具备阅读语义；`<div>`无专属语义，仅用于页面元素分组布局。
2. 嵌套规则：`<p>`仅能嵌套行内元素，无法包裹div、标题等块级标签；`<div>`无嵌套限制，可容纳任意块级、行内元素。
3. 默认样式：`<p>`自带上下外边距；`<div>`无任何默认内外边距。
4. 使用场景：`<p>`放置文章段落、简短描述文本；`<div>`用于页面分块、卡片、多元素组合布局。
5. 配套行内容器`<span>`：无默认样式行内标签，用于局部文字单独修改样式，不会自动换行。
div与p最简示例代码：
```html
<div>
    <p>这是段落标签，只能放文字行内元素</p>
    <p>段落内局部文字 <span style="...">单独修饰</span></p>
</div>
```

### 1.5 HTML常用标签
1. 基础排版标签
    - `<br>`：换行标签，单标签，强制文本换行，无额外间距。
    - `<hr>`：分割线标签，单标签，生成水平分割线，自带上下留白，用于页面区域分隔。
2. 图片标签 `<img src="图片地址" alt="图片描述" width="300" height="auto" title="悬浮文字" loading="lazy">`
    - src属性：填写图片地址，分为网络绝对地址、本地相对路径，相对路径包含同级文件、上级文件夹文件两种写法。
    - alt属性：图片加载失败时展示替代文字，无障碍访问与搜索引擎优化必备，必须填写。
    - width、height：设置图片宽高，仅填写宽度、高度设为auto可避免图片拉伸变形，单位默认px。
    - title属性：鼠标悬浮在图片上时展示提示文字。
    - loading="lazy"：图片懒加载，页面滚动至图片位置才发起资源请求，提升页面加载速度、节省流量。
3. 超链接`<a>`标签
    - 外部网站链接：`<a href="完整网址" target="_blank">文字</a>`，用于跳转外部站点。
    - 同页面锚点链接：`<a href="#元素id">跳转指定区域</a>`，实现页面内滚动跳转。
    - 空链接：`href="#"`点击返回页面顶部；`href="javascript:;"`无任何跳转行为。
    - 邮件链接：`<a href="mailto:邮箱地址">发送邮件</a>`，点击唤起本地邮件软件。
    - 电话链接：`<a href="tel:手机号">拨打电话</a>`，移动端点击可唤起拨号界面。
4. target属性取值说明
    - _self：默认属性，在当前页面窗口覆盖跳转。
    - _blank：全新空白标签页打开链接，外部网站统一推荐使用。
    - _parent：在父级框架窗口打开页面。
    - _top：在顶层页面窗口打开，适用于多层嵌套iframe场景。
5. 输入框基础标签`<input type="text">`，根据type切换不同输入功能。
常用标签综合最简示例代码：
```html
<p>第一行文字<br>第二行换行文字</p>
<hr>
<img src="test.jpg" alt="测试图片" width="200" loading="lazy">
<a href="https://www.baidu.com" target="_blank">百度（新窗口打开）</a>
<a href="#top">回到顶部</a>
```

### 1.6 导航栏
1. `<nav>`标签用于定义页面导航链接区域，可放置网站菜单、分页导航、返回顶部链接等导航组。
2. 标签核心作用
    - 语义化标识：让浏览器、搜索引擎识别该区域为导航模块，提升网站SEO效果与无障碍阅读体验。
    - 简化代码结构：替代传统`<div class="nav">`写法，代码可读性更强。
3. 页面可设置多个`<nav>`，分别承载主导航、侧边导航、分页导航。
导航最简示例代码：
```html
<nav>
	<a href="index.html">首页</a>
	<a href="news.html">新闻</a>
	<a href="about.html">关于我们</a>
</nav>
```

### 1.7 列表
1. 无序列表：外层`<ul>`包裹，内部使用`<li>`书写每一条列表项，默认展示实心圆点，适用于菜单、商品列表。
2. 有序列表：外层`<ol>`包裹，内部使用`<li>`书写列表项，默认按阿拉伯数字排序，适用于步骤、排名内容。
3. 自定义列表：外层`<dl>`包裹，`<dt>`为列表标题，`<dd>`为标题对应描述内容，用于名词解释类内容展示。
4. 有序列表可用属性
    - type：修改排序编号样式，type="1"阿拉伯数字、type="A"大写字母、type="a"小写字母、type="I"大写罗马数字、type="i"小写罗马数字。
    - start：设置列表起始编号，start="5"代表从数字5开始排序。
    - reversed：开启倒序排列，无需赋值，直接添加到ol标签即可。
5. 列表开发规范：ul、ol标签内部仅可直接放置li，其余标签需要嵌套在li内部。
列表全套最简示例代码：
```html
<!-- 无序列表 -->
<ul>
    <li>苹果</li>
    <li>香蕉</li>
</ul>
<!-- 有序列表 -->
<ol type="1" start="2" reversed>
    <li>步骤一</li>
    <li>步骤二</li>
</ol>
<!-- 自定义列表 -->
<dl>
    <dt>HTML</dt>
    <dd>搭建页面结构</dd>
</dl>
```

### 1.8 表格
1. 表格相关标签
    - `<table>`：整个表格的外层容器，所有表格元素均嵌套其中。
    - `<thead>`：表格头部区域，存放表头文字。
    - `<tbody>`：表格主体区域，存放业务数据内容。
    - `<tr>`：代表表格单行，表头、数据行统一使用该标签。
    - `<th>`：表头单元格，文字默认加粗居中。
    - `<td>`：普通数据单元格，存放表格具体内容。
2. 表格常用属性
    - border：设置表格边框宽度，仅学习演示使用，正式项目使用CSS实现边框。
    - cellpadding：单元格内部文字与边框的间距。
    - cellspacing：单元格与单元格之间的空隙。
    - colspan：单元格横向合并，属性值代表合并列数量。
    - rowspan：单元格纵向合并，属性值代表合并行数量。
    表格最简示例代码：
```html
<table border="1">
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
  </tbody>
</table>
```

### 1.9 输入框
1. `<form>`是表单根标签，所有输入控件必须嵌套在form内部，两个核心属性
    - action：表单数据提交的后端接口地址，填写#代表提交至当前页面。
    - method：数据提交方式，get适用于查询类请求，参数明文展示在地址栏；post适用于登录、注册，数据隐藏传输，安全性更高。
2. 表单基础结构包裹所有表单元素。
3. `<input>`输入框核心type类型
    - text：普通文本输入框，用于填写用户名、昵称。
    - password：密码输入框，输入内容自动隐藏。
    - email：邮箱输入框，浏览器自动校验邮箱格式。
    - number：数字输入框，搭配min、max限制输入数值范围。
    - date：日期选择控件，点击唤起日历选择面板。
4. input通用属性
    - name：表单提交必备属性，后端依靠name获取对应输入内容。
    - placeholder：输入框内灰色提示文字，无输入时展示。
    - value：输入框默认填充内容，单选、复选框提交值依靠value传递。
    - required：添加后开启表单必填校验，未填写提交会自动弹窗提示。
    - disabled：控件禁用，无法输入、数据不会随表单提交。
    - readonly：控件只读，可查看内容无法修改，数据正常提交。
    - maxlength：限制输入字符最大长度。
5. 表单控件分类
    - 单选按钮`<input type="radio">`：同一组单选name属性必须保持一致，仅能选择一项，checked设置默认选中。
    - 复选框`<input type="checkbox">`：支持多选，同组控件name统一命名，checked标记默认选中项。
    - 下拉列表`<select>`搭配`<option>`：点击展开选择菜单，multiple属性开启多选下拉，selected设置默认选中选项。
    - 多行文本域`<textarea></textarea>`：支持换行输入长文本，rows控制显示行数，cols控制显示宽度，默认文字写在标签中间。
    - label绑定标签：搭配input的id属性使用，点击文字可自动聚焦输入框，优化操作体验与无障碍访问。
6. 按钮分类
    - 提交按钮：`<input type="submit">`、`<button type="submit">`，点击自动提交表单数据。
    - 重置按钮：`<input type="reset">`、`<button type="reset">`，一键清空所有输入框内容。
    - 普通按钮：`<input type="button">`、`<button type="button">`，无默认交互逻辑，配合JavaScript实现自定义功能。
7. 按钮使用注意：form表单内`<button>`标签不书写type属性时，默认等同于提交按钮。
表单最简示例代码：
```html
<form action="#" method="post">
    <p>用户名：<input type="text" name="user" placeholder="请输入用户名" required></p>
    <p>密码：<input type="password" name="pwd" placeholder="请输入密码"></p>
    <p>性别：
        <input type="radio" name="sex" value="man" id="man">
        <label for="man">男</label>
    </p>
    <p>留言：<textarea name="msg" rows="3"></textarea></p>
    <button type="submit">提交</button>
    <input type="reset" value="重置">
</form>
```

### 1.10 课堂实践
1. 实现用户注册网页完整需求
    - 网页标题设置为“用户注册”
    - 自定义网页图标，替换link标签内图标地址
    - 页面包含导航栏，导航链接：首页、登录、注册、校园资讯、帮助中心，href统一填写#
    - 页面添加一级标题`<h1>用户注册</h1>`
    - 搭建表单，包含用户名、密码、邮箱三类输入框，全部设置必填校验
    - 添加提交注册按钮
    完整可运行代码：
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>用户注册</title>
    <link rel="icon" href="favicon.ico">
</head>
<body>
    <nav>
        <a href="#">首页</a>
        <a href="#">登录</a>
        <a href="#">注册</a>
        <a href="#">校园资讯</a>
        <a href="#">帮助中心</a>
    </nav>
    <h1>用户注册</h1>
    <form action="#" method="post">
        <p>
            <label>用户名：</label>
            <input type="text" name="username" placeholder="请输入用户名" required>
        </p>
        <p>
            <label>密码：</label>
            <input type="password" name="password" placeholder="请输入密码" required>
        </p>
        <p>
            <label>邮箱：</label>
            <input type="email" name="email" placeholder="请输入邮箱" required>
        </p>
        <button type="submit">提交注册</button>
    </form>
</body>
</html>
```

## 二、HTML基础拓展知识点
### 2.1 页面元素分类
1. 块级元素：独占一行，宽度默认铺满父容器，可设置宽高、内外边距。常用标签：div、p、h1~h6、ul、ol、table、form、nav。
2. 行内元素：同排展示，尺寸由文字内容自动撑开，无法直接设置宽高。常用标签：a、strong、em、u、span。
3. 行内块元素：同行展示，同时支持自定义宽高。常用标签：img、input。
元素分类简易示例：
```html
<!-- 块级 -->
<div>块级div</div>
<p>块级段落</p>

<!-- 行内 -->
<span>行内span</span>
<a href="#">行内链接</a>

<!-- 行内块 -->
<input type="text">
<img src="img.jpg" alt="图片">
```

### 2.2 HTML实体字符
1. 网页特殊符号无法直接输入，需要使用实体编码渲染
    - 空格：`&nbsp;`
    - 小于符号<：`&lt;`
    - 大于符号>：`&gt;`
    - 版权符号©：`&copy;`
    - 人民币符号¥：`&yen;`
    实体字符示例代码：
```html
<p>100 &gt; 99 &nbsp;&copy;2026 版权所有 ¥100</p>
```

### 2.3 HTML5语义化布局标签
- `<header>`：页面或区块头部区域。
- `<main>`：页面核心主体内容，单个页面仅允许出现一次。
- `<section>`：独立内容区块，用于划分章节、模块。
- `<article>`：完整独立内容块，适用于新闻、文章展示。
- `<aside>`：侧边栏、辅助补充信息区域。
- `<footer>`：页面底部，放置版权、备案、底部导航信息。
  语义标签最简示例：

```html
<header>网站头部</header>
<main>
    <section>文章区域</section>
    <aside>侧边栏</aside>
</main>
<footer>底部版权</footer>
```

### 2.4 前端通用开发规范
1. 所有标签、属性统一使用小写书写，属性值包裹双引号。
2. 自闭合标签统一规范书写，无需额外闭合斜杠。<img>
3. 图片alt、表单name、移动端viewport标签为强制必备配置。
4. 边框、间距、尺寸样式统一交由CSS控制，不使用HTML原生border、align等样式属性
5. 跳转外部网站的a标签统一添加target="_blank"属性。

## 相关知识

- [[Web Development Knowledge Map]]
- [[Web Basics]]
- [[Frontend Basics 2]]：CSS 与 Bootstrap。
- [[Browser DevTools Notes]]：调试 HTML 和 CSS。
- [[Backend Basics 1#四、Jinja2 模板引擎|Jinja2 模板]]
