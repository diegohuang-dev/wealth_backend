from datetime import datetime
from typing import Any, Optional
from typing_extensions import Annotated

from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column
from sqlalchemy.types import JSON, String

class Base(MappedAsDataclass, DeclarativeBase):
    MAX_STR_LENGTH = 256   # Assume that all strings are maximum of 256 characters long.
                           # Could make this more fine-grained for different strings if needed.

    type_annotation_map = {
        dict[str, Any]: JSON,
        str: String(MAX_STR_LENGTH),
    }

int_pk = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]

class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int_pk] = mapped_column(init=False)
    assetDescription: Mapped[Optional[str]]
    assetId: Mapped[str]
    assetInfo: Mapped[dict[str, Any]]
    assetInfoType: Mapped[str]
    assetMask: Mapped[Optional[str]]
    assetName: Mapped[Optional[str]]
    assetOwnerName: Mapped[Optional[str]]
    balanceAsOf: Mapped[datetime]
    balanceCostBasis: Mapped[float]
    balanceCostFrom: Mapped[str]
    balanceCurrent: Mapped[float]
    balanceFrom: Mapped[str]
    balancePrice: Mapped[Optional[float]]
    balancePriceFrom: Mapped[str]
    balanceQuantityCurrent: Mapped[Optional[float]]
    beneficiaryComposition: Mapped[Optional[str]]
    cognitoId: Mapped[str]
    creationDate: Mapped[datetime]
    currencyCode: Mapped[Optional[str]]
    deactivateBy: Mapped[Optional[str]]
    descriptionEstatePlan: Mapped[str]
    hasInvestment: Mapped[Optional[bool]]
    holdings: Mapped[Optional[dict[str, Any]]]
    includeInNetWorth: Mapped[bool]
    institutionId: Mapped[int]
    institutionName: Mapped[Optional[str]]
    integration: Mapped[Optional[str]]
    integrationAccountId: Mapped[Optional[str]]
    isActive: Mapped[bool]
    isAsset: Mapped[bool]
    isFavorite: Mapped[bool]
    isLinkedVendor: Mapped[Optional[bool]]
    lastUpdate: Mapped[datetime]
    lastUpdateAttempt: Mapped[datetime]
    logoName: Mapped[Optional[str]]
    modificationDate: Mapped[datetime]
    nextUpdate: Mapped[Optional[datetime]]
    nickname: Mapped[str]
    note: Mapped[Optional[str]]
    noteDate: Mapped[Optional[datetime]]
    ownership: Mapped[Optional[str]]
    primaryAssetCategory: Mapped[str]
    status: Mapped[Optional[str]]
    statusCode: Mapped[Optional[str]]
    userInstitutionId: Mapped[str]
    vendorAccountType: Mapped[Optional[str]]
    vendorContainer: Mapped[Optional[str]]
    vendorResponse: Mapped[Optional[str]]
    vendorResponseType: Mapped[str]
    wealthAssetType: Mapped[str]
    wid: Mapped[str]
