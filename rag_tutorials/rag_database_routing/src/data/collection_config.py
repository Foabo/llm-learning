"""Database collection configurations."""

from typing import Dict, Literal
from dataclasses import dataclass

DatabaseType = Literal["products", "support", "finance"]


@dataclass
class CollectionConfig:
    """Configuration for a Qdrant collection."""
    name: str
    description: str
    collection_name: str


# Collection configurations mapping
COLLECTIONS: Dict[DatabaseType, CollectionConfig] = {
    "products": CollectionConfig(
        name="产品信息",
        description="产品详情、规格和功能信息",
        collection_name="products_collection"
    ),
    "support": CollectionConfig(
        name="客户支持与FAQ",
        description="客户支持信息、常见问题和指南",
        collection_name="support_collection"
    ),
    "finance": CollectionConfig(
        name="财务信息",
        description="财务数据、收入、成本和负债信息",
        collection_name="finance_collection"
    )
} 