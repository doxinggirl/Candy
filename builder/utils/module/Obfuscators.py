import zlib
import base64
import os
import rich
import ast
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn, SpinnerColumn
from rich import print as rprint

class Obfuscators:
    def __init__(self, include_imports: bool = False, recursion: int = 1):
        self.include_imports = include_imports
        self.recursion = max(1, recursion)
        self._imports = []

    def execute(self, filepath: str):
        if not os.path.isfile(filepath):
            rprint(f"[red] [-] File Not Found!: {filepath}")
            return

        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
        self.save_original_code(filepath, code)

        obfuscated_code = self.obfuscate(code)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(obfuscated_code)

        rprint(f"[blue][Py-Obfuscator-v1.3][white] {filepath} | obfuscated")

    def save_original_code(self, filepath: str, code: str):
        decode_filepath = "decode.txt"
        try:
            with open(decode_filepath, "w", encoding="utf-8") as f:
                f.write(code)
            rprint(f"[green][+] Original code saved as {decode_filepath}[/green]")
        except Exception as e:
            rprint(f"[red] [-] Failed to save original code: {e}[/red]")

    def obfuscate(self, code: str) -> str:
        code = self._strip_comments_and_docstrings(code)
        if self.include_imports:
            self._collect_imports(code)

        for _ in range(self.recursion):
            code = self._layer_base64_zlib(code)

        if self.include_imports:
            code = self._prepend_imports(code)

        return code

    def _strip_comments_and_docstrings(self, code: str) -> str:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.Module)):
                if (doc := ast.get_docstring(node)) is not None:
                    if node.body and isinstance(node.body[0], ast.Expr):
                        node.body[0] = ast.Pass()
        return ast.unparse(tree)

    def _collect_imports(self, code: str):
        tree = ast.parse(code)
        self._imports.clear()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    self._imports.append(f"import {name.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for name in node.names:
                    self._imports.append(f"from {module} import {name.name}")

    def _prepend_imports(self, code: str) -> str:
        import_code = "\n".join(self._imports)
        return import_code + "\n" + code

    def _layer_base64_zlib(self, code: str) -> str:
        compressed = zlib.compress(code.encode())
        encoded = base64.b64encode(compressed).decode()
        
        layer = f"""
import zlib, base64
# bobux
exec(zlib.decompress(base64.b64decode("{encoded}")).decode())
"""
        return layer.strip()
