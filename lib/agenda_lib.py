import datetime
import enum
from pydantic import BaseModel
from typing import List
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from fastapi.responses import StreamingResponse


DATEFORMATSTR = "%Y-%m-%d"


class AgendaItemType(enum.Enum):
    personal_updates = "personal-updates"
    accomplishments = "accomplishments"
    blockers = "blockers"
    risks = "risks"


class AgendaInput(BaseModel):
    user: str
    startDate: datetime.datetime
    endDate: datetime.datetime
    agendaItems: List[AgendaItemType]


def create_agenda_pdf(agenda_input: AgendaInput):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    width = 100

    # Add some text
    c.setFont("Helvetica", 12)

    c.drawString(100, height - 100, f"Agenda for: {agenda_input.user}")
    c.drawString(
        width,
        height - 120,
        f"From: {agenda_input.startDate.strftime(DATEFORMATSTR)}-{agenda_input.endDate.strftime(DATEFORMATSTR)}",
    )

    for idx, item in enumerate(agenda_input.agendaItems):
        c.drawString(width, height - 140 - 20 * (idx + 1), f"{item}")

    # Save the PDF file
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer


def download_agenda(agenda_input: AgendaInput) -> StreamingResponse:
    pdf_buffer = create_agenda_pdf(agenda_input)
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=example.pdf"},
    )
