\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{jitagent_zh}[2026/09/04 JIT-Agent Chinese report class]

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax
\LoadClass{article}

\PassOptionsToPackage{table}{xcolor}

\RequirePackage{fontspec}
\RequirePackage{xeCJK}
\setmainfont{XCharter}
\setCJKmainfont[AutoFakeBold=2,AutoFakeSlant=0.2]{Songti SC}
\setCJKsansfont{Heiti SC}
\setCJKmonofont{Kaiti SC}
\XeTeXlinebreaklocale "zh"
\XeTeXlinebreakskip = 0pt plus 1pt
\RequirePackage[authoryear,round]{natbib}
\RequirePackage{microtype}
\RequirePackage{xcolor}
\RequirePackage{tcolorbox}
\tcbuselibrary{listings,breakable,skins}
\RequirePackage{listings}
\RequirePackage[
  a4paper,
  left=2.5cm,
  right=2.5cm,
  top=2.8cm,
  bottom=2.5cm,
  headheight=16pt,
  headsep=10pt,
  footskip=24pt
]{geometry}
\RequirePackage{graphicx}
\RequirePackage{caption}
\RequirePackage{subcaption}
\RequirePackage{float}
\RequirePackage{afterpage}
\RequirePackage{booktabs}
\RequirePackage{longtable}
\RequirePackage{enumitem}
\RequirePackage{array}
\RequirePackage{ragged2e}
\RequirePackage{amsmath}
\RequirePackage{amsfonts}
\RequirePackage{mathtools}
\RequirePackage[xcharter,bigdelims,vvarbb]{newtxmath}
\RequirePackage{adjustbox}
\RequirePackage{tabularx}
\RequirePackage{csquotes}
\RequirePackage{pifont}
\RequirePackage{titlesec}
\RequirePackage{titling}
\RequirePackage{hyperref}
\RequirePackage{tikz}
\RequirePackage{xltabular}
\RequirePackage{eso-pic}
\RequirePackage{xspace}
\RequirePackage{setspace}

\definecolor{tealblue}{RGB}{16, 102, 102}
\definecolor{tealblueLight}{RGB}{232, 245, 244}
\definecolor{brightteal}{RGB}{45, 170, 165}
\definecolor{headerbg}{RGB}{240, 242, 245}
\definecolor{goodgreen}{RGB}{40, 140, 60}
\definecolor{badred}{RGB}{200, 50, 50}
\definecolor{principlebg}{RGB}{248, 249, 250}

\hypersetup{
  colorlinks=true,
  linkcolor=tealblue,
  citecolor=brightteal,
  urlcolor=brightteal
}
\urlstyle{same}

\newcommand{\jitbodyfont}{\fontsize{10.5pt}{13.7pt}\selectfont}
\newcommand{\jitabstractfont}{\fontsize{9.8pt}{12.6pt}\selectfont}
\newcommand{\jitsectionfont}{\fontsize{13pt}{15.5pt}\selectfont}
\newcommand{\jitsubsectionfont}{\fontsize{11.2pt}{13.8pt}\selectfont}
\newcommand{\jitsubsubsectionfont}{\fontsize{10.5pt}{13.2pt}\selectfont}

\AtBeginDocument{\jitbodyfont}
\setlength{\parindent}{0pt}
\setlength{\parskip}{5pt plus 1pt minus 0.5pt}
\setlength{\emergencystretch}{2em}
\setlength{\jot}{3pt}
\setlength{\abovedisplayskip}{8pt plus 2pt minus 2pt}
\setlength{\belowdisplayskip}{8pt plus 2pt minus 2pt}
\setlength{\abovedisplayshortskip}{4pt plus 2pt}
\setlength{\belowdisplayshortskip}{6pt plus 2pt minus 1pt}

\pretitle{\par\begingroup\centering}
\posttitle{\par\endgroup\vspace{0.55em}}
\preauthor{\par\begingroup\centering\jitbodyfont}
\postauthor{\par\endgroup\vspace{0.4em}}
\predate{}
\postdate{}

\titleformat{\section}{\jitsectionfont\bfseries\color{tealblue}}{\thesection}{0.7em}{}
\titleformat{\subsection}{\jitsubsectionfont\bfseries\color{tealblue}}{\thesubsection}{0.7em}{}
\titleformat{\subsubsection}{\jitsubsubsectionfont\bfseries\color{tealblue}}{\thesubsubsection}{0.7em}{}
\titleformat{\paragraph}[runin]{\jitbodyfont\bfseries\color{tealblue}}{}{0pt}{}

\titlespacing*{\section}{0pt}{2.8ex plus 0.8ex minus 0.4ex}{0.8ex}
\titlespacing*{\subsection}{0pt}{2.3ex plus 0.6ex minus 0.3ex}{0.55ex}
\titlespacing*{\subsubsection}{0pt}{1.9ex plus 0.5ex minus 0.2ex}{0.4ex}
\titlespacing*{\paragraph}{0pt}{1.3ex plus 0.4ex minus 0.2ex}{0.65em}

\renewenvironment{abstract}
  {\par\vspace{0.3em}
   \begin{tcolorbox}[
     enhanced,
     width=0.96\textwidth,
     center,
     colback=tealblueLight,
     colframe=tealblueLight,
     boxrule=0pt,
     arc=2pt,
     left=10pt,
     right=10pt,
     top=6pt,
     bottom=7pt,
     before skip=0pt,
     after skip=0pt
   ]
   {\centering
     \fontsize{10.5pt}{12.2pt}\selectfont\bfseries\color{tealblue}Abstract\par}
   \vspace{0.1em}
   \jitabstractfont\setlength{\parindent}{0pt}\setlength{\parskip}{3pt}\ignorespaces}
  {\end{tcolorbox}\par\vspace{0.1em}}

\setlist[itemize]{
  itemsep=2.5pt,
  parsep=0pt,
  topsep=4pt,
  partopsep=0pt,
  leftmargin=*
}

\DeclareCaptionFont{jitcaption}{\fontsize{9.2pt}{11.5pt}\selectfont}
\DeclareCaptionFont{jitsubcaption}{\fontsize{8.7pt}{10.7pt}\selectfont}
\captionsetup{
  font=jitcaption,
  labelfont=bf,
  skip=5.5pt
}
\captionsetup[table]{
  font=jitcaption,
  skip=4pt
}
\captionsetup[subfigure]{
  font=jitsubcaption
}

\renewcommand{\topfraction}{0.92}
\renewcommand{\bottomfraction}{0.85}
\renewcommand{\textfraction}{0.07}
\renewcommand{\floatpagefraction}{0.78}

\newcommand{\cmark}{\textcolor{goodgreen}{\ding{51}}}
\newcommand{\xmark}{\textcolor{badred}{\ding{55}}}
