import re
import typing

import jl95terceira.pytools.pp as pp

REGEX         = 'PPJAVA'
SAFE_REGEX    = f'{REGEX}98006097C52D49A0961609C7E687AF2B'
BODY          = lambda r: f'{r}'
TAIL          = lambda r: f'{r}:TAIL'
COMMENT_BEGIN = '/*'
COMMENT_END   = '*/'

class CAPTURE:

    CODE = 'code'

class Processor(pp.Processor):

    @typing.override
    def __init__(self):

        super().__init__(pis=[pp.ProcessingInstruction(abort_if=lambda fcontent,_a=abort_if_match_safe_rex: ((lambda m: m) if _a else (lambda m: not m))(re.match(pattern=f'.*{SAFE_REGEX}.*',string=fcontent)),
                                                       pattern =f'{re.escape(COMMENT_BEGIN)} *{BODY(rex)}(?P<{CAPTURE.CODE}>.*?){re.escape(COMMENT_END)}.*?{re.escape(COMMENT_BEGIN)} *{TAIL(rex)} *{re.escape(COMMENT_END)}',
                                                       capture =lambda match                              : match.group(CAPTURE.CODE),
                                                       descape =lambda input                              : input.replace(COMMENT_END[:-1]+'\\'+COMMENT_END[-1], COMMENT_END),
                                                       repl    =lambda output,match,rex=rex               : f'{COMMENT_BEGIN} {BODY(rex)}{match.group(CAPTURE.CODE)}{COMMENT_END}\n{output}\n{COMMENT_BEGIN} {TAIL(rex)} {COMMENT_END}') for abort_if_match_safe_rex,rex in [(True,  REGEX), 
                                                                                                                                                                                                                                                                             (False, SAFE_REGEX)]])

if __name__ == '__main__': pp.main_simple(Processor(), 'Java')