"""
Configuration Management
========================

Centralized configuration using Pydantic Settings for type-safe 
environment variable management.
"""

from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class QiLinkSettings(BaseSettings):
    """Application settings with environment variable support."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="QILINK_",
        case_sensitive=False,
        extra="ignore",
    )

    # OpenAI Configuration
    openai_api_key: SecretStr = Field(
        default=SecretStr(""),
        description="OpenAI API key for DALL-E image generation",
    )
    openai_model: str = Field(
        default="dall-e-3",
        description="OpenAI image model to use",
    )
    openai_image_size: Literal["1024x1024", "1792x1024", "1024x1792"] = Field(
        default="1024x1024",
        description="Generated image dimensions",
    )
    openai_image_quality: Literal["standard", "hd"] = Field(
        default="hd",
        description="Image quality setting",
    )

    # Network Configuration
    ping_target: str = Field(
        default="8.8.8.8",
        description="Target IP for latency measurement",
    )
    ping_timeout: float = Field(
        default=5.0,
        description="Ping timeout in seconds",
    )

    # Application Mode
    mock_mode: bool = Field(
        default=True,
        description="Use mock data instead of real API calls",
    )
    debug: bool = Field(
        default=False,
        description="Enable debug logging",
    )

    # UI Configuration
    app_title: str = Field(
        default="氣鏈 Qi-Link",
        description="Application title",
    )
    app_subtitle: str = Field(
        default="DePIN 風水節點 | Cyber-Metaphysics Protocol",
        description="Application subtitle",
    )

    @property
    def has_openai_key(self) -> bool:
        """Check if a valid OpenAI API key is configured."""
        key = self.openai_api_key.get_secret_value()
        return bool(key and key.startswith("sk-"))


@lru_cache
def get_settings() -> QiLinkSettings:
    """Get cached settings instance."""
    return QiLinkSettings()

