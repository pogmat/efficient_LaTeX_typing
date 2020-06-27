from re import sub as substitute
from re import escape
from argparse import ArgumentParser
from sys import stdout, stderr


SUBSTITUTIONS = {"†": "\\dagger",
                 "‖": "\\|",#‖
                 "⟨": "\\langle",
                 "≪": "\\ll",
                 "⟩": "\\rangle",
                 "≫": "\\gg",
                 "∑": "\\sum",
                 "∏": "\\prod",
                 "±": "\\pm",
                 "∓": "\\mp",
                 "⊕": "\\oplus",
                 "⊗": "\\otimes",
                 "∈": "\\in",
                 "∉": "\\notin",
                 "∫": "\\int",
                 "∮": "\\oint",
                 "∞": "\\infty",
                 "∝": "\\propto",
                 "∼": "\\sim",
                 "≃": "\\simeq",
                 "≠": "\\neq",
                 "≡": "\\equiv",
                 "∧": "\\wedge",
                 "∨": "\\vee",
                 "∂": "\\partial",
                 "∇": "\\nabla",
                 "ω": "\\omega",
                 "Ω": "\\Omega",
                 "ϵ": "\\epsilon",
                 "ε": "\\varepsilon",
                 "∃": "\\exists",
                 "ρ": "\\rho",
                 "∄": "\\nexists",
                 "τ": "\\tau",
                 "υ": "\\upsilon",
                 "Υ": "\\Upsilon",
                 "θ": "\\theta",
                 "Θ": "\\Theta",
                 "ι": "\\iota",
                 "ı": "\\imath",
                 "∅": "\\emptyset",
                 "π": "\\pi",
                 "Π": "\\Pi",
                 "α": "\\alpha",
                 "∀": "\\forall",
                 "σ": "\\sigma",
                 "Σ": "\\Sigma",
                 "δ": "\\delta",
                 "Δ": "\\Delta",
                 "φ": "\\varphi",
                 "ϕ": "\\phi",
                 "Φ": "\\Phi",
                 "γ": "\\gamma",
                 "Γ": "\\Gamma",
                 "η": "\\eta",
                 "ℏ": "\\hslash",
                 "ξ": "\\xi",
                 "Ξ": "\\Xi",
                 "κ": "\\kappa",
                 "ȷ": "\\jmath",
                 "λ": "\\lambda",
                 "Λ": "\\Lambda",
                 "⇔": "\\Leftrightarrow",
                 "⇒": "\\Rightarrow",
                 "∪": "\\cup",
                 "∩": "\\cap",
                 "≤": "\\leq",
                 "≥": "\\geq",
                 "ζ": "\\zeta",
                 "χ": "\\chi",
                 "×": "\\times",
                 "ψ": "\\psi",
                 "Ψ": "\\Psi",
                 "⊂": "\\subset",
                 "β": "\\beta",
                 "⊃": "\\supset",
                 "ν": "\\nu",
                 "⊆": "\\subseteq",
                 "μ": "\\mu",
                 "⊇": "\\supseteq",
                 "…": "\\dots",
                 "↔": "\\leftrightarrow",
                 "⋅": "\\cdot",
                 "•": "\\bullet",
                 "∘": "\\circ",
                 "→": "\\rightarrow",
                 "↦": "\\mapsto"}
                     
EXIT_CODES = ('$', '_', '^', '{', '}', '[', ']', '(', ')', '\\', ' ')


class output_file:
    """
    A simple class to handle file output and stdout in the same way
    """
    def __init__(self, filename=None):
        self._filename = filename
        
    def __enter__(self):
        if self._filename:
            self._fd = open(self._filename, 'w')
        else:
            self._fd = stdout
        return self._fd
    
    def __exit__(self, exc_type, exc_value, traceback):
        if self._filename:
            self._fd.close()


def substitute_all(text):
    # chatacters that need to be replaced adding an extra space:
    # those are che unicodes which are followed by an character
    # which does not belong to EXIT_CODES.
    # i.e. "a_αb_β"  cannot be transalted to "a_\alphab_beta";
    # the correct form is "a_\alpha b_\beta"
    pattern_space = '|'.join(escape(k) for k in SUBSTITUTIONS)
    replace_space = lambda m: SUBSTITUTIONS[m.group(0)] + ' '
    
    # chatacters that can be replaced as they stand.
    # i.e. "α_aβ_b" con be transalted to "\alpha_a\beta_b"
    exit_pattern = '|'.join(escape(e) for e in EXIT_CODES)
    pattern_no_space = '(' + pattern_space + ')(?=(' + pattern_space + '|' + exit_pattern + '))'
    replace_no_space = lambda m: SUBSTITUTIONS[m.group(0)]
    
    return substitute(pattern_space, replace_space, substitute(pattern_no_space, replace_no_space, text))


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('infile', type=str)
    parser.add_argument('outfile', nargs='?', type=str,
                        help='if omitted the output is on stdout')
    
    args = parser.parse_args()
    
    try:
        with open(args.infile, 'r') as infile, output_file(args.outfile) as outfile:
            for line in infile:
                outfile.write(substitute_all(line))
    except FileNotFoundError as not_found:
        print('File not found:', not_found.filename, file=stderr)
    except IOError:
        print('An I/O error has occurred', file=stderr)
