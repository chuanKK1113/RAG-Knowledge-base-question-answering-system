# RAG 知识库问答系统

基于 RAG（Retrieval-Augmented Generation）架构的知识库问答系统。上传 PDF/TXT 文档后，AI 基于文档内容回答用户问题。

## 架构

```
Streamlit 前端 ──HTTP──> FastAPI 后端 ──> ChromaDB (本地)
                              │
                              ├──> sentence-transformers (本地 Embedding)
                              └──> DeepSeek API (LLM 生成)
```

## 快速开始

### 环境要求

- Python 3.11+
- pip

### 安装

```bash
# 1. 安装后端依赖
cd backend
pip install -r requirements.txt

# 2. 安装前端依赖
cd ../frontend
pip install -r requirements.txt
```

### 配置

```bash
# 从模板创建 .env 文件
cp .env.example backend/.env

# 编辑 backend/.env，填入你的 LLM API Key
# LLM_API_KEY=sk-your-key-here
# LLM_API_BASE=https://api.deepseek.com/v1
# LLM_MODEL=deepseek-v4-flash
```

### 启动

```bash
# 终端 1：启动后端
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# 终端 2：启动前端
cd frontend
streamlit run app.py --server.port 8501
```

打开浏览器访问 http://localhost:8501

## 功能

| 功能 | 说明 |
|------|------|
| 文档上传 | 支持 PDF / TXT / MD / CSV |
| 智能问答 | 基于文档内容的 RAG 问答，带引用来源 |
| 知识库管理 | 查看、删除已上传文档 |
| API 文档 | Swagger UI 在 http://localhost:8000/docs |

## API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/health` | 健康检查 |
| POST | `/documents/upload` | 上传文档 |
| GET | `/documents` | 文档列表 |
| DELETE | `/documents/{id}` | 删除文档 |
| POST | `/query` | RAG 问答（检索+生成） |
| POST | `/query/retrieve` | 仅检索 |
| GET | `/collections` | 集合列表 |

## 技术栈

- **后端**: FastAPI + Pydantic
- **前端**: Streamlit
- **向量数据库**: ChromaDB
- **Embedding**: sentence-transformers (all-MiniLM-L6-v2, 384 维)
- **LLM**: DeepSeek v4-flash (OpenAI 兼容)
- **分段策略**: 段落感知 + 滑窗重叠 (chunk=800, overlap=150)

## 配置项

所有配置通过 `.env` 文件管理：

```env
# Embedding（本地模型，无需 API）
EMBEDDING_MODEL=all-MiniLM-L6-v2
EMBEDDING_DIMENSIONS=384

# LLM API
LLM_API_BASE=https://api.deepseek.com/v1
LLM_API_KEY=sk-your-key-here
LLM_MODEL=deepseek-v4-flash
LLM_TEMPERATURE=0.1
LLM_MAX_TOKENS=1024

# ChromaDB
CHROMA_PERSIST_DIR=./data/chroma_db
CHROMA_COLLECTION_NAME=knowledge_base

# 分段
CHUNK_SIZE=800
CHUNK_OVERLAP=150

# 检索
TOP_K=5
SIMILARITY_THRESHOLD=0.7
```

## 运行测试

```bash
cd backend
pytest tests/ -v
```

## 项目结构

```
rag-knowledge-base/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI 入口
│   │   ├── config.py         # 配置管理
│   │   ├── dependencies.py   # 依赖注入
│   │   ├── models/           # Pydantic 数据模型
│   │   ├── routes/           # API 路由
│   │   └── services/         # 业务逻辑层
│   ├── tests/                # 测试
│   └── requirements.txt
├── frontend/
│   ├── app.py                # Streamlit 入口
│   ├── pages/                # 页面组件
│   ├── components/           # 公共组件
│   └── requirements.txt
├── data/
│   ├── chroma_db/            # 向量数据库持久化
│   ├── models/               # Embedding 模型缓存
│   └── uploads/              # 临时文件
└── README.md
```
