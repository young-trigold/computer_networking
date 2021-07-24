- [1. 介绍](#1-介绍)
  - [1.1. 要求记号](#11-要求记号)
  - [1.2. 语法记号](#12-语法记号)
- [2. 架构](#2-架构)
  - [2.1. 客户/服务器交换报文](#21-客户服务器交换报文)
  - [2.2. 实现多样性](#22-实现多样性)
  - [2.3. 中介](#23-中介)
  - [2.4. 缓存](#24-缓存)
  - [2.5. 符合性和错误处理](#25-符合性和错误处理)
  - [2.6. 协议版本](#26-协议版本)
  - [2.7. 统一资源标识符(URI)](#27-统一资源标识符uri)
    - [2.7.1. http URI 方案](#271-http-uri-方案)

# 1. 介绍

**超文本传输协议(Hypertext Transfer Protocol, HTTP)** 是一个无状态的应用级请求/响应协议，它使用可扩展的语义和自我描述的报文有效载荷，与基于网络的超文本信息系统进行灵活的交互。本文件是一系列文件中的第一个，这些文件共同构成了HTTP/1.1规范：

1. “报文语法和路由”（本文件）
2. “语义和内容” [RFC 7231] 
3. “条件请求” [RFC 7232]
4. “范围请求” [RFC 7233]
5. “缓存” [RFC 7234]
6. “认证” [RFC 7235]

这个HTTP/1.1规范废除了RFC 2616和RFC 2145（关于HTTP版本）。该规范还更新了以前在RFC 2817中定义的使用CONNECT建立隧道的方法，并定义了在RFC 2818中非正式描述的 “https” URI方案。

HTTP是一个信息系统的通用接口协议。它旨在通过向客户提供一个独立于所提供的资源类型的统一接口，来隐藏服务实现的细节。同样，服务器也不需要知道每个客户端的目的：一个HTTP请求可以被孤立地考虑，而不是与特定类型的客户端或预先确定的应用步骤序列相关联。其结果是一个可以在许多不同的环境中有效使用的协议，其实现可以随着时间的推移独立发展。

HTTP也被设计为一种中介协议，用于翻译与非HTTP信息系统的通信。HTTP代理和网关可以提供对其他信息服务的访问，将其不同的协议翻译成超文本格式，可以被客户以与HTTP服务相同的方式查看和操作。

这种灵活性的一个后果是，不能用接口后面发生的事情来定义协议。相反，我们只限于定义通信的语法、接收通信的意图以及接收者的预期行为。如果通信被孤立地考虑，那么成功的行动应该反映在对服务器提供的可观察界面的相应改变中。然而，由于多个客户可能平行行动，而且可能是交叉行动，我们不能要求这种变化在单个响应的范围之外可以观察到。

本文件描述了在HTTP中使用或提及的架构基本组成，定义了 “http” 和 “https” URI方案，描述了整体网络操作和连接管理，并定义了HTTP报文架构和转发要求。我们的目标是定义所有独立于报文语义的HTTP报文处理所需的机制，从而为报文解析器和报文转发中介机构定义一套完整的要求。

## 1.1. 要求记号

本文档中的关键词 "必须"、"不得"、"REQUIRED"、"SHALL"、"SHALL NOT"、"SHOULD"、"RECOMMENDED"、可以" 和 "OPTIONAL "应按照[RFC 2119]中的描述进行解释。

有关错误处理的一致性标准和注意事项在第2.5节中定义。

## 1.2. 语法记号

本规范使用 [RFC 5234] 的 Augmented Backus-Naur Form (ABNF) 符号，并在第 7 节中定义了一个列表扩展，允许使用'#'运算符（类似于'*'运算符表示重复的方式）紧凑地定义逗号分隔的列表。附录B显示了收集的语法，其中所有的列表操作符都扩展为标准的ABNF符号。

以下核心规则通过参考包括在 [RFC 5234] 附录 B.1 中的定义。ALPHA（字母）、CR（回车）、CRLF（CR LF）、CTL（控制）、DIGIT（十进制0-9）、DQUOTE（双引号）、HEXDIG（十六进制0-9/A-F/a-f）、HTAB（水平制表符）、LF（换行）、OCTET（任何8位数据序列）、SP（空格）和VCHAR（任何可见[USASCII]字符）。

按照惯例，ABNF规则名称前缀为 "obs-"，表示由于历史原因出现的 "过时 "语法规则。

# 2. 架构

HTTP是为万维网(WWW)架构而创建的，并随着时间的推移不断发展，以支持全球超文本系统的可扩展性需求。该架构的大部分内容反映在用于定义HTTP的术语和语法产生式上。


## 2.1. 客户/服务器交换报文

HTTP是一个无状态的请求/响应协议，通过可靠的传输层或会话层的 “连接”（第6节）交换报文（第3节）。一个HTTP “**客户(client)**” 是一个程序，它建立了一个与服务器的连接，目的是发送一个或多个HTTP请求。HTTP “**服务器(server)**” 是一个接受连接的程序，以便通过发送HTTP响应来服务HTTP请求。

术语 "客户端"和 "服务器" 仅指这些程序在特定连接中所扮演的角色。同一个程序可能在某些连接上充当客户端，而在其他连接上充当服务器。术语 "**用户代理(user agent)**" 是指发起请求的各种客户端程序，包括（但不限于）浏览器、爬虫（基于网络的机器人）、命令行工具、定制应用程序和移动应用程序。术语 "**初始服务器(origin server)**" 指的是能够为特定目标资源发起权威响应的程序。术语 "**发送方(sender)**"和 "**接收方(recipent)**"分别指发送或接收特定信息的任何实现。

HTTP依靠 **统一资源标识符(Uniform Resource Identifier, URI)** 标准[RFC 3986]来表示目标资源（第5.1节）和资源之间的关系。报文的传递格式类似于互联网邮件[RFC 5322]和多用途互联网邮件扩展（MIME）[RFC 2045]所使用的格式（关于HTTP和MIME报文的区别，请参见[RFC 7231]的附录A）。

大多数HTTP通信包括对由URI识别的某些资源的表示的检索请求（GET）。在最简单的情况下，这可能是通过用户代理（UA）和源服务器（O）之间的单一双向连接（==）完成的。


        请求 >>>
UA ======================================= O
                                <<< 响应

客户端以请求报文的形式向服务器发送一个HTTP请求，以包括方法、URI和协议版本的请求行开始（第3.1.1节），然后是包含请求修饰词、客户信息和表示元数据的首部字段（第3.2节），一个空行表示头部分的结束，最后是包含有效载荷体的报文体（如果有的话，第3.3节）。

服务器通过发送一个或多个HTTP响应报文来响应客户的请求，每个响应报文以一个状态行开始，其中包括协议版本、成功或错误代码以及文本原因短语（第3.1.2节），后面可能是包含服务器信息、资源元数据和表示元数据的首部字段（第3.2节），一个空行表示首部的结束，最后是包含有效载荷体的报文体（如果有的话，第3.3节）。

一个连接可能用于多个请求/响应交互，如第6.3节所定义。

下面的例子说明了URI "http://www.example.com/hello.txt"的GET请求（[RFC 7231]第4.3.1节）的典型报文交互。

客户请求：

```http
GET /hello.txt HTTP/1.1
User-Agent: curl/7.16.3 libcurl/7.16.3 OpenSSL/0.9.7l zlib/1.2.3
Host: www.example.com
Accept-Language: en, mi
```

服务器响应：

```http
HTTP/1.1 200 OK
Date: Mon, 27 Jul 2009 12:28:53 GMT
Server: Apache
Last-Modified: Wed, 22 Jul 2009 19:15:56 GMT
ETag: "34aa387-d-1568eb00"
Accept-Ranges: bytes
Content-Length: 51
Vary: Accept-Encoding
Content-Type: text/plain

Hello World! My payload includes a trailing CRLF.
```

## 2.2. 实现多样性

在考虑HTTP的设计时，很容易落入一个陷阱，认为所有的用户代理都是通用的浏览器，所有的初始服务器都是大型的公共网站。实际情况并非如此。常见的HTTP用户代理包括家用电器、音响、天平、固件更新脚本、命令行程序、移动应用程序以及各种形状和大小的通信设备。同样，常见的HTTP初始服务器包括家庭自动化装置、可配置的网络组件、办公机器、自动机器人、新闻源、交通摄像头、广告选择器和视频交付平台。

术语 "用户代理" 并不意味着在请求时有一个人类用户直接与软件代理进行互动。在许多情况下，用户代理被安装或配置为在后台运行，并保存其结果供以后检查（或只保存那些可能有趣或错误的结果的子集）。例如，爬虫通常被赋予一个起始URI，并被配置为在作为超文本图抓取网络时遵循某些行为。

HTTP的实现多样性意味着并非所有的用户代理都能向他们的用户提出交互式建议，或为安全或隐私问题提供足够的警告。在本规范要求向用户报告错误的少数情况下，这种报告只在错误控制台或日志文件中可以观察到是可以接受的。同样地，要求自动操作在进行之前由用户确认的要求可以通过预先的
配置选择、运行时选项或简单地避免不安全的动作；如果用户已经做出了选择，确认并不意味着任何特定的用户界面或中断正常处理。

## 2.3. 中介

HTTP允许使用中介机构，通过一连串的连接来满足请求。有三种常见的HTTP中介形式：代理、网关和隧道。在某些情况下，一个中介可能充当初始服务器、代理、网关或隧道，根据每个请求的性质切换行为。


    >>>         >>>         >>>         >>>
UA =========== A =========== B =========== C =========== O
            <<<             <<<           <<<        <<<

上图显示了用户代理和初始服务器之间的三个中介（A、B和C）。一个穿越整个链条的请求或响应信息将通过四个独立的连接。一些HTTP通信选项可能只适用于与最近的、非隧道邻接节点的连接，只适用于链的端点，或适用于沿链的所有连接。尽管图表是线性的，但每个参与者都可能参与多个同时进行的通信。例如，B在处理A的请求的同时，可能正在接收来自A以外的许多客户的请求，和/或将请求转发给C以外的服务器。同样，后来的请求可能会通过不同的连接路径发送，通常是基于负载平衡的动态配置。

术语 "**上游(upstream)**" 和 "**下游(downstream)**" 用于描述与报文流有关的方向性要求：所有报文都从上游流向下游。术语 "**(inbound)**" 和 "**出站(outbound)**" 用于描述与请求路线有关的方向性要求。"入站" 是指朝向源服务器，"出站" 是指朝向用户代理。

**代理(proxy)**"是一个报文转发代理，由客户选择，通常通过本地配置规则，接收对某些类型的绝对URI的请求，并试图通过HTTP接口的翻译来满足这些请求。一些转译是最小的，例如对 "http" URI的代理请求，而其他请求可能需要转译成完全不同的应用级协议。为了安全、注释服务或共享缓存，代理通常被用来通过一个共同的中介来组合一个组织的HTTP请求。一些代理被设计成在转发时对选定的报文或有效载荷进行转换，如5.7.2节所述。

**网关(gateway)** "（又称 "反向代理"）是一个中介，它作为出站连接的初始服务器，但转译收到的请求并将其转发到另一个或多个服务器。网关经常被用来封装传统的或不被信任的信息服务，通过 "加速器" 缓存来提高服务器的性能，并实现HTTP服务在多台机器上的分区或负载平衡。

所有适用于初始服务器的HTTP要求也适用于网关的出站通信。网关使用它所希望的任何协议与入站服务器进行通信，包括本规范范围之外的HTTP的私有扩展。然而，一个希望与第三方HTTP服务器互通的HTTP-to-HTTP网关应该符合网关入站连接的用户代理要求。

**隧道(tunnel)** "作为两个连接之间的盲目中继，不改变信息。一旦激活，隧道不被认为是HTTP通信的一方，尽管隧道可能是由一个HTTP请求发起的。当中继连接的两端都关闭时，隧道就不存在了。隧道被用来通过一个中介扩展一个虚拟连接，例如，当传输层安全（TLS，[RFC 5246]）被用来通过一个共享的防火墙代理建立保密通信。

上述中介的类别只考虑那些作为HTTP通信的参与者。也有一些中介机构可以在网络协议栈的较低层发挥作用，在信息发送方不知情或没有许可的情况下过滤或重定向HTTP流量。网络中介机构（在协议层面）与中间人攻击没有区别，往往由于错误地违反了HTTP语义而引入安全缺陷或互操作性问题。

例如，"拦截代理"[RFC 3040]（通常也被称为 "透明代理"[RFC 1919]或 "圈养门户"）与HTTP代理不同，因为它不是由客户端选择的。相反，拦截代理过滤或重定向传出的TCP 80端口数据包（偶尔也有其他普通端口流量）。拦截代理通常出现在公共网络接入点上，作为在允许使用非本地互联网服务之前执行账户订阅的一种手段，以及在企业防火墙内执行网络使用政策。

HTTP被定义为一个无状态协议，这意味着每个请求信息都可以被独立地理解。许多实现都依赖于HTTP的无状态设计，以便重复使用代理连接或在多个服务器上动态地平衡请求。因此，服务器不能假定同一连接上的两个请求是来自同一个用户代理，除非该连接是安全的，并且是特定于该代理的。一些非标准的HTTP扩展（例如，[RFC 4559]）已经被认为违反了这一要求，导致了安全和互操作性问题。

## 2.4. 缓存

**缓存(cache)** "是过去响应报文的本地存储，是控制其信息存储、检索和删除的子系统。缓存存储可缓存响应，以减少未来同等请求的响应时间和网络带宽消耗。任何客户端或服务器都可以使用缓存，尽管服务器在作为隧道时不能使用缓存。

缓存的作用是，如果链上的一个参与者有一个适用于该请求的缓存响应，那么请求/响应链就会缩短。下面说明了如果B拥有O（通过C）对一个没有被UA或A缓存的请求的早期响应的缓存副本，那么产生的链。


    >>>         >>>         >>>         >>>
UA =========== A =========== B - - - - - - C - - - - - - O
            <<<             <<<           <<<        <<<

如果允许缓存存储响应报文的副本以用于回答后续请求，那么响应就是 "可缓存的"。即使一个响应是可缓冲的，也可能有客户或原服务器对该缓冲响应何时可用于特定请求的额外限制。HTTP对缓冲行为和可缓冲响应的要求在[RFC 7234]的第2节中定义。

在万维网和大型组织内部部署了各种各样的架构和缓存配置。这些包括国家层次的代理缓存以节省跨洋带宽，广播或多播缓存条目的协作系统，用于离线或高延迟环境的预取缓存条目的档案，等等。

## 2.5. 符合性和错误处理

本规范根据HTTP通信中的参与者的角色来确定符合性标准。因此，HTTP要求被置于发送方、接收者、客户、服务器、用户代理、中介、初始服务器、代理、网关或缓存上，这取决于什么行为被要求所限制。额外的（社会）要求被放在实现、资源所有者和协议元素注册上，当它们适用于单个通信的范围之外。

动词 "生成 "被用来代替 "发送"，当需求区分了创建协议元素和仅仅将收到的元素转发给下游时。

如果一个实现符合与它在HTTP中的角色相关的所有要求，那么它就被认为是符合的。

符合性包括协议元素的语法和语义。发送方 **不得** 生成传达错误含义的协议元素，而该发送方知道这一点。发送方 **不得** 产生不符合相应ABNF规则所定义的语法的协议元素。在一个给定的报文中，发送方 **不得** 生成只允许由其他角色的参与者（即发送方对该报文不具有的角色）生成的协议元素或语法替代。

当收到的协议元素被解析时，接收者 **必须** 能够解析适用于接收者角色的任何合理长度的值，并且与相应的ABNF规则所定义的语法相匹配。然而，请注意，一些收到的协议元素可能不会被解析。例如，转发报文的中间人可能会将头字段解析为通用的字段名和字段值成分，但随后转发头字段，而不进一步解析字段值内部。

HTTP对它的许多协议元素没有具体的长度限制，因为可能适合的长度会有很大的不同，取决于部署环境和实现的目的。因此，发送方和接收方之间的互操作性取决于对每个协议元素的合理长度的共同期望。此外，在过去20年的HTTP使用过程中，人们普遍认为某些协议元素的合理长度已经发生了变化，预计未来还会继续变化。

至少，接收者 **必须** 能够解析和处理协议元素的长度，至少与它在其他报文中为这些相同的协议元素产生的值一样长。例如，一个发布非常长的URI引用到它自己的资源的初始服务器需要能够在收到请求目标时解析和处理这些相同的引用。

接收者 **必须** 根据本规范为其定义的语义（包括本规范的扩展）来解释收到的协议元素，除非接收者（通过经验或配置）确定发送方不正确地实现这些语义所暗示的内容。例如，如果对User-Agent首部字段的检查表明一个特定的实现版本在收到某些内容编码时是失败的，那么一个原点服务器可能会忽略收到的Accept-Encoding首部字段的内容。

除非另有说明，接收者 **可以** 尝试从一个无效的结构中恢复一个可用的协议元素。HTTP没有定义具体的错误处理机制，除非它们对安全有直接影响，因为协议的不同应用需要不同的错误处理策略。例如，网络浏览器可能希望透明地从位置头字段没有按照ABNF解析的响应中恢复，而系统控制客户端可能认为任何形式的错误恢复都是危险的。

## 2.6. 协议版本

HTTP使用"<主要版本号>.<次要版本号>"的编号方案来表示协议的版本。本规范定义了 "1.1" 版本。协议版本作为一个整体表明发送方符合该版本对应的HTTP规范中规定的一系列要求。

HTTP报文的版本由报文第一行的HTTP-version字段表示。HTTP-version是区分大小写的。

```
HTTP-version = HTTP-name "/" DIGIT "." DIGIT
HTTP-name = %x48.54.54.50 ; "HTTP", case-sensitive
```

HTTP版本号由两位小数组成，以"."（句号或小数点）分开。第一个数字（"主要版本号"）表示HTTP信息传递语法，而第二个数字（"次要版本号"）表示该主要版本中最高的次要版本，发送方符合并能够理解该版本，以便将来进行通信。次要版本通告发送方的通信能力，即使发送方只使用协议的向后兼容的子集，从而让接收方知道，更高级的功能可以在响应（由服务器）或未来的请求（由客户）中使用。

当HTTP/1.1报文被发送到HTTP/1.0接收方[RFC 1945]或版本未知的接收方时，HTTP/1.1报文的构造是，如果所有较新的功能被忽略，它可以被解释为一个有效的HTTP/1.0报文。本规范对一些新特性提出了接收方版本的要求，这样符合要求的发送方将只使用兼容的特性，直到它通过配置或收到的报文确定接收方支持HTTP/1.1。

一个首部字段的解释在同一主要HTTP版本的不同次要版本之间不会改变，尽管接收方在没有这样一个字段时的默认行为可能会改变。除非另有规定，在HTTP/1.1中定义的首部字段是为HTTP/1.x的所有版本定义的。特别是，所有HTTP/1.x的实现都应该实现Host和Connection首部字段，不管它们是否通告与HTTP/1.1一致。

如果新的首部字段定义的语义允许它们被不认识它们的接收者安全地忽略，那么可以在不改变协议版本的情况下引入这些字段。3.2.1节中讨论了首部字段的可扩展性。

处理HTTP报文的中介机构（即除了作为隧道的中介机构以外的所有中介机构）必须在转发的报文中发送自己的HTTP版本。换句话说，他们不允许盲目地转发HTTP报文的第一行，而不确保该报文中的协议版本与该中介在接收和发送报文时符合的版本一致。在没有重写HTTP-版本的情况下转发HTTP报文，当下游接收者使用报文发送者的版本来确定以后与该发送者的通信可以安全使用哪些功能时，可能会导致通信错误。

客户应该发送一个与客户符合的最高版本相等的请求版本，并且其主要版本不高于服务器所支持的最高版本，如果这是已知的。客户决不能发送它不符合的版本。

如果知道服务器不正确地实现了HTTP规范，客户可能会发送一个较低的请求版本，但只有在客户尝试了至少一个正常的请求并从响应状态代码或标题字段（例如，服务器）确定服务器不正确地处理较高的请求版本之后。

服务器应该发送一个等于服务器符合的最高版本的响应版本，该版本的主要版本小于或等于请求中收到的版本。服务器不应该发送它不符合的版本。如果服务器出于任何原因希望拒绝为客户的主要协议版本提供服务，它可以发送一个505（HTTP Version Not Supported）响应。

如果已知或怀疑客户端不正确地实现了HTTP规范，并且没有能力正确地处理后来的版本响应，例如，当客户端未能正确地解析版本号时，或者当已知中介机构盲目地转发HTTP-版本时，即使它不符合给定的协议的次要版本，服务器可能会对请求发送HTTP/1.0响应。这种协议降级不应该被执行，除非由特定的客户端属性触发，例如当一个或多个请求首部字段（如User-Agent）与已知有错误的客户端发送的值唯一匹配时。

HTTP版本设计的意图是，只有在引入不兼容的报文语法时，才会增加主版本号，而只有在对协议的修改具有增加报文语义或暗示发送者的额外能力的效果时，才会增加次版本号。然而，在[RFC 2068]和[RFC 2616]之间引入的变化中，次要版本没有被递增，这次修订特别避免了对协议的任何此类变化。

当收到一个HTTP报文，其主要版本号是接收方实现的，但其次要版本号比接收方实现的要高，接收方应将该报文作为接收方符合的该主要版本中的最高次要版本来处理。接收方可以认为，当发送至尚未表示支持更高版本的接收方时，具有更高次要版本的报文是充分向后兼容的，可以被同一主要版本的任何实现安全地处理。

## 2.7. 统一资源标识符(URI)

统一资源标识符（URI）[RFC 3986]在整个HTTP中被用作识别资源的手段（[RFC 7231]第2节）。URI引用被用来定位请求，指示重定向，并定义关系。

URI-reference"、"absolute-URI"、"relative-part"、"scheme"、"authority"、"port"、"host"、"path-abempty"、"segment"、"query "和 "fragment "的定义来自URI通用语法。一个 "绝对路径 "规则被定义为可以包含一个非空的路径组件的协议元素。(这个规则与RFC 3986的path-abempty规则略有不同，后者允许在引用中使用空路径，而path-absolute规则则不允许以"//"开头的路径）。) "部分URI "规则是为可以包含相对URI但不包含片段成分的协议元素而定义的。

```
URI-reference = <URI-reference, see [RFC3986], Section 4.1>
absolute-URI = <absolute-URI, see [RFC3986], Section 4.3>
relative-part = <relative-part, see [RFC3986], Section 4.2>
scheme = <scheme, see [RFC3986], Section 3.1>
authority = <authority, see [RFC3986], Section 3.2>
uri-host = <host, see [RFC3986], Section 3.2.2>
port = <port, see [RFC3986], Section 3.2.3>
path-abempty = <path-abempty, see [RFC3986], Section 3.3>
segment = <segment, see [RFC3986], Section 3.3>
query = <query, see [RFC3986], Section 3.4>
fragment = <fragment, see [RFC3986], Section 3.5>

absolute-path = 1*( "/" segment )
partial-URI = relative-part [ "?" query ]
```

HTTP中每个允许URI引用的协议元素将在其ABNF生产中指出该元素是否允许任何形式的引用（URI-reference），只允许绝对形式的URI（absolute-URI），只允许路径和可选查询组件，或上述的一些组合。除非另有说明，URI引用是相对于有效请求URI解析的（第5.5节）。

### 2.7.1. http URI 方案

在此定义 "http "URI方案，目的是根据其与潜在的HTTP初始服务器在特定端口上监听TCP（[RFC0793]）连接所管理的层次化命名空间的关联来铸造标识符。

```
http-URI = "http:" "//" authority path-abempty [ "?" query ] [ "#" fragment ]
```

http "URI的初始服务器是由授权组件确定的，其中包括一个主机标识和可选的TCP端口（[RFC3986]，第3.2.2节）。分层路径组件和可选的查询组件作为该源服务器命名空间中潜在目标资源的标识符。如[RFC3986]第3.5节所定义，可选片段组件允许间接识别二级资源，与URI方案无关。

发送方 **不得** 生成带有空主机标识符的 "http" URI。处理这种URI引用的接收者必须拒绝它，因为它是无效的。

如果主机标识符被提供为一个IP地址，那么初始服务器就是该IP地址上指定的TCP端口的监听器（如果有的话）。如果主机是一个注册的名字，注册的名字是一个间接的标识符，用于名称解析服务，如DNS，为该初始服务器找到一个地址。如果端口子组件是空的或没有给出，TCP端口80（为WWW服务保留的端口）是默认的。

Note that the presence of a URI with a given authority component does
not imply that there is always an HTTP server listening for
connections on that host and port. Anyone can mint a URI. What the
authority component determines is who has the right to respond
authoritatively to requests that target the identified resource. The
delegated nature of registered names and IP addresses creates a
federated namespace, based on control over the indicated host and
port, whether or not an HTTP server is present. See Section 9.1 for
security considerations related to establishing authority.

When an "http" URI is used within a context that calls for access to
the indicated resource, a client MAY attempt access by resolving the
host to an IP address, establishing a TCP connection to that address
on the indicated port, and sending an HTTP request message
(Section 3) containing the URI’s identifying data (Section 5) to the
server. If the server responds to that request with a non-interim
HTTP response message, as described in Section 6 of [RFC7231], then
that response is considered an authoritative answer to the client’s
request.

Although HTTP is independent of the transport protocol, the "http"
scheme is specific to TCP-based services because the name delegation
process depends on TCP for establishing authority. An HTTP service
based on some other underlying connection protocol would presumably
be identified using a different URI scheme, just as the "https"
scheme (below) is used for resources that require an end-to-end
secured connection. Other protocols might also be used to provide
access to "http" identified resources -- it is only the authoritative
interface that is specific to TCP.

The URI generic syntax for authority also includes a deprecated
userinfo subcomponent ([RFC3986], Section 3.2.1) for including user
authentication information in the URI. Some implementations make use
of the userinfo component for internal configuration of
authentication information, such as within command invocation
options, configuration files, or bookmark lists, even though such
usage might expose a user identifier or password. A sender MUST NOT
generate the userinfo subcomponent (and its "@" delimiter) when an
"http" URI reference is generated within a message as a request
target or header field value. Before making use of an "http" URI
reference received from an untrusted source, a recipient SHOULD parse
for userinfo and treat its presence as an error; it is likely being
used to obscure the authority for the sake of phishing attacks.