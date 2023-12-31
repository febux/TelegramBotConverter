import argparse
import glob
import os
from typing import List, Callable, Optional, Union, Tuple


def arg_file_info(file: str, *, rel_path: bool = True, ide_col_suf: bool = True, line: int = 0, col: Optional[int] = None) -> str:
    suf = f':{line}{f":{col}" if col is not None else ""}' if ide_col_suf else ''
    return f'./{os.path.relpath(file, os.getcwd())}{suf}' if rel_path else file


def arg_file_glob_compile_files(include: Union[List[str], List[List[str]]], exclude: Optional[Union[List[str], List[List[str]]]] = None) -> Tuple[List[str], List[str]]:
    include_files = set()
    for inc in include:
        if not isinstance(inc, (list, tuple)):
            inc = [inc]
        for f in inc:
            assert isinstance(f, str), f'path must be str. "{type(f).__name__}" was given'
            include_files.add(os.path.abspath(f))

    exclude_files = set()
    for exc in (exclude or []):
        if not isinstance(exc, (list, tuple)):
            exc = [exc]
        for f in exc:
            assert isinstance(f, str), f'path must be str. "{type(f).__name__}" was given'
            exclude_files.add(os.path.abspath(f))

    res_files = include_files - exclude_files

    return list(sorted(res_files)), list(sorted(include_files - res_files))


def arg_files_glob(*, ignore_absent: bool = False, dir: bool = False) -> Callable[[str], List[str]]:
    def arg_files_glob_wr(value: str) -> List[str]:
        files: List[str] = list()
        if '*' in value:
            for gf in glob.iglob(value, recursive=True):
                gf_s = os.path.abspath(str(gf))
                if (dir and os.path.isdir(gf_s)) or (not dir and os.path.isfile(gf_s)):
                    files.append(os.path.abspath(gf_s))
        else:
            if (dir and os.path.isdir(value)) or (not dir and os.path.isfile(value)):
                files.append(os.path.abspath(value))
        if not ignore_absent and len(files) == 0:
            raise argparse.ArgumentTypeError(f'no files found with path template "{value}"')
        return files

    return arg_files_glob_wr
