%%%% Commonstack LaTeX Template
%%%% Adapted from the company arXiv template.

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{commonstack}
\LoadClassWithOptions{article}

\RequirePackage{etoolbox}
\RequirePackage[margin=1in]{geometry}
\RequirePackage{setspace}
\RequirePackage{placeins}
\RequirePackage{graphicx}
\RequirePackage{hyperref}
\RequirePackage{url}
\RequirePackage{booktabs}
\RequirePackage{amsfonts}
\RequirePackage{nicefrac}
\RequirePackage[scaled=0.94]{helvet}
\RequirePackage{microtype}
\microtypesetup{expansion=false}
\RequirePackage{xcolor}
\RequirePackage[most]{tcolorbox}
\RequirePackage{lineno}
\RequirePackage{nicematrix}

\newcommand\contributionlist{}
\newcommand\commonstackfont[1]{{\sffamily\bfseries #1}}

\definecolor{commonstackblue}{RGB}{31,33,136}
\definecolor{commonstackgray}{RGB}{95,95,105}
\definecolor{commonstacklightgray}{RGB}{246,247,250}
\definecolor{commonstacktext}{HTML}{1C2B33}
\definecolor{linkBlue}{RGB}{0,82,217}

\hypersetup{
    colorlinks=true,
    linkcolor=linkBlue,
    citecolor=linkBlue,
    urlcolor=linkBlue,
    pdfauthor={Commonstack},
    pdftitle={TwinRouterBench},
    pdfsubject={Artificial Intelligence},
    pdfkeywords={Commonstack, LLM routing, benchmark},
}

\renewcommand{\title}[1]{\newcommand{\titlelist}{\begin{center}{\LARGE\bfseries #1}\end{center}}}

\renewcommand\addtolist[5][]{
  \begingroup
    \if\relax#3\relax\def\sep{}\else\def\sep{#5}\fi
    \let\protect\@unexpandable@protect
    \xdef#3{\expandafter{#3}\sep #4[#1]{#2}}%
  \endgroup
}

\newcommand\authorlist{}
\newcommand\authorformat[2][]{\begin{center}{\sffamily #2$^{#1}$}\end{center}}
\renewcommand\author[2][]{\addtolist[#1]{#2}{\authorlist}{\authorformat}{, }}

\newcommand\affiliationlist{}
\newcommand\affiliationformat[2][]{\begin{center}{\small\sffamily $^{#1}$#2}\end{center}}
\newcommand\affiliation[2][]{\addtolist[#1]{#2}{\affiliationlist}{\affiliationformat}{, }}

\newcommand\metadatalist{}
\newcommand\metadataformat[2][]{{\small {\bfseries #1:} #2}}
\newcommand\metadata[2][]{\addtolist[#1]{#2}{\metadatalist}{\metadataformat}{\par}}

\renewcommand\date[1]{\metadata[\raisebox{-0.1em}{\includegraphics[height=1em]{figures/icons8-date-96.png}} Date]{#1}}
\newcommand\sourcecode[1]{\metadata[\raisebox{-0.1em}{\includegraphics[height=1em]{figures/github.png}} Code and Data]{\url{#1}}}
\newcommand\project[1]{\metadata[\raisebox{-0.1em}{\includegraphics[height=1em]{figures/icons8-website-100.png}} Project]{\url{#1}}}
\newcommand\demo[1]{\metadata[\raisebox{-0.2em}{\includegraphics[height=1em]{figures/icons8-robot-100.png}} Demo]{\url{#1}}}
\newcommand{\data}[1]{\metadata[\raisebox{-0.1em}{\includegraphics[height=1em]{figures/huggingface-color.png}} Data]{\url{#1}}}
\newcommand\correspondence[1]{\metadata[\raisebox{-0.1em}{\includegraphics[height=1em]{figures/icons8-email-96.png}} Correspondence]{\texttt{#1}}}
\newcommand\papertype[1]{\metadata[Type]{#1}}

\renewcommand{\abstract}[1]{\newcommand{\abstractlist}{{\color{commonstacktext} #1}}}

\newcommand{\mymaketitle}{%
  \setlength{\parindent}{0cm}
  \setlength{\parskip}{0.5cm}
  {
    \setlength{\parskip}{0cm}
    \raggedright
    {
      \setstretch{1.25}
      \titlelist\par
    }
    \vskip 0.2cm
    \authorlist\par
    \vskip 0.2cm
    \affiliationlist\par
    \contributionlist\par
  }
  \begin{tcolorbox}[colback=commonstacklightgray, left=0.5cm, right=0.5cm, top=0.5cm, bottom=0.5cm, arc=8pt, enhanced, frame hidden, before skip=0pt, grow to left by=1.5pt, grow to right by=1.5pt]
    \abstractlist\par
    \vskip 0.45cm
    \ifdefempty{\metadatalist}{}{\metadatalist\par}
  \end{tcolorbox}
  \FloatBarrier
}

\if@twocolumn
\renewcommand{\maketitle}{
\twocolumn[%
  \mymaketitle
  \vskip 0.38cm
]
}
\else
\renewcommand{\maketitle}{
  \mymaketitle
}
\fi

\setlength{\headheight}{24pt}
\setlength{\emergencystretch}{2em}

\renewcommand{\section}{\@startsection{section}{1}{\z@}%
                       {-3.5ex \@plus -1ex \@minus -.2ex}%
                       {2.3ex \@plus.2ex}%
                       {\normalfont\Large\bfseries\color{commonstackgray}}}
\renewcommand{\subsection}{\@startsection{subsection}{2}{\z@}%
                          {-3.25ex\@plus -1ex \@minus -.2ex}%
                          {1.5ex \@plus .2ex}%
                          {\normalfont\large\bfseries\color{commonstackgray}}}
\renewcommand{\subsubsection}{\@startsection{subsubsection}{3}{\z@}%
                             {-3.25ex\@plus -1ex \@minus -.2ex}%
                             {1.5ex \@plus .2ex}%
                             {\normalfont\normalsize\bfseries\color{commonstackgray}}}

\RequirePackage[font={small}]{caption}
\captionsetup[figure]{labelfont={bf},name={Figure},labelsep=period}
\captionsetup[table]{labelfont={bf},name={Table},labelsep=period}

\RequirePackage{natbib}
\bibliographystyle{unsrtnat}

\RequirePackage{fancyhdr}
\pagestyle{fancy}
\fancyhf{}
\fancyhead[L]{\includegraphics[height=1.45\baselineskip]{figures/commonstack.png}}
\fancyhead[R]{\commonstackfont{TwinRouterBench}}
\fancyfoot[C]{\thepage}
\renewcommand{\headrulewidth}{0.5pt}
\renewcommand{\footrulewidth}{0pt}

\endinput
