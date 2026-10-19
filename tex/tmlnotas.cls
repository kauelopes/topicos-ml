% =====================================================================
%  tmlnotas.cls — classe para notas de aula, listas e apostila.
%
%  Opções:
%    apostila   cada \aula{}{} abre nova página e entra no sumário
%               (usado por apostila/main.tex)
%    lista      cabeçalho de lista de exercícios em vez de notas
% =====================================================================
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{tmlnotas}[2026/10/15 Notas de aula - Topicos em ML]

\newif\if@apostila \@apostilafalse
\newif\if@lista    \@listafalse
\DeclareOption{apostila}{\@apostilatrue}
\DeclareOption{lista}{\@listatrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{scrartcl}}
\ProcessOptions\relax

\LoadClass[a4paper,11pt,parskip=half-,headings=standardclasses]{scrartcl}

% ---------------------------------------------------------------------
% Fontes (LuaLaTeX)
% ---------------------------------------------------------------------
\RequirePackage{fontspec}
\RequirePackage{unicode-math}
\setmainfont{Libertinus Serif}
\setsansfont{Fira Sans}[BoldFont={Fira Sans SemiBold}]
\setmonofont{Fira Mono}[Scale=0.88]
\setmathfont{Libertinus Math}
\RequirePackage{microtype}

\RequirePackage[top=2.5cm,bottom=2.5cm,left=2.8cm,right=2.8cm,headsep=0.8cm]{geometry}
\RequirePackage{topicosml}
\RequirePackage{enumitem}
\RequirePackage[hidelinks]{hyperref}
\hypersetup{colorlinks=true, linkcolor=tmlblue, urlcolor=tmlblue, citecolor=tmlblue}
\RequirePackage[brazilian,nameinlink,noabbrev]{cleveref}

% Títulos em Fira Sans, na cor do curso
\addtokomafont{disposition}{\sffamily\color{tmlprimary}}
\addtokomafont{section}{\Large}
\addtokomafont{subsection}{\large}
\setkomafont{descriptionlabel}{\sffamily\bfseries}

% Teoremas numerados por aula
\RequirePackage{amsthm}

% ---------------------------------------------------------------------
% Cabeçalho/rodapé
% ---------------------------------------------------------------------
\RequirePackage[automark]{scrlayer-scrpage}
\clearpairofpagestyles
\setkomafont{pageheadfoot}{\sffamily\footnotesize\color{gray}}
\ihead{\tmlcursocurto}
\ohead{\ifnum\value{aula}>0 Aula~\theaula\ \textbullet\ \aulatitulocurto\fi}
\cfoot{\pagemark}
\pagestyle{scrheadings}

% ---------------------------------------------------------------------
% \aula{número}{título}[título curto para o cabeçalho]
% ---------------------------------------------------------------------
\newcounter{aula}
\newcommand{\aulatitulo}{}
\newcommand{\aulatitulocurto}{}
\renewcommand{\thesection}{\theaula.\arabic{section}}
\renewcommand{\theequation}{\theaula.\arabic{equation}}
\renewcommand{\thefigure}{\theaula.\arabic{figure}}
\renewcommand{\thetable}{\theaula.\arabic{table}}

\NewDocumentCommand{\aula}{m m o}{%
  \if@apostila\clearpage\fi
  \setcounter{aula}{#1}%
  \setcounter{section}{0}\setcounter{equation}{0}%
  \setcounter{figure}{0}\setcounter{table}{0}%
  \renewcommand{\aulatitulo}{#2}%
  \IfValueTF{#3}{\renewcommand{\aulatitulocurto}{#3}}{\renewcommand{\aulatitulocurto}{#2}}%
  \if@apostila
    \phantomsection
    \addcontentsline{toc}{part}{Aula #1\quad #2}%
  \fi
  \@cabecalhoaula
}

\newcommand{\@tipodoc}{\if@lista Lista de Exercícios\else Notas de Aula\fi}
\newcommand{\@cabecalhoaula}{%
  \thispagestyle{plain.scrheadings}%
  \begingroup\sffamily
  \noindent{\footnotesize\color{gray}\MakeUppercase{\tmlcurso}}\par\vspace{2pt}
  \noindent\textcolor{tmlaccent}{\rule{\linewidth}{1.2pt}}\par\vspace{8pt}
  \noindent{\large\color{tmlaccent}\@tipodoc\ \textbullet\ Aula \theaula}\par\vspace{2pt}
  \noindent{\LARGE\bfseries\color{tmlprimary}\aulatitulo}\par\vspace{6pt}
  \noindent{\small\color{gray}\tmlautor\ \textbullet\ \tmlsemestre}\par
  \endgroup
  \vspace{1.2em}%
}

% Capa da apostila
\newcommand{\capaapostila}{%
  \begin{titlepage}\sffamily
    \vspace*{4cm}
    {\color{tmlaccent}\rule{\linewidth}{2pt}}\par\vspace{1cm}
    {\Huge\bfseries\color{tmlprimary}\tmlcurso}\par\vspace{0.8cm}
    {\Large\color{gray}Notas de aula}\par\vfill
    {\large\tmlautor}\par
    {\color{gray}\tmlsemestre}
  \end{titlepage}}

\endinput
