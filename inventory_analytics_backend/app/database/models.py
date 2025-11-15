from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class ProductMaster(Base):
    __tablename__ = "product_master"
    
    sku_id = Column(String, primary_key=True, index=True)
    product_name = Column(String, nullable=False)
    category = Column(String, nullable=False, index=True)
    sub_category = Column(String, nullable=False)
    brand = Column(String, nullable=False)
    unit_cost_price = Column(Float, nullable=False)
    unit_selling_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    sales_transactions = relationship("SalesTransaction", back_populates="product")
    stock_receipts = relationship("StockReceipt", back_populates="product")

class SalesTransaction(Base):
    __tablename__ = "sales_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    transaction_date = Column(DateTime, default=datetime.utcnow, index=True)
    sku_id = Column(String, ForeignKey("product_master.sku_id"), nullable=False)
    quantity_sold = Column(Integer, nullable=False)
    sale_price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("ProductMaster", back_populates="sales_transactions")

class StockReceipt(Base):
    __tablename__ = "stock_receipts"
    
    id = Column(Integer, primary_key=True, index=True)
    receipt_date = Column(DateTime, default=datetime.utcnow, index=True)
    sku_id = Column(String, ForeignKey("product_master.sku_id"), nullable=False)
    quantity_received = Column(Integer, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.supplier_id"), nullable=False)
    unit_cost = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("ProductMaster", back_populates="stock_receipts")
    supplier = relationship("Supplier", back_populates="stock_receipts")

class Supplier(Base):
    __tablename__ = "suppliers"
    
    supplier_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    supplier_name = Column(String, nullable=False, unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    stock_receipts = relationship("StockReceipt", back_populates="supplier")
