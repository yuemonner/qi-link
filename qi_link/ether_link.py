"""
Ether Link - The Web3 Layer
===========================

Blockchain simulation module for generating immutable proof
of existence for talisman metadata.
"""

import json
import secrets
import time
from datetime import datetime
from typing import Optional

from web3 import Web3

from qi_link.exceptions import HashingError
from qi_link.models import Diagnosis, TalismanMetadata


class EtherLink:
    """Web3 interface for simulating on-chain operations."""

    def __init__(self):
        self._web3 = Web3()
        self._mock_block_number = self._generate_mock_block_number()

    def create_talisman_metadata(self, diagnosis: Diagnosis, image_url: str, location_ip: Optional[str] = None, location_region: Optional[str] = None) -> TalismanMetadata:
        token_id = self._generate_token_id()
        metadata = TalismanMetadata(
            token_id=token_id,
            created_at=datetime.now(),
            location_ip=location_ip or self._get_mock_ip(),
            location_region=location_region or "Cyber Realm",
            diagnosis=diagnosis,
            image_url=image_url,
            metadata_hash="0" * 64,
            block_number=self._mock_block_number,
            chain_id=1,
        )
        metadata_hash = self.hash_metadata(metadata)
        return TalismanMetadata(
            token_id=token_id,
            created_at=metadata.created_at,
            location_ip=metadata.location_ip,
            location_region=metadata.location_region,
            diagnosis=diagnosis,
            image_url=image_url,
            metadata_hash=metadata_hash,
            block_number=self._mock_block_number,
            chain_id=1,
        )

    def hash_metadata(self, metadata: TalismanMetadata) -> str:
        try:
            hashable_data = {
                "token_id": metadata.token_id,
                "timestamp": metadata.created_at.isoformat(),
                "location": {"ip": metadata.location_ip, "region": metadata.location_region},
                "diagnosis": {
                    "birth_datetime": metadata.diagnosis.fate_profile.birth_datetime.isoformat(),
                    "major_star": metadata.diagnosis.fate_profile.major_star.value,
                    "inherent_element": metadata.diagnosis.fate_profile.inherent_element.value,
                    "environment_element": metadata.diagnosis.environment.dominant_environment_element.value,
                    "cpu_temp": metadata.diagnosis.environment.cpu_temperature,
                    "network_latency": metadata.diagnosis.environment.network_latency_ms,
                    "entropy_hash": metadata.diagnosis.environment.entropy_hash,
                    "remedy_elements": [e.value for e in metadata.diagnosis.remedy_elements],
                },
                "image_url": metadata.image_url,
            }
            json_str = json.dumps(hashable_data, sort_keys=True, separators=(",", ":"))
            hash_bytes = self._web3.keccak(text=json_str)
            return hash_bytes.hex()
        except Exception as e:
            raise HashingError(message=f"Failed to hash metadata: {str(e)}", details={"token_id": metadata.token_id})

    def generate_nft_json(self, metadata: TalismanMetadata) -> dict:
        return {
            "name": f"Qi-Link Talisman #{metadata.token_id[:8]}",
            "description": self._generate_description(metadata),
            "image": metadata.image_url,
            "external_url": f"https://qi-link.io/talisman/{metadata.token_id}",
            "attributes": metadata.opensea_attributes,
            "properties": {
                "metadata_hash": metadata.metadata_hash,
                "block_number": metadata.block_number,
                "chain_id": metadata.chain_id,
                "created_at": metadata.created_at.isoformat(),
                "diagnosis": {"imbalance": metadata.diagnosis.imbalance_description, "remedy": metadata.diagnosis.remedy_description},
            },
        }

    def _generate_token_id(self) -> str:
        timestamp_hex = hex(int(time.time() * 1000))[2:]
        random_hex = secrets.token_hex(16)
        return f"{timestamp_hex}-{random_hex}"

    def _generate_mock_block_number(self) -> int:
        base_block = 19_000_000
        days_elapsed = (time.time() - 1704067200) / 86400
        return base_block + int(days_elapsed * 7200) + secrets.randbelow(100)

    def _get_mock_ip(self) -> str:
        octets = [(hash(str(time.time_ns())) >> i) & 255 for i in range(0, 32, 8)]
        octets[0] = max(1, min(223, octets[0]))
        return ".".join(str(o) for o in octets)

    def _generate_description(self, metadata: TalismanMetadata) -> str:
        fate = metadata.diagnosis.fate_profile
        env = metadata.diagnosis.environment
        return f"""🔮 Qi-Link Cyber Talisman
A unique DePIN-generated corrective energy talisman.
📊 CPU: {env.cpu_temperature}°C | Latency: {env.network_latency_ms}ms | Entropy: {env.entropy_score}/100
⭐ Star: {fate.major_star.value} | Element: {fate.inherent_element.chinese}
⚖️ {metadata.diagnosis.imbalance_description_chinese}
💫 {metadata.diagnosis.remedy_description}
🔗 Hash: {metadata.metadata_hash[:16]}... | Block: {metadata.block_number}"""

