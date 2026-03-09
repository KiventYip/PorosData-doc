#!/bin/bash
# deploy.sh - 自动化部署脚本 (支持 GitHub Pages 和 ReadTheDocs)

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查依赖
check_dependencies() {
    log_info "检查依赖..."

    if ! command -v python &> /dev/null; then
        log_error "Python 未安装"
        exit 1
    fi

    if ! command -v pip &> /dev/null; then
        log_error "pip 未安装"
        exit 1
    fi

    if ! command -v git &> /dev/null; then
        log_error "Git 未安装"
        exit 1
    fi

    log_success "依赖检查通过"
}

# 安装依赖
install_dependencies() {
    log_info "安装项目依赖..."
    pip install -r requirements.txt
    log_success "依赖安装完成"
}

# 初始化文档
init_docs() {
    log_info "初始化文档结构..."
    if [ -f "init_docs.py" ]; then
        python init_docs.py
        log_success "文档初始化完成"
    else
        log_warning "init_docs.py 不存在，跳过文档初始化"
    fi
}

# 构建文档
build_docs() {
    log_info "构建文档..."
    mkdocs build --clean
    log_success "文档构建完成"
}

# 本地预览
serve_docs() {
    log_info "启动本地预览服务器..."
    log_info "访问 http://localhost:8000 查看文档"
    mkdocs serve
}

# GitHub Pages 部署
deploy_github() {
    log_info "部署到 GitHub Pages..."

    # 检查是否在 git 仓库中
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "不在 Git 仓库中"
        exit 1
    fi

    # 检查是否有未提交的更改
    if ! git diff-index --quiet HEAD --; then
        log_warning "有未提交的更改，请先提交或暂存"
        read -p "是否继续? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    # 部署到 GitHub Pages
    mkdocs gh-deploy --force

    log_success "GitHub Pages 部署完成"
    log_info "访问 https://YOUR_USERNAME.github.io/YOUR_REPO/ 查看文档"
}

# 显示帮助
show_help() {
    cat << EOF
PorosData 文档部署工具

用法: $0 [选项]

选项:
    -h, --help          显示此帮助信息
    -i, --init          初始化文档结构
    -b, --build         构建文档
    -s, --serve         本地预览文档
    -d, --deploy        部署到 GitHub Pages
    --all               执行完整流程 (初始化 -> 构建 -> 部署)

示例:
    $0 --init           # 初始化文档
    $0 --serve          # 本地预览
    $0 --all            # 完整部署流程

环境变量:
    GITHUB_REPO         GitHub 仓库名 (格式: username/repo)
    GITHUB_TOKEN        GitHub 个人访问令牌 (用于 CI/CD)

EOF
}

# 主函数
main() {
    # 默认执行完整流程
    if [ $# -eq 0 ]; then
        set -- "--all"
    fi

    while [[ $# -gt 0 ]]; do
        case $1 in
            -h|--help)
                show_help
                exit 0
                ;;
            -i|--init)
                check_dependencies
                install_dependencies
                init_docs
                shift
                ;;
            -b|--build)
                check_dependencies
                install_dependencies
                build_docs
                shift
                ;;
            -s|--serve)
                check_dependencies
                install_dependencies
                serve_docs
                shift
                ;;
            -d|--deploy)
                check_dependencies
                install_dependencies
                build_docs
                deploy_github
                shift
                ;;
            --all)
                check_dependencies
                install_dependencies
                init_docs
                build_docs
                deploy_github
                shift
                ;;
            *)
                log_error "未知选项: $1"
                show_help
                exit 1
                ;;
        esac
    done
}

# 执行主函数
main "$@"