"""
Task 1: Structured LLM Prompt Pipeline & JSON Extractor
Pydantic v2 Invoice Schemas with line-item validation and financial arithmetic checks.
"""

from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class VendorInfo(BaseModel):
    name: str = Field(..., description="Full legal name or business trading name of the vendor")
    tax_id: Optional[str] = Field(None, description="VAT/GST/EIN tax identification number")
    email: Optional[str] = Field(None, description="Contact billing email address")
    phone: Optional[str] = Field(None, description="Contact phone number")
    address: Optional[str] = Field(None, description="Physical or billing address")


class ClientInfo(BaseModel):
    name: str = Field(..., description="Name of the customer or recipient business")
    email: Optional[str] = Field(None, description="Customer contact email")
    phone: Optional[str] = Field(None, description="Customer phone number")
    address: Optional[str] = Field(None, description="Billing or delivery address")


class InvoiceLineItem(BaseModel):
    description: str = Field(..., description="Description of the goods or services provided")
    quantity: float = Field(..., gt=0, description="Quantity of items billed (must be positive)")
    unit_price: float = Field(..., ge=0, description="Price per individual unit")
    total_price: float = Field(..., ge=0, description="Line item calculated total")

    @model_validator(mode="after")
    def compute_or_validate_total(self) -> InvoiceLineItem:
        expected = round(self.quantity * self.unit_price, 2)
        if abs(self.total_price - expected) > 0.05:
            self.total_price = expected
        return self


class InvoiceSchema(BaseModel):
    invoice_id: str = Field(..., description="Unique alphanumeric identifier for the invoice")
    invoice_date: str = Field(..., description="Date of issue in YYYY-MM-DD or standard readable format")
    due_date: Optional[str] = Field(None, description="Payment due date")
    currency: str = Field(default="USD", description="ISO 4217 currency code (e.g. USD, EUR, INR)")
    vendor: VendorInfo
    client: ClientInfo
    line_items: List[InvoiceLineItem] = Field(..., min_length=1, description="List of invoiced line items")
    subtotal: float = Field(..., ge=0, description="Sum of line item totals before tax and discounts")
    tax_amount: float = Field(default=0.0, ge=0, description="Taxes applied (sales tax, VAT, GST)")
    discount_amount: float = Field(default=0.0, ge=0, description="Discounts or coupons deducted")
    total_amount: float = Field(..., ge=0, description="Grand total payable")
    payment_terms: Optional[str] = Field("Net 30", description="Terms of payment e.g. Due upon receipt, Net 30")

    @field_validator("currency")
    @classmethod
    def normalize_currency(cls, v: str) -> str:
        code = v.strip().upper()
        if code in ["$", "US$", "DOLLARS"]:
            return "USD"
        if code in ["€", "EUROS"]:
            return "EUR"
        if code in ["₹", "INR", "RUPEES"]:
            return "INR"
        if code in ["£", "GBP"]:
            return "GBP"
        return code

    @model_validator(mode="after")
    def validate_totals_consistency(self) -> InvoiceSchema:
        calculated_subtotal = round(sum(item.total_price for item in self.line_items), 2)
        if abs(self.subtotal - calculated_subtotal) > 0.10:
            self.subtotal = calculated_subtotal
        
        expected_total = round(self.subtotal + self.tax_amount - self.discount_amount, 2)
        if abs(self.total_amount - expected_total) > 0.10:
            self.total_amount = expected_total
        return self
