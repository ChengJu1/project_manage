# 网页基础
## 1. 网页与网站基础

### 1.1 网页（Web Page）
- 定义：浏览器可解析并渲染的单个可访问文档，是网站的最小访问单元。  
- 技术栈：HTML（结构）、CSS（样式）、JavaScript（交互逻辑）。  
- 文件后缀：`.html` / `.htm`。  
- 本质：文本文件，经浏览器解析渲染为可视化页面。  
- 示例：文章详情页、商品页、登录页、用户个人主页。
---
### 1.2 静态网页 vs 动态网页
#### 静态网页（Static Web Page）
- 内容：文件内容固定不变，所有用户、所有时间看到完全一致。
- 渲染：服务器直接返回静态文件，浏览器直接解析渲染，无后端逻辑执行。
- 更新：必须修改源代码并重新上传，维护成本高。
- 技术：仅 HTML + CSS + JS（前端），无需后端、无需数据库。
- 特点：加载快、成本低、安全、适合低更新频率场景。
- 适用：企业官网、个人简历页、产品宣传页、帮助文档。

#### 动态网页（Dynamic Web Page）
- 内容：实时生成、因人而异、因时而异，数据来自数据库或后端计算。
- 渲染：浏览器请求 → 服务器执行后端代码 → 查询数据库 → 生成HTML → 返回浏览器渲染。
- 更新：通过后台管理系统修改数据，无需改代码，维护高效。
- 技术：前端（HTML/CSS/JS）+ 后端（Python/Java/PHP）+ 数据库（MySQL/PostgreSQL/MongoDB）。
- 特点：交互强、数据驱动、支持用户体系、内容实时更新。
- 适用：电商、社交平台、管理系统、用户中心、内容社区。
---
### 1.3 网站（Website）
定义：同一域名下、主题相关、通过超链接互联的一组网页、静态资源、服务程序与数据的集合。  
核心组成：
1. 域名（Domain）：人类可读的唯一标识，如 `qq.com`。
2. 网页集合：首页、列表页、详情页、功能页，由超链接关联。
3. 静态资源：图片、CSS、JS、字体、图标、视频等。
4. Web服务器：Nginx/Apache/Tomcat，负责接收HTTP请求、分发资源、反向代理。
5. 应用服务器（后端）：Flask/Django/Java Spring，执行业务逻辑、处理数据。
6. 数据库：持久化存储结构化数据（用户、商品、订单、文章）。

示例：微信读书 `weread.qq.com`，包含首页、书架、阅读页、笔记页、个人中心等。

---

## 2. URL 详解（统一资源定位符）
### 2.1 定义
URL（Uniform Resource Locator）：互联网上唯一标识资源位置与访问方式的字符串，俗称“网址”。

---
### 2.2 标准结构（完整）
```
协议://域名:端口/路径/资源名?查询参数#锚点
```
---
### 2.3 逐段解析（示例）
示例：
```
https://movie.douban.com/people/64345698/collect?start=15&sort=time#top
```

1. 协议 Protocol：`https://`
    - `http`：超文本传输协议，明文传输，端口 80。
    - `https`：HTTP+TLS/SSL，加密传输，端口 443，主流网站标准。
    - 作用：规定客户端与服务器之间数据传输格式与安全机制。

2. 域名 Domain：`movie.douban.com`
    - 顶级域名（TLD）：`.com` / `.cn` / `.org`.`gov`,。
    - 主域名：`douban.com`，主体标识。
    - 子域名：`movie`，服务/模块划分，可多级。
    - 解析：通过DNS将域名映射为服务器IP地址。

3. 端口 Port：默认省略
    - HTTP：80；HTTPS：443；FTP：21；SSH：22。
    - 端口用于区分同一服务器上不同服务进程。

4. 路径 Path：`/people/64345698/collect`
    - 服务器上资源的逻辑路径，定位具体接口或页面。
    - `/people`：用户模块；`64345698`：用户唯一ID；`collect`：收藏功能。

5. 查询参数 Query：`?start=15&sort=time`
    - 格式：`?k1=v1&k2=v2`。
    - 用途：分页、筛选、排序、搜索、传递业务参数。
    - 示例：`start=15` 从第16条开始；`sort=time` 按时间排序。

6. 锚点 Fragment：`#top`
    - 仅浏览器识别，不发送给服务器。
    - 作用：页面内定位，滚动到指定ID元素位置。

---

## 3. HTTP/HTTPS 核心
### 3.1 HTTP 协议
HTTP（Hypertext Transfer Protocol）：无状态、请求-响应模型的应用层协议，规定浏览器与服务器之间请求格式、响应格式、交互规则。

### 3.2 HTTP 请求组成
- 请求行：方法 + URL + 协议版本
- 请求头（Request Headers）：客户端信息、Cookie、认证、内容类型
- 请求体（Request Body）：POST/PUT 提交的数据（JSON/表单/文件）

### 3.3 HTTP 响应组成
- 响应行：协议版本 + 状态码 + 描述
- 响应头（Response Headers）：服务器信息、数据类型、缓存策略、Cookie
- 响应体（Response Body）：HTML、JSON、图片、文本等返回内容

### 3.4 常用 HTTP 状态码
#### 2xx 成功
- 200 OK：请求成功，正常返回资源。
- 201 Created：资源创建成功（注册、提交）。
- 204 No Content：成功但无返回体（删除）。

#### 3xx 重定向
- 301 Moved Permanently：永久重定向（域名迁移）。
- 302 Found：临时重定向。
- 304 Not Modified：资源未修改，使用缓存。

#### 4xx 客户端错误
- 400 Bad Request：请求语法/参数错误。
- 401 Unauthorized：未认证/Token失效。
- 403 Forbidden：已认证但无权限。
- 404 Not Found：资源不存在。
- 405 Method Not Allowed：方法不允许（接口只支持GET）。

#### 5xx 服务器错误
- 500 Internal Server Error：服务器代码异常。
- 502 Bad Gateway：网关/反向代理收到无效响应。
- 503 Service Unavailable：服务不可用（过载/维护）。
- 504 Gateway Timeout：网关超时。

### 3.5 常用请求方法（RESTful）
- GET：获取资源，参数在URL，无副作用、可缓存。
- POST：创建资源，参数在请求体，不可缓存、数据量大。
- PUT：整体更新资源。
- PATCH：局部更新资源。
- DELETE：删除资源。

### 3.6 HTTPS
HTTPS = HTTP + TLS/SSL
- 作用：加密传输、身份认证、防篡改。
- 流程：握手→协商密钥→加密传输。
- 现状：现代网站全站HTTPS，HTTP逐渐淘汰。

---

## 4. 浏览器开发者工具实践
### 4.1 Network（网络面板）
- 查看请求列表、状态码、响应时间、请求/响应头、请求/响应体。
- 分析页面加载流程、资源依赖、接口调用。

### 4.2 关键概念补充
- Cookie：服务器下发、浏览器存储的小型文本数据，用于会话保持、身份识别、状态记录。
- Session：服务器端会话，与Cookie配合实现用户登录态。
- DNS：域名解析系统，将域名转为IP。(.hosts)
- Socket：网络通信端点，实现进程间数据传输。
- MIME Type：资源类型标识（`text/html`、`application/json`、`image/png`）。

---

## 5. 本章小结
- 网页：单个渲染单元；网站：域名下资源集合。
- 静态 vs 动态：内容是否实时生成、是否依赖后端与数据库。
- URL：协议://域名:端口/路径?参数#锚点。
- HTTP：请求-响应、无状态；状态码：2xx成功、4xx客户端、5xx服务端。
- 方法：GET查、POST创、PUT改、DELETE删。
- HTTPS：HTTP+加密，安全传输标准。

## 相关知识

- [[Web Development Knowledge Map]]
- [[Browser DevTools Notes]]：使用浏览器工具观察网页与网络请求。
- [[Frontend Basics 1]]：HTML 页面结构。
- [[Backend Basics 1]]：Flask 与 HTTP 请求处理。
- [[Test Development Notes#第三章 接口测试|接口测试]]

