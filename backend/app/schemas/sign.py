"""Schemas cho Pydantic liên quan đến tra cứu biển báo."""

from __future__ import annotations

from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

WarningLevel = Literal["low", "medium", "high", "info"]


class SignBase(BaseModel):
    class_id: int = Field(..., ge=0, description="ID lớp tương ứng trong model ML")
    sign_code: str = Field(..., min_length=1, description="Mã biển báo theo QC 41:2019/BGTVT")
    name: str = Field(..., min_length=1, description="Tên biển báo chính thức")
    group_name: str = Field(..., min_length=1, description="Nhóm biển báo")
    meaning: str = Field(..., min_length=1, description="Ý nghĩa quy chuẩn")
    recommended_action: str = Field(..., min_length=1, description="Khuyến nghị hành vi tuân thủ")
    warning_level: WarningLevel = Field("info", description="Mức độ cảnh báo")
    image_url: str | None = Field(None, description="URL hoặc đường dẫn ảnh minh họa")
    legal_source: str = Field(..., min_length=1, description="Văn bản quy chuẩn viện dẫn")
    source_checked_at: date = Field(..., description="Ngày đối chiếu văn bản pháp luật")


class SignCreate(SignBase):
    pass


class SignResponse(SignBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    updated_at: datetime


class SignDetail(SignResponse):
    pass


class SignSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = None
    sign_code: str
    name: str
    group: str
    meaning: str
    recommended_action: str
    warning_level: WarningLevel
    source: str
    source_checked_at: date | None = None
    image_url: str | None = None


class SignGroupSummary(BaseModel):
    group_name: str
    count: int


class SignListResponse(BaseModel):
    items: list[SignResponse]
    total: int
    page: int
    page_size: int
    total_pages: int
