import os
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable

from .read import scan_files


class DataFileConverter:
    def __init__(
        self,
        read_func: Callable,
        write_func: Callable,
        read_file_extension: str,
        write_file_extension: str,
        read_func_kwargs: dict[str, Any] | None = None,
        write_func_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """Initialize a data file converter

        Args:
            read_func (Callable): file reading function whose first argument is the file
                path
            write_func (Callable): file writing function whose first argument is the
                data waiting to be written and second argument is the file path
            read_file_extension (str): file extension for reading
            write_file_extension (str): file extension for writing
            read_func_kwargs (dict[str, Any] | None, optional): other arguments for
                reading function. Defaults to None.
            write_func_kwargs (dict[str, Any] | None, optional): other arguments for
                writing function. Defaults to None.
        """
        if read_func_kwargs is None:
            read_func_kwargs = {}
        if write_func_kwargs is None:
            write_func_kwargs = {}

        def _convert(file_path: str, inplace: bool = False) -> None:
            r_file_path = f"{file_path}.{read_file_extension}"
            w_file_path = f"{file_path}.{write_file_extension}"
            data = read_func(r_file_path, **read_func_kwargs)
            write_func(data, w_file_path, **write_func_kwargs)
            if inplace:
                os.remove(r_file_path)

        self._convert = _convert
        self._r_ext = read_file_extension

    def __call__(
        self, root_dir: str, n_threads: int | None = None, inplace: bool = False
    ) -> None:
        """Read and then write all files in a root directory by multithreading

        Args:
            root_dir (str): root directory
            n_threads (int | None, optional): number of threads. Defaults to None.
            inplace (bool, optional): delete original files or not. Defaults to False.
        """
        file_paths = scan_files(root_dir, self._r_ext)
        with ThreadPoolExecutor(n_threads) as pool:
            for file_path in file_paths:
                pool.submit(self._convert, file_path, inplace)