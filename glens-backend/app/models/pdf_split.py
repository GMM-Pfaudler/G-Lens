from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from datetime import datetime, timezone
from sqlalchemy.ext.declarative import declarative_base
import enum
import json
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

Base = declarative_base()

class SplitStatusEnum(str, enum.Enum):
    success = "success"
    failure = "failure"

class PDFSplitResult(Base):
    __tablename__ = "pdf_splits"

    id = Column(Integer, primary_key=True, index=True)

    # User who uploaded the file
    user_id = Column(String(255), nullable=False)

    # Name of the uploaded PDF file
    file_name = Column(String(255), nullable=False)

    # Store multiple output file paths as JSON string
    results_path = Column(Text, nullable=True)  

    # success / failure
    status = Column(Enum(SplitStatusEnum), nullable=False, default=SplitStatusEnum.success)

    # In case failure happens
    error_message = Column(Text, nullable=True)

    # When the PDF was uploaded
    uploaded_on = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    # Helper to store Python list into JSON string
    def set_results(self, paths: list):
        self.results_path = json.dumps(paths)

    # Helper to retrieve JSON list
    def get_results(self):
        try:
            return json.loads(self.results_path) if self.results_path else []
        except:
            return []

# -------------------------
# Async upsert function
# -------------------------
async def upsert_pdf_split_result(
    db: AsyncSession,
    user_id: str,
    file_name: str,
    results: list | None = None,
    status: SplitStatusEnum = SplitStatusEnum.success,
    error_message: str | None = None
) -> PDFSplitResult:
    # Check if record exists
    stmt = select(PDFSplitResult).where(
        PDFSplitResult.user_id == user_id,
        PDFSplitResult.file_name == file_name
    )
    res = await db.execute(stmt)
    pdf_split = res.scalars().first()

    if pdf_split:
        # Update existing record
        pdf_split.status = status
        pdf_split.error_message = error_message
        if results is not None:
            pdf_split.set_results(results)
    else:
        # Create new record
        pdf_split = PDFSplitResult(
            user_id=user_id,
            file_name=file_name,
            status=status,
            error_message=error_message
        )
        if results:
            pdf_split.set_results(results)
        db.add(pdf_split)

    await db.commit()
    await db.refresh(pdf_split)
    return pdf_split
