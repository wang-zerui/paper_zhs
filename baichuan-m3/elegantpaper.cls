% Author: Dongsheng Deng
% Homepage: https://ddswhu.me/
% Email: elegantlatex2e@gmail.com
% Lastest Version: https://github.com/ElegantLaTeX/ElegantPaper
% --- Class structure: identification part
\ProvidesClass{elegantpaper}[2022/12/31 v0.11 ElegantLaTeX Paper class]
\NeedsTeXFormat{LaTeX2e}
\RequirePackage{kvoptions}
\RequirePackage{etoolbox}
\RequirePackage{calc}
\SetupKeyvalOptions{family=ELEGANT, prefix=ELEGANT@, setkeys=\kvsetkeys}
\newcommand{\ekv}[1]{\kvsetkeys{ELEGANT}{#1}}
\DeclareStringOption[en]{lang}
\DeclareVoidOption{cn}{\ekv{lang=cn}}
\DeclareVoidOption{en}{\ekv{lang=en}}
\DeclareStringOption[cm]{math}
\DeclareStringOption[numeric-comp]{citestyle}
\DeclareStringOption[numeric]{bibstyle}
\DeclareStringOption[bibtex]{bibend}
\DeclareVoidOption{biber}{\ekv{bibend=biber}}
\DeclareVoidOption{bibtex}{\ekv{bibend=bibtex}}
\DeclareStringOption[ctexfont]{chinesefont}
\DeclareVoidOption{ctexfont}{\ekv{chinesefont=ctexfont}}
\DeclareVoidOption{founder}{\ekv{chinesefont=founder}}
\DeclareVoidOption{nofont}{\ekv{chinesefont=nofont}}
\DeclareVoidOption{newtx}{\ekv{math=newtx}}
\DeclareVoidOption{mtpro2}{\ekv{math=mtpro2}}
\DeclareVoidOption{cm}{\ekv{math=cm}}
\DeclareDefaultOption{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessKeyvalOptions*\relax
\LoadClass{article}
% --- 1. 定义橙色系颜色 ---
\RequirePackage{xcolor}
\definecolor{mainorange}{RGB}{230, 100, 0}      % 主橙色
\definecolor{secondorange}{RGB}{255, 140, 0}    % 亮橙色
\definecolor{lightgrey}{rgb}{0.95,0.95,0.95}
\definecolor{commentcolor}{RGB}{0,100,0}
\definecolor{darkbrown}{RGB}{121, 85, 72}
% --- 2. 标题样式设置 ---
\RequirePackage{titlesec}
% section: 编号颜色为 mainorange，文字颜色保持默认(黑色)
\titleformat{\section}
  {\Large\bfseries}{\color{mainorange}\thesection}{1em}{}
% subsection:
\titleformat{\subsection}
  {\large\bfseries}{\color{mainorange}\thesubsection}{1em}{}
% subsubsection:
\titleformat{\subsubsection}
  {\normalsize\bfseries}{\color{mainorange}\thesubsubsection}{1em}{}
% --- Hyperref 设置 ---
\RequirePackage{hyperref}
\hypersetup{
  pdfborder={0 0 0},
  colorlinks=true,
  linkcolor={mainorange}, % 链接改为橙色
  urlcolor={mainorange},  % URL改为橙色
  filecolor={mainorange}, % 文件链接改为橙色
  citecolor={mainorange}, % 引用改为橙色
  linktoc=all,
}
% settings for the hyperref and geometry
\RequirePackage[
  left=1in,
  right=1in,
  top=1in,
  bottom=1in,
  headheight=0pt,
  headsep=0pt]{geometry}
\setlength{\headsep}{5pt}
\RequirePackage{amsthm}
\RequirePackage{amsmath}
\RequirePackage{amssymb}
% \RequirePackage{indentfirst} % --- 修改：取消首行缩进宏包 ---
\RequirePackage{booktabs}
\RequirePackage{multicol}
\RequirePackage{multirow}
\RequirePackage{graphicx}
\RequirePackage{fancyvrb}
\RequirePackage{abstract}
\RequirePackage{hologo}

% --- 修改部分：行距与段间距 ---
\linespread{1.35}           % 行距恢复为默认较舒适的 1.35
\setlength{\parskip}{1em}   % --- 修改：设置段落间距为 1em (约一行高度) ---

\graphicspath{{image/}{figure/}{fig/}{img/}}
% caption settings
\RequirePackage[labelfont={bf}]{caption}
\captionsetup[table]{skip=3pt}
\captionsetup[figure]{skip=3pt}
% list/itemize/enumerate setting
\RequirePackage[shortlabels,inline]{enumitem}
\setlist{nolistsep}
% 修改列表符号的颜色
\setlist[itemize,1]{label=\color{mainorange}\textbullet}
\setlist[enumerate,1]{label=\color{mainorange}\arabic*.}
% add the email cmd
\newcommand\email[1]{\href{mailto:#1}{\nolinkurl{#1}}}
% --- 字体设置 (修改为 Palatino 方案) ---
\PassOptionsToPackage{no-math}{fontspec}
\PassOptionsToPackage{quiet}{fontspec}
\RequirePackage{iftex}
\ifXeTeX
  \RequirePackage[no-math]{fontspec}
  % 将 texgyretermes (Times) 替换为 texgyrepagella (Palatino)
  \setmainfont{texgyrepagella}[
    UprightFont = *-regular ,
    BoldFont = *-bold ,
    ItalicFont = *-italic ,
    BoldItalicFont = *-bolditalic ,
    Extension = .otf ,
    Scale = 1.0]
  % 无衬线字体保持 Heros (类似 Helvetica)，与 Palatino 搭配良好
  \setsansfont{texgyreheros}[
    UprightFont = *-regular ,
    BoldFont = *-bold ,
    ItalicFont = *-italic ,
    BoldItalicFont = *-bolditalic ,
    Extension = .otf ,
    Scale = 0.9]
\else
  % 如果使用 pdfLatex，加载 newpxtext (Palatino) 而非 newtxtext (Times)
  \RequirePackage{newpxtext}
  \RequirePackage[scaled=.90]{helvet}
\fi
\ifdefstring{\ELEGANT@lang}{cn}{
  \ifdefstring{\ELEGANT@chinesefont}{founder}{
    \RequirePackage[UTF8,scheme=plain,fontset=none]{ctex}
    \setCJKmainfont[BoldFont={FZHei-B01},ItalicFont={FZKai-Z03}]{FZShuSong-Z01}
    \setCJKsansfont[BoldFont={FZHei-B01}]{FZKai-Z03}
    \setCJKmonofont[BoldFont={FZHei-B01}]{FZFangSong-Z02}
    \setCJKfamilyfont{zhsong}{FZShuSong-Z01}
    \setCJKfamilyfont{zhhei}{FZHei-B01}
    \setCJKfamilyfont{zhkai}[BoldFont={FZHei-B01}]{FZKai-Z03}
    \setCJKfamilyfont{zhfs}[BoldFont={FZHei-B01}]{FZFangSong-Z02}
    \newcommand*{\songti}{\CJKfamily{zhsong}}
    \newcommand*{\heiti}{\CJKfamily{zhhei}}
    \newcommand*{\kaishu}{\CJKfamily{zhkai}}
    \newcommand*{\fangsong}{\CJKfamily{zhfs}}}{\relax}
  \ifdefstring{\ELEGANT@chinesefont}{nofont}{
    \RequirePackage[UTF8,scheme=plain,fontset=none]{ctex}}{\relax}
  \ifdefstring{\ELEGANT@chinesefont}{ctexfont}{
    \RequirePackage[UTF8,scheme=plain]{ctex}}{\relax}
  \AfterEndPreamble{
    % --- 修改：将中文段落缩进设为 0 ---
    \setlength\parindent{0pt}}
}{\relax}
\ifcsname kaishu\endcsname
  \newcommand{\citshape}{\kaishu}
\else
  \newcommand{\citshape}{\itshape}
\fi
\ifcsname kaishu\endcsname
  \newcommand{\cnormal}{\kaishu}
\else
  \newcommand{\cnormal}{\normalfont}
\fi
\ifcsname fangsong\endcsname
  \newcommand{\cfs}{\fangsong}
\else
  \newcommand{\cfs}{\normalfont}
\fi
% --- 数学字体设置 (适配 Palatino) ---
\ifdefstring{\ELEGANT@math}{newtx}{
  % 将 newtxmath 替换为 newpxmath 以匹配 Palatino 风格
  \RequirePackage{newpxmath}
  \let\Bbbk\relax
  \RequirePackage{esint}
  \DeclareSymbolFont{CMlargesymbols}{OMX}{cmex}{m}{n}
  \let\sumop\relax\let\prodop\relax
  \DeclareMathSymbol{\sumop}{\mathop}{CMlargesymbols}{"50}
  \DeclareMathSymbol{\prodop}{\mathop}{CMlargesymbols}{"51}
}{\relax}
% ----------------------------------------------------------------
% 配置 biblatex
% ----------------------------------------------------------------
\RequirePackage[
  backend=\ELEGANT@bibend,
  citestyle=\ELEGANT@citestyle,
  bibstyle=\ELEGANT@bibstyle,
  sorting=none,  
  maxbibnames=6, 
  minbibnames=3  
]{biblatex}
% ----------------------------------------------------------------
\RequirePackage{appendix}
\ifdefstring{\ELEGANT@lang}{cn}{
  \theoremstyle{plain}% default
  \newtheorem{theorem}{定理}[section] %
  \newtheorem{lemma}[theorem]{引理} %
  \newtheorem{proposition}[theorem]{命题} %
  \newtheorem*{corollary}{推论} %
  \theoremstyle{definition} %
  \newtheorem{definition}{定义}[section] %
  \newtheorem{conjecture}{猜想}[section] %
  \newtheorem{example}{例}[section] %
  \theoremstyle{remark} %
  \newtheorem*{remark}{\normalfont\bfseries 评论} %
  \newtheorem*{note}{\normalfont\bfseries 注} %
  \newtheorem{case}{\normalfont\bfseries 案例} %
  \renewcommand*{\proofname}{\normalfont\bfseries 证明} %
  \renewcommand\contentsname{目录}
  \renewcommand\refname{参考文献} %
  \renewcommand\figurename{图} %
  \renewcommand\tablename{表}%
  \newcommand\versiontext{版本：}%
  \newcommand\updatetext{日期：}%
  \newcommand{\ebibname}{参考文献}
  \renewcommand\abstractname{摘\hspace{2em}要}
  % --- 修改：将中文段落缩进设为 0 ---
  \setlength\parindent{0pt}
  % --- 中文摘要字体: 与正文一致 ---
  \renewcommand{\abstracttextfont}{\normalfont\noindent\ignorespaces}
  \newcommand{\keywords}[1]{\vskip2ex\par\noindent\normalfont{\bfseries 关键词: } #1}
  \newcommand\figref[1]{{\bfseries 图~\ref{#1}}}
  \newcommand\tabref[1]{{\bfseries 表~\ref{#1}}}
  \renewcommand{\appendixtocname}{附录}
  \renewcommand{\appendixpagename}{附录}}{\relax}
\ifdefstring{\ELEGANT@lang}{en}{
  \theoremstyle{plain}% default
  \newtheorem{theorem}{Theorem}[section] %
  \newtheorem{lemma}[theorem]{Lemma} %
  \newtheorem{proposition}[theorem]{Proposition} %
  \newtheorem*{corollary}{Corollary} %
  \theoremstyle{definition} %
  \newtheorem{definition}{Definition}[section] %
  \newtheorem{conjecture}{Conjecture}[section] %
  \newtheorem{example}{Example}[section] %
  \theoremstyle{remark} %
  \newtheorem*{remark}{Remark} %
  \newtheorem*{note}{Note} %
  \newtheorem{case}{Case} %
  \renewcommand*{\proofname}{\normalfont\bfseries Proof}%
  \newcommand\versiontext{\itshape Version: }%
  \newcommand\updatetext{\itshape Date: }%
  % --- 修改：将英文段落缩进设为 0 ---
  \setlength\parindent{0pt}
  % --- 英文摘要字体: 与正文一致 ---
  \renewcommand{\abstracttextfont}{\normalfont\noindent\ignorespaces}
  \newcommand{\keywords}[1]{\vskip 2ex\par\noindent\normalfont{\bfseries Keywords: } #1}
  \newcommand\figref[1]{{\bfseries Figure~\ref{#1}}}
  \newcommand\tabref[1]{{\bfseries Table~\ref{#1}}}
  \newcommand{\ebibname}{Bibliography}}{\relax}
\def\bibfont{\footnotesize}
\AtBeginEnvironment{verbatim}{\microtypesetup{activate=false}}
\BeforeBeginEnvironment{tabular}{\small}
\AfterEndEnvironment{tabular}{}
\AtBeginDocument{
  \setlength{\abovedisplayskip}{3pt}
  \setlength{\belowdisplayskip}{3pt}
  \RequirePackage[flushmargin]{footmisc}
  \setlength{\footnotesep}{12pt}}
\def\IfEmpty#1{%
  \edef\1{\the#1}
  \ifx\1\empty
}
\newtoks\version
\newtoks\institute
\renewcommand\maketitle{\par
  \begingroup
    \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
    \def\@makefnmark{\rlap{\@textsuperscript{\normalfont\@thefnmark}}}%
    \long\def\@makefntext##1{\parindent 1em\noindent
            \hb@xt@0.1em{%
                \hss\@textsuperscript{\normalfont\@thefnmark}}##1}%
    \if@twocolumn
      \ifnum \col@number=\@ne
        \@maketitle
      \else
        \twocolumn[\@maketitle]%
      \fi
    \else
      \newpage
      \global\@topnum\z@   
      \@maketitle
    \fi
    \thispagestyle{plain}\@thanks
  \endgroup
  \setcounter{footnote}{0}%
  \global\let\thanks\relax
  \global\let\maketitle\relax
  \global\let\@maketitle\relax
  \global\let\@thanks\@empty
  \global\let\@author\@empty
  \global\let\@ELEGANT@version\@empty
  \global\let\@date\@empty
  \global\let\@title\@empty
  \global\let\title\relax
  \global\let\author\relax
  \global\let\date\relax
  \global\let\and\relax
  \global\let\ELEGANT@version\relax
}
\def\@maketitle{%
  \newpage
  \null
  \vskip 2em%
  \begin{center}%
  \let \footnote \thanks
    {\LARGE\bfseries \@title \par}%
    \vskip 1.5em%
    {\large
      \lineskip .5em%
      \begin{tabular}[t]{c}%
        \@author\\[1ex]
      \end{tabular}\par}
      \the\institute%
\vskip 0.5ex%
\IfEmpty\version
\else
{\small\normalfont\citshape\versiontext\the\version}
\fi
% --- 修改：去掉日期显示 ---
% \ifx\@date\empty
% \else
% \vskip 0.1em%
% {\small\normalfont\citshape\updatetext\@date}%
% \fi
  \end{center}%
  \par
}
% --- 代码高亮设置 ---
\RequirePackage{listings}
\renewcommand{\ttdefault}{cmtt}
\lstdefinestyle{estyle}{
  basicstyle=%
    \ttfamily
    \lst@ifdisplaystyle\footnotesize\fi
}
\lstset{basicstyle=\scriptsize\ttfamily,style=estyle}
\lstset{language=[LaTeX]TeX,
texcsstyle=*\color{mainorange},
numbers=none,
breaklines=true,
keywordstyle=\color{mainorange},
frame=tlbr,framesep=4pt,framerule=0pt,
commentstyle=\color{commentcolor},
emph={elegantpaper,fontenc,fontspec,xeCJK,FiraMono,xunicode,newtxmath,figure,fig,image,img,table,itemize,enumerate,newtxtext,newtxtt,ctex,microtype,description,times,newtx,booktabs,tabular,PDFLaTeX,XeLaTeX,type1cm,BibTeX,cite,gbt7714,lang},
emphstyle={\color{darkbrown}},
morekeywords={DeclareSymbolFont,SetSymbolFont,toprule,midrule,bottomrule,institute,version,includegraphics,setmainfont,setsansfont,setmonofont ,setCJKmainfont,setCJKsansfont,setCJKmonofont,RequirePackage,figref,tabref,email,maketitle,keywords,zhdate,zhtoday},
tabsize=2,
backgroundcolor=\color{lightgrey}
}
\renewcommand\ttdefault{lmtt}