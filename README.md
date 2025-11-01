# 🚀 Repopack - GitHub Repository Flattener for Claude

**Pack entire GitHub repositories into Claude-ready context in seconds.**

RepoStack is a powerful Model Context Protocol (MCP) server that transforms any GitHub repository into a single, beautifully formatted file that Claude can analyze instantly. No more manual copying, no more missing files—just pure codebase intelligence.

## 🎯 What It Does

RepoStack empowers Claude to:
- 📦 **Instant Access** - Fetch any GitHub repository with a single command
- 🔍 **Smart Extraction** - Automatically identifies and extracts relevant code files
- 📄 **Perfect Formatting** - Concatenates everything into a clean, navigable document
- 🤖 **Full Context** - Gives Claude the complete picture of any codebase

Perfect for code reviews, security audits, documentation generation, learning new frameworks, architecture analysis, and technical interviews.

## ✨ Features

- ✅ **Public & Private Repos** - Works with any GitHub repository
- ✅ **Intelligent Filtering** - Excludes dependencies, build files, and noise
- ✅ **40+ Languages** - Python, JavaScript, TypeScript, Go, Rust, and more
- ✅ **Configurable Limits** - Control how many files to include
- ✅ **Auto Branch Detection** - Finds main/master automatically
- ✅ **Beautiful Output** - Clean separators and file headers
- ✅ **Lightning Fast** - Async operations for maximum speed

## 🎬 Demo

```
You: "RepoStack, analyze https://github.com/facebook/react"

Claude: *fetches entire React codebase*
        "React is a declarative JavaScript library for building user interfaces..."
        *provides deep insights from the actual source code*
```

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Claude Desktop** application
- **GitHub Account** (for private repos)

## 🚀 Quick Start

### Step 1: Installation

```bash
# Clone RepoStack
git clone <your-repo-url>
cd repostack

# Install dependencies
pip install fastmcp httpx
```

**💡 Pro Tip:** Use a virtual environment:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
pip install fastmcp httpx
```

### Step 2: Configure Claude Desktop

#### Windows 🪟

1. Press `Win + R` and type: `%APPDATA%\Claude`
2. Create or edit `claude_desktop_config.json`
3. Add this configuration:

```json
{
  "mcpServers": {
    "repostack": {
      "command": "python",
      "args": ["D:\\path\\to\\repostack\\github_flattener.py"]
    }
  }
}
```

#### macOS 🍎

```bash
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

```json
{
  "mcpServers": {
    "repostack": {
      "command": "python3",
      "args": ["/path/to/repostack/github_flattener.py"]
    }
  }
}
```

#### Linux 🐧

```bash
nano ~/.config/Claude/claude_desktop_config.json
```

```json
{
  "mcpServers": {
    "repostack": {
      "command": "python3",
      "args": ["/path/to/repostack/github_flattener.py"]
    }
  }
}
```

### Step 3: Restart Claude

**Important:** Completely quit Claude Desktop (not just minimize) and restart it.

## 💬 Usage

Simply chat with Claude naturally:

### 🎯 Basic Commands

```
"Flatten https://github.com/openai/whisper"
```

```
"Use RepoStack on github.com/vercel/next.js"
```

```
"Analyze the codebase at https://github.com/microsoft/typescript"
```

### 🎨 Creative Prompts

**Code Review:**
```
"RepoStack https://github.com/user/project and review the code quality"
```

**Security Audit:**
```
"Find security vulnerabilities in https://github.com/user/webapp"
```

**Architecture Analysis:**
```
"Explain the architecture of https://github.com/nestjs/nest"
```

**Learning:**
```
"How does https://github.com/django/django handle authentication?"
```

**Documentation:**
```
"Create comprehensive docs for https://github.com/user/api"
```

**Migration Planning:**
```
"How would I migrate https://github.com/user/js-app to TypeScript?"
```

## ⚙️ Configuration

### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `repo_url` | string | ✅ Yes | - | GitHub URL or `owner/repo` format |
| `github_token` | string | ❌ No | None | Personal access token for private repos |
| `max_files` | number | ❌ No | 100 | Maximum files to include (prevents overwhelming context) |

### Examples

**Limit files:**
```
"Flatten https://github.com/large/repo with max 50 files"
```

**Private repository:**
```
"Flatten https://github.com/user/private with token ghp_your_token_here"
```

## 🔐 Private Repositories

For private repositories, you'll need a GitHub Personal Access Token:

1. Visit https://github.com/settings/tokens
2. Click **"Generate new token (classic)"**
3. Name it: `RepoStack MCP`
4. Select scope: **`repo`** (Full control of private repositories)
5. Click **"Generate token"**
6. Copy and save your token securely

**Usage:**
```
"Flatten https://github.com/mycompany/private-api with token ghp_abc123xyz"
```

## 📁 Supported File Types

RepoStack intelligently includes:

### Languages
`py` `js` `ts` `jsx` `tsx` `java` `cpp` `c` `h` `cs` `go` `rs` `rb` `php` `swift` `kt` `scala` `r` `m` `sh`

### Web
`html` `css` `scss` `sass` `less` `vue` `svelte`

### Config
`json` `yaml` `yml` `toml` `xml` `md` `txt`

### Special
`Makefile` `Dockerfile` `.gitignore` `.env.example`

## 🚫 Auto-Excluded

RepoStack automatically skips:
- 📁 Dependencies: `node_modules/`, `vendor/`, `dist/`, `build/`
- 🔒 Cache: `__pycache__/`, `.next/`, `.nuxt/`, `coverage/`
- 🔐 Env: `venv/`, `env/`, `.venv/`
- 📦 Lock files: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`
- 🗜️ Minified: `.min.js`, `.min.css`, `bundle.js`

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'fastmcp'"

```bash
pip install fastmcp httpx
```

### "Server disconnected immediately"

Check your Python path:
```bash
where python      # Windows
which python3     # macOS/Linux
```

Update your config with the **full path**:
```json
{
  "mcpServers": {
    "repostack": {
      "command": "C:\\Python313\\python.exe",
      "args": ["D:\\path\\to\\github_flattener.py"]
    }
  }
}
```

### "GitHub API rate limit exceeded"

You've hit GitHub's rate limit (60 requests/hour without auth).

**Solution:** Add a GitHub token to increase limit to 5,000/hour.

### "Can't see RepoStack in Claude"

1. ✅ Verify config file has no JSON syntax errors
2. ✅ Completely quit and restart Claude Desktop
3. ✅ Check logs: Claude → Help → View Logs
4. ✅ Test the server independently (see Testing section)

### "Repository not found (404)"

- Verify the repository URL is correct
- For private repos, ensure you're using a valid token
- Check that the repository hasn't been deleted or renamed

## 🧪 Testing

### Method 1: MCP Inspector (Recommended)

```bash
npx @modelcontextprotocol/inspector
```

Connect with:
- **Command:** `python` (or full path)
- **Args:** `D:\path\to\github_flattener.py`

### Method 2: Direct Test Script

Create `test.py`:

```python
import asyncio
import sys

# Add your imports here based on the test script from earlier
# Run the flatten function directly

asyncio.run(test())
```

Run:
```bash
python test.py
```

## 📊 Performance

RepoStack is optimized for speed:

- **Small repos** (<50 files): ~2-5 seconds
- **Medium repos** (50-200 files): ~5-15 seconds  
- **Large repos** (200+ files): ~15-30 seconds

*Times vary based on network speed and file sizes*

## 🔒 Security & Privacy

- ✅ All data stays between you, GitHub, and Claude
- ✅ No data is stored or logged by RepoStack
- ✅ Tokens are used only for API authentication
- ✅ Open source - audit the code yourself

## 🛠️ Development

### Project Structure

```
repostack/
├── github_flattener.py    # Main MCP server
├── requirements.txt       # Dependencies
├── README.md             # This file
├── LICENSE               # MIT License
└── tests/                # Test files
    └── test_mcp.py
```

### Contributing

We love contributions! 

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m 'Add amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📝 Requirements

Create `requirements.txt`:

```txt
fastmcp>=0.1.0
httpx>=0.27.0
```

Install:
```bash
pip install -r requirements.txt
```

## 🎓 Use Cases

### For Developers
- 🔍 Quick codebase exploration
- 🐛 Bug hunting across large projects
- 📚 Learning from popular open-source projects
- 🔄 Refactoring assistance

### For Teams
- 👀 Code review automation
- 📖 Documentation generation
- 🏗️ Architecture analysis
- 🔐 Security audits

### For Learners
- 📖 Study real-world codebases
- 🎯 Understand design patterns
- 🚀 Learn best practices
- 💡 Get explanations of complex code

## 🌟 Pro Tips

1. **Start Small:** Test with smaller repos first (< 50 files)
2. **Use Tokens:** Always use a GitHub token to avoid rate limits
3. **Limit Files:** Use `max_files` for very large repositories
4. **Be Specific:** Ask Claude specific questions about the code
5. **Combine Tools:** Use with Claude's other tools for maximum power

## 📜 License

MIT License - use it, modify it, ship it! See `LICENSE` file for details.

## 🙏 Credits

Built with love using:
- [FastMCP](https://github.com/jlowin/fastmcp) - Simplified MCP development
- [httpx](https://www.python-httpx.org/) - Modern async HTTP
- [Model Context Protocol](https://modelcontextprotocol.io/) - By Anthropic

## 📞 Support

Need help? Here's how to get it:

1. 📖 Check the [Troubleshooting](#-troubleshooting) section
2. 🔍 Review [MCP Documentation](https://modelcontextprotocol.io/docs/tools/debugging)
3. 💬 Open an [Issue on GitHub](your-repo-url/issues)
4. 📧 Contact: your-email@example.com

## 🚀 What's Next?

Upcoming features:
- [ ] Support for GitLab and Bitbucket
- [ ] Custom file filtering rules
- [ ] Diff analysis between branches
- [ ] Direct Git clone support
- [ ] Repository comparison tool
- [ ] Code statistics and insights

---

**⭐ If RepoStack helped you, give it a star on GitHub!**

Made with ❤️ by Om Manoj Sharma for the  developer community