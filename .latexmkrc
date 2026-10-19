# latexmk — configuração única do repositório.
# Funciona chamando latexmk a partir da raiz (o Makefile faz isso com -cd).
use Cwd qw(abs_path);
use File::Basename qw(dirname);

my $root = dirname(abs_path(__FILE__));

# Pacotes/classes em tex/ e bibliografia tex/refs.bib visíveis de qualquer pasta
# (o separador ":" final mantém os caminhos padrão do TeX)
$ENV{'TEXINPUTS'} = "$root/tex//:" . ($ENV{'TEXINPUTS'} // '');
$ENV{'BIBINPUTS'} = "$root/tex//:" . ($ENV{'BIBINPUTS'} // '');

$pdf_mode = 4;                     # 4 = LuaLaTeX
$lualatex = 'lualatex -shell-escape -interaction=nonstopmode -file-line-error %O %P';  # %P: aceita -pretex (handout)
$out_dir  = 'build';
$bibtex_use = 2;                   # roda biber quando necessário
@generated_exts = (@generated_exts, 'nav', 'snm', 'vrb', 'run.xml', 'bbl');
