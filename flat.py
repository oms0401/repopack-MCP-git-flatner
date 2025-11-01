#!/usr/bin/env python3
"""
MCP Server for flattening GitHub repositories into a single file.
Built using FastMCP for simplified server creation.
"""

import os
from typing import Optional
import httpx
from fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("github-flattener")

# Common code file extensions to include
CODE_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.h', '.hpp',
    '.cs', '.go', '.rs', '.rb', '.php', '.swift', '.kt', '.scala', '.r',
    '.m', '.mm', '.sh', '.bash', '.zsh', '.sql', '.html', '.css', '.scss',
    '.sass', '.less', '.vue', '.svelte', '.json', '.yaml', '.yml', '.toml',
    '.xml', '.md', '.txt', '.gitignore', '.env.example', 'Makefile', 'Dockerfile'
}

# Files to exclude
EXCLUDE_PATTERNS = {
    'package-lock.json', 'yarn.lock', 'pnpm-lock.yaml',
    '.min.js', '.min.css', 'bundle.js'
}

async def fetch_repo_tree(owner: str, repo: str, token: Optional[str] = None) -> list[dict]:
    """Fetch the repository file tree from GitHub API."""
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    headers = {"Accept": "application/vnd.github.v3+json"}
    if token:
        headers["Authorization"] = f"token {token}"
    
    # Try 'main' branch first, then 'master'
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=30.0)
        if response.status_code == 404:
            url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
            response = await client.get(url, headers=headers, timeout=30.0)
        
        response.raise_for_status()
        data = response.json()
        return data.get("tree", [])

async def fetch_file_content(owner: str, repo: str, path: str, token: Optional[str] = None) -> str:
    """Fetch individual file content from GitHub."""
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{path}"
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, timeout=30.0)
        if response.status_code == 404:
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/master/{path}"
            response = await client.get(url, headers=headers, timeout=30.0)
        
        if response.status_code == 200:
            try:
                return response.text
            except:
                return f"[Binary file: {path}]"
        return ""

def should_include_file(path: str) -> bool:
    """Determine if a file should be included based on extension and patterns."""
    # Check exclude patterns
    for pattern in EXCLUDE_PATTERNS:
        if pattern in path:
            return False
    
    # Check if it's in a common ignore directory
    ignore_dirs = ['node_modules/', '.git/', 'dist/', 'build/', '__pycache__/', 
                   'venv/', 'env/', '.next/', '.nuxt/', 'coverage/']
    if any(ignore_dir in path for ignore_dir in ignore_dirs):
        return False
    
    # Check file extension
    _, ext = os.path.splitext(path)
    filename = os.path.basename(path)
    return ext.lower() in CODE_EXTENSIONS or filename in CODE_EXTENSIONS

@mcp.tool()
async def flatten_github_repo(
    repo_url: str,
    github_token: Optional[str] = None,
    max_files: int = 100
) -> str:
    """
    Fetches a GitHub repository and flattens all code files into a single text output.
    
    Useful for providing entire codebases to LLMs for analysis.
    Accepts a GitHub repository URL or owner/repo format.
    
    Args:
        repo_url: GitHub repository URL (e.g., 'https://github.com/owner/repo') or 'owner/repo' format
        github_token: Optional GitHub personal access token for private repos or higher rate limits
        max_files: Maximum number of files to include (default: 100)
    
    Returns:
        Flattened repository content with all code files concatenated
    """
    # Parse repository owner and name
    repo_url = repo_url.strip().rstrip('/')
    if "github.com/" in repo_url:
        parts = repo_url.split("github.com/")[1].split("/")
        owner, repo = parts[0], parts[1]
    else:
        parts = repo_url.split("/")
        if len(parts) == 2:
            owner, repo = parts
        else:
            raise ValueError("Invalid repository URL format. Use 'owner/repo' or full GitHub URL")
    
    try:
        # Fetch repository tree
        tree = await fetch_repo_tree(owner, repo, github_token)
        
        # Filter files
        files_to_fetch = [
            item for item in tree 
            if item["type"] == "blob" and should_include_file(item["path"])
        ][:max_files]
        
        # Build flattened output
        output_lines = [
            f"# Flattened Repository: {owner}/{repo}",
            f"# Total files included: {len(files_to_fetch)}",
            "=" * 80,
            ""
        ]
        
        # Fetch and concatenate file contents
        for item in files_to_fetch:
            path = item["path"]
            content = await fetch_file_content(owner, repo, path, github_token)
            
            if content:
                output_lines.extend([
                    "",
                    f"{'=' * 80}",
                    f"# FILE: {path}",
                    f"{'=' * 80}",
                    content,
                    ""
                ])
        
        result = "\n".join(output_lines)
        return result
    
    except httpx.HTTPStatusError as e:
        raise Exception(f"GitHub API error: {e.response.status_code} - {e.response.text}")
    except Exception as e:
        raise Exception(f"Error flattening repository: {str(e)}")

if __name__ == "__main__":
    mcp.run()