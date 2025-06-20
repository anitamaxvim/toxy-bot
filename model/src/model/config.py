import os
from dataclasses import dataclass, field
from multiprocessing import cpu_count
from pathlib import Path

this_file = Path(__file__)
root_path = this_file.parents[2]

LABELS: list[str] = [
    "toxic",
    "severe_toxic",
    "obscene",
    "threat",
    "insult",
    "identity_hate",
]


@dataclass(frozen=True)
class Config:
    cache_dir: str | Path = field(
        default_factory=lambda: os.path.join(root_path, "data")
    )
    log_dir: str | Path = field(default_factory=lambda: os.path.join(root_path, "logs"))
    ckpt_dir: str | Path = field(
        default_factory=lambda: os.path.join(root_path, "checkpoints")
    )
    seed: int = 0


@dataclass
class DataModuleConfig:
    dataset_name: str = "anitamaxvim/toxy-dataset"
    labels: list[str] = field(default_factory=lambda: LABELS)
    train_split: str = "balanced_train"
    test_split: str = "test"
    batch_size: int = 64
    max_seq_length: int = 512
    train_size: float = 0.80
    stratify_by_column: str = "toxic"
    num_workers: int = field(default_factory=cpu_count)


@dataclass
class ModuleConfig:
    model_name: str = "google/bert_uncased_L-2_H-128_A-2"  # Tiny Bert
    learning_rate: float = 3e-5
    finetuned: str = field(
        default_factory=lambda: os.path.join(
            this_file.parent,
            "checkpoints",
            "google-bert-uncased-L-2-H-128-A-2_LR3e-5_BS64_MSL512_20250430-161306.ckpt",
        )
    )


@dataclass
class TrainerConfig:
    accelerator: str = "auto"
    devices: int | str = "auto"
    strategy: str = "auto"
    precision: str | None = "16-mixed"
    max_epochs: int = 10
    log_every_n_steps: int | None = 50
    deterministic: bool = True


@dataclass
class ServerConfig:
    finetuned: str = (
        "google-bert-uncased-L-2-H-128-A-2_LR3e-5_BS64_MSL512_20250430-161306.ckpt"
    )
    accelerator: str = "auto"
    devices: int | str = "auto"
    timeout: int = 30
    track_requests: bool = True
    generate_client_file: bool = False


CONFIG = Config()
DATAMODULE_CONFIG = DataModuleConfig()
MODULE_CONFIG = ModuleConfig()
TRAINER_CONFIG = TrainerConfig()
SERVER_CONFIG = ServerConfig()
