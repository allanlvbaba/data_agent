import os
from dataclasses import dataclass
from pathlib import Path

from app.config.config_loader import load_config


# 日志配置
@dataclass
class File:
    enable: bool
    level: str
    path: str
    rotation: str
    retention: str


@dataclass
class Console:
    enable: bool
    level: str


@dataclass
class LoggingConfig:
    file: File
    console: Console


# 数据库配置
@dataclass
class DBConfig:
    host: str
    port: int
    user: str
    password: str
    database: str


@dataclass
class QdrantConfig:
    host: str
    port: int
    embedding_size: int


@dataclass
class EmbeddingConfig:
    host: str
    port: int
    model: str


@dataclass
class ESConfig:
    host: str
    port: int
    index_name: str


@dataclass
class LLMConfig:
    model_name: str
    api_key: str
    base_url: str = ""


@dataclass
class AppConfig:
    logging: LoggingConfig
    db_meta: DBConfig
    db_dw: DBConfig
    qdrant: QdrantConfig
    embedding: EmbeddingConfig
    es: ESConfig
    llm: LLMConfig


config_file = Path(__file__).parents[2] / 'conf' / 'app_config.yaml'
app_config: AppConfig = load_config(AppConfig, config_file)


def _load_dotenv(path: Path) -> None:
    """极简 .env 加载器:仅支持 KEY=VALUE 与 # 注释,不覆盖已存在的环境变量。"""
    if not path.exists():
        return
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        key, _, value = line.partition('=')
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _apply_env_overrides() -> None:
    """敏感账密只从环境变量注入,配置文件(conf/*.yaml)中不落明文。"""
    db_password = os.getenv('APP_DB_PASSWORD', '')
    if db_password:
        app_config.db_meta.password = db_password
        app_config.db_dw.password = db_password
    else:
        print('[config] 提示: 未配置 APP_DB_PASSWORD(参考 .env.example),数据库将无法连接')

    api_key = os.getenv('APP_LLM_API_KEY', '')
    if api_key:
        app_config.llm.api_key = api_key
    else:
        print('[config] 提示: 未配置 APP_LLM_API_KEY(参考 .env.example),大模型将无法调用')


_load_dotenv(Path(__file__).parents[2] / '.env')
_apply_env_overrides()

if __name__ == '__main__':
    print(app_config.db_meta.port)

