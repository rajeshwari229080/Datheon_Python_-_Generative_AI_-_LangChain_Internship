"""
Task 3: Multi-Tool Autonomous AI Agent
Tool 2: Restricted Sandboxed Local File Reader.
Strictly jails file reading operations to a designated safe workspace directory.
Blocks directory traversal (../), absolute root escapes, symlinks, and oversized files.
"""

from __future__ import annotations
import os
from typing import Optional


class FileAccessSecurityError(Exception):
    """Raised when an operation attempts directory traversal or unauthorized access."""
    pass


class SafeFileReader:
    """
    Safely reads file contents strictly confined inside a designated sandbox directory.
    Rejects path traversal, forbidden extensions, and files exceeding size budgets.
    """

    ALLOWED_EXTENSIONS = {".txt", ".csv", ".json", ".md", ".log"}
    MAX_FILE_BYTES = 500 * 1024  # 500 KB safety cap

    def __init__(self, workspace_dir: Optional[str] = None):
        if workspace_dir is None:
            # Default to local safe_workspace directory
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            workspace_dir = os.path.join(base_dir, "safe_workspace")

        self.workspace_dir = os.path.realpath(workspace_dir)
        os.makedirs(self.workspace_dir, exist_ok=True)

    def read_file(self, relative_path: str) -> str:
        """
        Safely reads a file within the sandboxed directory.
        Returns file content or an explicit, auditable security error message.
        """
        clean_path = relative_path.strip().lstrip("/\\")
        if not clean_path:
            return "Error: Empty filename specified."

        # Compute full target path
        target_path = os.path.realpath(os.path.join(self.workspace_dir, clean_path))

        # Check Jail / Boundary confinement
        try:
            # Under Windows or Unix, target_path must start with workspace_dir
            common_prefix = os.path.commonpath([self.workspace_dir, target_path])
            if common_prefix != self.workspace_dir:
                return (
                    f"Security Error: Path traversal attack detected! "
                    f"Requested path '{relative_path}' resolves outside the allowed sandbox jail."
                )
        except ValueError:
            # On Windows, comparing across different drives raises ValueError
            return "Security Error: Cross-drive access attempt blocked."

        # Verify extension whitelist
        ext = os.path.splitext(target_path)[1].lower()
        if ext not in self.ALLOWED_EXTENSIONS:
            return (
                f"Security Error: File extension '{ext}' is forbidden. "
                f"Allowed extensions: {sorted(list(self.ALLOWED_EXTENSIONS))}"
            )

        if not os.path.exists(target_path):
            return f"File Error: File '{clean_path}' does not exist in the sandbox workspace."

        if not os.path.isfile(target_path):
            return f"File Error: Target '{clean_path}' is a directory or special device, not a regular file."

        # Size check
        file_size = os.path.getsize(target_path)
        if file_size > self.MAX_FILE_BYTES:
            return f"Security Error: File size ({file_size} bytes) exceeds maximum limit of {self.MAX_FILE_BYTES} bytes."

        # Read safely
        try:
            with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            return content
        except Exception as e:
            return f"Read Error: Could not read file '{clean_path}': {e}"

    def list_files(self) -> list[str]:
        """Lists all readable files present in the safe workspace."""
        files = []
        for root, _, filenames in os.walk(self.workspace_dir):
            for name in filenames:
                ext = os.path.splitext(name)[1].lower()
                if ext in self.ALLOWED_EXTENSIONS:
                    full_p = os.path.join(root, name)
                    rel_p = os.path.relpath(full_p, self.workspace_dir)
                    files.append(rel_p)
        return sorted(files)
