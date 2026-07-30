%%%%%%%%%
%
% Evolvent AI Research Paper Template
% Based on the UC Berkeley RAIL / Google DeepMind tech report template (CC BY-SA 4.0).
% Redesigned for Evolvent AI — high-end academic tech report aesthetic.
%
% \documentclass[11pt, letterpaper]{mystyle}
% Options: logo, copyright, nonumbering, internal, twocolumn
%
%%%%%%%%%

\NeedsTeXFormat{LaTeX2e}

%%======== Package options and base class ========
\RequirePackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\RequirePackage{xifthen}
\newboolean{nonumbering}
\newboolean{logo}
\newboolean{address}
\newboolean{copyright}
\newboolean{internal}
\DeclareOption{nonumbering}{\setboolean{nonumbering}{true}}
\DeclareOption{logo}{\setboolean{logo}{true}}
\DeclareOption{address}{\setboolean{address}{true}}
\DeclareOption{copyright}{\setboolean{copyright}{true}}
\DeclareOption{internal}{\setboolean{internal}{true}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{extarticle}}
\ProcessOptions
\LoadClass{extarticle}

%%======== Core packages ========
\AtEndOfClass{\RequirePackage[tracking=smallcaps,letterspace=20]{microtype}}
\RequirePackage[utf8]{inputenc}
\RequirePackage[T1]{fontenc}
\RequirePackage[english]{babel}
\RequirePackage{amsthm, amsmath, amsfonts, amssymb}
\RequirePackage{cmap}
\RequirePackage{url}
\RequirePackage{pifont}
\RequirePackage{textcomp}
\RequirePackage[overload]{textcase}
\RequirePackage{graphicx}
\RequirePackage{colortbl}
\RequirePackage{booktabs}
\RequirePackage{changepage}
\RequirePackage{tabularx}
\RequirePackage{datetime}
\RequirePackage{fancyhdr}
\RequirePackage{lastpage}
\RequirePackage{enumitem}
\setlist[itemize]{noitemsep, topsep=2pt}
\setlist[enumerate]{noitemsep, topsep=2pt}
\RequirePackage[explicit]{titlesec}
\RequirePackage{bibentry}
\RequirePackage{mdframed}
\RequirePackage{caption}
\RequirePackage{needspace}
\RequirePackage{tikz}
\usetikzlibrary{shadows.blur}

%%======== Fonts ========
% Linux Libertine: elegant serif used by Wikipedia, pairs beautifully with math
% libertinust1math: matching math font
% tgheros: Helvetica clone for headings/labels
% inconsolata: monospace
\RequirePackage{libertine}
\RequirePackage{libertinust1math}
\RequirePackage{tgheros}   % sans-serif for headings (Helvetica clone)
\RequirePackage{inconsolata}            % monospace

%%======== Colors ========
\definecolor{EvolventInk}{HTML}{1F2329}       % Lark near-black
\definecolor{EvolventAccent}{RGB}{50,90,180}    % Lark primary blue
\definecolor{EvolventAccentDark}{RGB}{36,86,214} % Lark darker blue
\definecolor{EvolventTeal}{RGB}{0,194,194}      % Lark teal accent
\definecolor{EvolventGray}{RGB}{100,106,115}      % Lark mid gray
\definecolor{EvolventLightGray}{RGB}{245,246,247} % Lark bg tint
\definecolor{EvolventBorder}{RGB}{196,203,226}    % Lark border
\definecolor{EvolventTitleDark}{RGB}{31,35,41} % Title box dark bg
\definecolor{EvolventTagBg}{HTML}{E5EEFF}     % Blue-tinted tag bg
\definecolor{EvolventTagFg}{HTML}{3370FF}     % Tag text
\definecolor{TinaCrimson}{HTML}{F54A45}       % Lark red

% Legacy aliases
\definecolor{LightBlue}{HTML}{E5EEFF}
\definecolor{DarkBlue}{HTML}{1F2329}
\definecolor{LARGBlue}{HTML}{3370FF}
\definecolor{IronGrey}{HTML}{646A73}

\RequirePackage[colorlinks=true,
  linkcolor=EvolventAccent,
  citecolor=EvolventAccentDark,
  urlcolor=EvolventAccent]{hyperref}

%%======== Margins ========
\RequirePackage[left=1.9cm, right=1.9cm, top=2.8cm, bottom=2.5cm,
  headheight=40pt, headsep=18pt, letterpaper]{geometry}
\setlength{\columnsep}{15pt}
\setlength{\parskip}{0pt plus 1pt}
\setlength{\parindent}{1em}

%%======== Font commands ========
\newcommand{\headerfont}{\color{EvolventGray}\normalfont\sffamily\fontsize{8}{10}\selectfont}
\newcommand{\titlefont}{\centering\color{EvolventInk}\libertine\bfseries\fontsize{20}{22}\selectfont}
\newcommand{\absfont}{\linespread{0.9}\fontsize{9.5}{13.5}\color{EvolventInk}\selectfont}
\newcommand{\footerfont}{\color{EvolventGray}\normalfont\sffamily\fontsize{7.5}{9}\selectfont}
\newcommand{\headingfont}{\color{EvolventInk}\bfseries\fontsize{13}{16}\selectfont}
\newcommand{\subheadingfont}{\color{EvolventInk}\bfseries\fontsize{11.5}{14}\selectfont}
\newcommand{\urlheaderfont}{\color{EvolventAccent}\sffamily\fontsize{8}{10}\selectfont}
\newcommand{\copyrightfont}{\normalfont\fontsize{7}{9}\selectfont}

%%======== Tokens ========
\newcommand{\keywords}[1]{\def\@keywords{#1}}
\newtoks\correspondingauthor
\newtoks\paperurl
\newtoks\reportnumber
\newdateformat{monthyeardate}{\THEYEAR-\THEMONTH-\THEDAY}
\setcounter{secnumdepth}{3}
\ifthenelse{\boolean{nonumbering}}{\setcounter{secnumdepth}{0}}{}

%%======== Author / affiliation ========
\RequirePackage{authblk}
\setcounter{Maxaffil}{0}
\setlength{\affilsep}{0.15em}
\renewcommand\Authfont{\centering\color{EvolventInk}\normalfont\bfseries\fontsize{11}{15}\selectfont}
\renewcommand\Affilfont{\centering\color{EvolventGray}\normalfont\fontsize{9}{16}\selectfont}
\makeatletter
\renewcommand\AB@affilsepx{,\ \protect\Affilfont}
\makeatother
\renewcommand\Authands{,\ and\ }

\newcommand{\internalonly}{}
\newcommand{\copyrightext}{\footerfont \textcopyright\,\the\year{} Evolvent AI}

%%======== Header / Footer ========
\pagestyle{fancy}

% First page style
\fancypagestyle{firststyle}{
  \fancyhead[L]{%
    \ifthenelse{\boolean{logo}}{%
      \raisebox{-4pt}{\includegraphics[height=12pt]{logo/evolvent-title.pdf}}%
    }{\headerfont\color{EvolventInk}\textbf{Evolvent AI}}%
  }
  \fancyhead[C]{}
  \fancyhead[R]{\raisebox{-3pt}{\ifthenelse{\boolean{logo}}%
  {\includegraphics[height=18pt]{logo/evolvent-icon.pdf}}%
  {\headerfont\color{EvolventInk}\textbf{Evolvent AI}}}}
  \renewcommand{\headrulewidth}{0pt}
  \fancyfoot[L]{\footerfont\color{EvolventAccent}\textbf{evolvent.co}}
  \fancyfoot[C]{}
  \fancyfoot[R]{\footerfont\thepage}
}

\fancypagestyle{firststyleplain}{
  \fancyhf{}
  \fancyhead[L]{%
    \ifthenelse{\boolean{logo}}{%
      \raisebox{-4pt}{\includegraphics[height=12pt]{logo/evolvent-title.pdf}}%
    }{\headerfont\color{EvolventInk}\textbf{Evolvent AI}}%
  }
  \fancyhead[C]{}
  \fancyhead[R]{%
    \ifdefined\paperurl\if\relax\the\paperurl\relax\else
      \href{\the\paperurl}{\urlheaderfont\itshape\the\paperurl}\fi\fi
  }
  \renewcommand{\headrulewidth}{0pt}
  \renewcommand{\footrulewidth}{0.4pt}
  \fancyfoot[L]{%
    \ifthenelse{\boolean{copyright}}{\copyrightext}{}%
  }
  \fancyfoot[C]{}
  \fancyfoot[R]{\footerfont\color{EvolventAccent}\textbf{evolvent.co}}
}

% Running pages
\makeatletter
\newcommand\runningtitle[1]{\renewcommand\@runningtitle{#1}}
\newcommand\@runningtitle{}

\fancyhead[L]{\raisebox{-3pt}{\ifthenelse{\boolean{logo}}%
  {\includegraphics[height=12pt]{logo/evolvent-title.pdf}}%
  {\headerfont\color{EvolventInk}\textbf{Evolvent AI}}}}
\fancyhead[C]{\headerfont\itshape\@runningtitle}
\fancyhead[R]{\raisebox{-3pt}{\ifthenelse{\boolean{logo}}%
  {\includegraphics[height=18pt]{logo/evolvent-icon.pdf}}%
  {\headerfont\color{EvolventInk}\textbf{Evolvent AI}}}}
\fancyfoot[L]{\footerfont\color{EvolventAccent}\textbf{evolvent.co}}
\fancyfoot[C]{}
\fancyfoot[R]{\footerfont\thepage}
\makeatother

\renewcommand{\headrulewidth}{0.4pt}
\renewcommand{\footrulewidth}{0pt}
\let\DefaultHeadRule\headrule
\renewcommand{\headrule}{\color{EvolventBorder}\DefaultHeadRule}

%%======== Abstract env (captures text for maketitle) ========
\renewenvironment{abstract}{\par\noindent\ignorespaces}{\par\bigskip}

\def\xabstract{abstract}
\long\def\abstract#1\end#2{\def\two{#2}\ifx\two\xabstract
  \long\gdef\theabstract{\ignorespaces#1}
  \def\go{\end{abstract}}\else
  \typeout{^^J^^J PLEASE DO NOT USE \string\begin...\string\end IN ABSTRACT^^J^^J}%
  #1\end{#2}
  \gdef\theabstract{\vskip12pt BADLY FORMED ABSTRACT\vskip12pt}%
  \let\go\relax\fi\go}

%%======== Colors for hero card ========
\definecolor{EvolventShadow}{RGB}{200,215,255}
\definecolor{EvolventAbsBg}{RGB}{240,244,255}

%%======== maketitle ========
\makeatletter
\newcommand{\abscontent}{%
  \noindent\parbox{\dimexpr\linewidth}{\absfont\theabstract}%
  \@ifundefined{@keywords}{}{%
    \vskip0.8em\noindent{\sffamily\footnotesize\bfseries\color{EvolventGray}Keywords:\ }%
    {\sffamily\footnotesize\color{EvolventGray}\@keywords}}%
}

\if@twocolumn
\renewcommand{\maketitle}{%
  \twocolumn[%
  \begin{center}
    \vskip4pt
    {\titlefont\color{EvolventInk}\@title\par}
    \vskip10pt
    {\@author\par}
    \vskip6pt
    {\color{EvolventBorder}\rule{\textwidth}{0.5pt}}
    \vskip10pt
  \end{center}
  \abscontent
  \vskip18pt
  ]}%
\else
\renewcommand{\maketitle}{%
  \vphantom{a}\vspace{-10mm}%
  \bgroup\setlength{\parindent}{0pt}%
  % ── Hero card: white bg, accent top border ──
  \begin{tcolorbox}[
    enhanced,
    colback=white,
    colframe=EvolventBorder,
    boxrule=0.6pt,
    arc=6pt,
    left=10mm, right=10mm, top=8mm, bottom=6mm,
    borderline north={3pt}{0pt}{EvolventAccent},
    fuzzy shadow={0pt}{-4pt}{6pt}{1pt}{EvolventShadow!40!white},
  ]
    % Tags
    \@ifundefined{@papertags}{}{%
      \begin{center}{\@papertags}\end{center}\vskip8pt}%
    % Title
    {\centering\libertine\bfseries\fontsize{20}{26}\selectfont\color{EvolventInk}\@title\par}%
    \vskip8pt
    % {\color{EvolventBorder}\rule{\linewidth}{0.5pt}}\vskip6pt
    % Author
    \begin{center}\normalfont\fontsize{10}{14}\selectfont\color{EvolventGray}\@author\end{center}%
    \vskip8pt
    {\color{EvolventAccent}\rule{\linewidth}{1pt}}\vskip6pt
    % Abstract label
    {\sffamily\bfseries\fontsize{8}{10}\selectfont\color{EvolventAccent}ABSTRACT}\vskip4pt
    % Abstract text
    {\linespread{1.05}\fontsize{9.2}{13}\selectfont\color{EvolventInk}\theabstract\par}%
    \vskip2mm
  \end{tcolorbox}%
  \vskip6mm
  \egroup
}%
\fi
\makeatother
\newcommand{\evolventtag}[1]{%
  \tcbox[on line,
    colback=EvolventTagBg, colframe=EvolventTagBg,
    arc=2pt, boxrule=0pt,
    left=5pt, right=5pt, top=1.5pt, bottom=1.5pt,
    fontupper=\sffamily\scriptsize\bfseries\color{EvolventTagFg}
  ]{#1}%
}
\newcommand{\papertags}[1]{\def\@papertags{#1}}

%%======== Section headings ========
% Section: bold sans + blue number, small caps title
\titleformat{\section}
  {\headingfont}
  {\textcolor{EvolventAccent}{\thesection.}}
  {0.7em}
  {#1}
  []

\titleformat{name=\section,numberless}
  {\headingfont}{}
  {0em}{#1}[]

% Subsection: bold serif, slightly smaller
\titleformat{\subsection}
  {\subheadingfont}
  {\thesubsection.}
  {0.65em}{#1}[]

\titleformat{\subsubsection}
  {\normalsize\bfseries\itshape}
  {\thesubsubsection.}
  {0.5em}{#1}[]

\titlespacing*{\section}{0pc}{3.6ex plus4pt minus2pt}{6pt}
\titlespacing*{\subsection}{0pc}{2.8ex plus3pt minus1.5pt}{3pt}
\titlespacing*{\subsubsection}{0pc}{1.8ex plus2pt minus1pt}{2pt}

%%======== Captions ========
\DeclareCaptionLabelSeparator{pipe}{:~}
\captionsetup{
  labelfont={bf,small},
  textfont={small},
  labelsep=pipe,
  singlelinecheck=off,
}
