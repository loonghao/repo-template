# 项目名称

<div align="center">

[![PyPI version](https://badge.fury.io/py/your-project-name.svg)](https://badge.fury.io/py/your-project-name)
[![Build Status](https://github.com/username/your-project-name/workflows/Build%20and%20Release/badge.svg)](https://github.com/username/your-project-name/actions)
[![Documentation Status](https://readthedocs.org/projects/your-project-name/badge/?version=latest)](https://your-project-name.readthedocs.io/en/latest/?badge=latest)
[![Python Version](https://img.shields.io/pypi/pyversions/your-project-name.svg)](https://pypi.org/project/your-project-name/)
[![License](https://img.shields.io/github/license/username/your-project-name.svg)](https://github.com/username/your-project-name/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/your-project-name)](https://pepy.tech/project/your-project-name)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/ruff-enabled-brightgreen)](https://github.com/astral-sh/ruff)

</div>

项目描述

## 从模板到可用仓库：三步

下面三步都是改名字，不需要从零搭建。

1. **建仓并命名包。**
   点击 **Use this template**，或执行
   `python scripts/apply_template.py ../my-new-repo --name my-new-repo`
   把同一套契约文件套到已存在的仓库。然后把 `src/your_project_name/`
   改名为 `src/<your_package>/`，并替换 `pyproject.toml` 和本文件中的
   `your-project-name` / `yourusername`。

2. **锁定工具链并安装。**
   按项目需要修改 `vx.toml` 的 `[tools]`，然后执行 `just install`。
   所有任务入口都在 `justfile`：`just lint`、`just test`、`just docs`、`just ci`。

3. **让契约门禁接管检查。**
   `.github/workflows/repo-contract.yml` 会在每个 PR 上跑
   [`dcc-mcp` 仓库契约](https://github.com/dcc-mcp/.github/blob/main/docs/repo-contract.md)：
   根目录无构建产物、`justfile` 全小写、存在 `AGENTS.md`、`vx.toml` 版本可解析、
   根目录条目在白名单内。模板开箱即通过；本地自检：

   ```bash
   python <dcc-mcp/.github>/scripts/check_repo_contract.py --root . --profile strict
   ```

## 特性

- 特性 1
- 特性 2
- 特性 3

## 安装

```bash
pip install your-project-name
```

或者使用 Poetry:

```bash
poetry add your-project-name
```

## 使用方法

```python
import your_project_name

# 在此添加使用示例
```

## 开发

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/username/your-project-name.git
cd your-project-name

# 使用 Poetry 安装依赖
poetry install
```

### 测试

```bash
# 统一从 justfile 进入，底层仍是 nox
just lint        # ruff + mypy
just lint-fix    # 自动修复
just test        # pytest 带覆盖率
just ci          # lint + test，与 CI 一致

# 也可以直接调用 nox
nox -s pytest
nox -s lint
nox -s lint-fix
```

### 文档

```bash
just docs         # 构建 Sphinx 文档
just docs-serve   # 带实时重载本地预览
```

### 仓库契约

```bash
# 对当前仓库跑 dcc-mcp 仓库契约
python <dcc-mcp/.github>/scripts/check_repo_contract.py --root . --profile strict
```

`AGENTS.md` 是编码 Agent 指令的唯一真源；`CLAUDE.md`、`GEMINI.md`、`CURSOR.md`
等都是指向它的 symlink。lint 配置统一放在 `pyproject.toml`，仓库里没有
`.flake8`、`.pylintrc`、`.coveragerc`，加回来会被契约门禁拦下。

## 许可证

MIT

## GitHub Actions 配置

此模板使用 GitHub Actions 进行 CI/CD。包含以下工作流：

- **构建和发布**：在多个 Python 版本和操作系统上测试包，并在创建新版本时发布到 PyPI。
- **文档**：构建文档并部署到 GitHub Pages。
- **依赖审查**：扫描依赖项中的安全漏洞。
- **Scorecards**：分析项目的安全健康状况。

发布工作流使用 PyPI 的可信发布（trusted publishing）功能，这意味着您不需要设置任何 PyPI API 令牌。相反，您需要在创建包后在 PyPI 项目设置中配置可信发布。有关更多信息，请参阅 [PyPI 关于可信发布的文档](https://docs.pypi.org/trusted-publishers/)。

### 发布流程

创建新版本的步骤：

1. 更新 `pyproject.toml` 中的版本号
2. 更新 `CHANGELOG.md`，添加新版本和变更内容
3. 提交并推送更改
4. 创建一个带有版本号的新标签（例如 `1.0.0`）
5. 将标签推送到 GitHub

```bash
# 发布流程示例
git add pyproject.toml CHANGELOG.md
git commit -m "Release 1.0.0"
git tag 1.0.0
git push && git push --tags
```

GitHub Actions 工作流将自动构建包并发布到 PyPI。
