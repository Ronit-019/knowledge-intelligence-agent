from pathlib import Path

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "data" / "knowledge_base"


styles = getSampleStyleSheet()

TITLE = ParagraphStyle(
    "DocumentTitle",
    parent=styles["Title"],
    alignment=TA_CENTER,
    spaceAfter=20,
)

HEADING = ParagraphStyle(
    "SectionHeading",
    parent=styles["Heading2"],
    spaceBefore=14,
    spaceAfter=8,
)

BODY = ParagraphStyle(
    "Body",
    parent=styles["BodyText"],
    leading=15,
    spaceAfter=8,
)

META = ParagraphStyle(
    "Metadata",
    parent=styles["BodyText"],
    leading=13,
    spaceAfter=4,
)


DOCUMENTS = [
    {
        "path": "hr/remote_work_policy_v1.pdf",
        "document_id": "HR-RW-001",
        "title": "Remote Work Policy",
        "department": "HR",
        "document_type": "policy",
        "version": "1.0",
        "effective_date": "2025-01-01",
        "status": "superseded",
        "source": "internal-policy-demo",
        "sections": [
            (
                "Purpose",
                "This policy defines the conditions under which employees may work remotely.",
            ),
            (
                "Remote Work Eligibility",
                "Employees who have completed their probation period may request remote work subject to manager approval. Remote work is normally permitted from the employee's registered country of employment.",
            ),
            (
                "International Remote Work",
                "Employees may not work remotely from another country without prior approval from Human Resources. International remote work requests must be reviewed individually.",
            ),
            (
                "Duration",
                "International remote work was limited to a maximum of 30 consecutive calendar days under this version of the policy.",
            ),
            (
                "Manager Approval",
                "Manager approval is required before remote work arrangements begin.",
            ),
            (
                "Effective Date",
                "This version became effective on January 1, 2025.",
            ),
        ],
    },
    {
        "path": "hr/remote_work_policy_v2.pdf",
        "document_id": "HR-RW-001",
        "title": "Remote Work Policy",
        "department": "HR",
        "document_type": "policy",
        "version": "2.0",
        "effective_date": "2026-01-01",
        "status": "active",
        "source": "internal-policy-demo",
        "supersedes": "HR-RW-001:v1.0",
        "sections": [
            (
                "Purpose",
                "This policy defines the current requirements for remote and hybrid work arrangements.",
            ),
            (
                "Remote Work Eligibility",
                "Employees who have completed their probation period may request remote work subject to manager approval. Remote work is normally permitted from the employee's registered country of employment.",
            ),
            (
                "International Remote Work",
                "International remote work requires prior approval from Human Resources and the employee's manager. The request must identify the destination country, expected duration, and business justification.",
            ),
            (
                "Duration",
                "International remote work may be approved for up to 90 consecutive calendar days. Requests exceeding 90 days require review by HR and the Compliance team.",
            ),
            (
                "Manager Approval",
                "Manager approval and HR approval are required before international remote work begins.",
            ),
            (
                "Effective Date",
                "This version became effective on January 1, 2026. This policy supersedes version 1.0 of the Remote Work Policy.",
            ),
        ],
    },
    {
        "path": "hr/international_work_policy.pdf",
        "document_id": "HR-IW-002",
        "title": "International Work and Relocation Policy",
        "department": "HR",
        "document_type": "policy",
        "version": "1.0",
        "effective_date": "2026-02-01",
        "status": "active",
        "source": "internal-policy-demo",
        "sections": [
            (
                "Purpose",
                "This policy defines additional requirements for employees who intend to work internationally or relocate temporarily.",
            ),
            (
                "Temporary International Work",
                "Employees requesting international work must obtain approval before beginning work from the destination country. The request must include the destination country, dates, reason for travel, and confirmation from the employee's manager.",
            ),
            (
                "Extended International Work",
                "International work lasting more than 90 consecutive calendar days is considered extended international work. Extended international work requires review by Human Resources and Compliance.",
            ),
            (
                "Permanent Relocation",
                "Permanent relocation is not automatically authorized through the remote work process. Employees seeking permanent relocation must use the company's relocation process and receive separate approval.",
            ),
            (
                "Tax and Legal Review",
                "Approval for international work does not by itself confirm that all tax, immigration, employment, or regulatory requirements have been satisfied. Employees must complete any required compliance review before beginning international work.",
            ),
            (
                "Effective Date",
                "This policy became effective on February 1, 2026.",
            ),
        ],
    },
    {
        "path": "finance/employee_expense_policy.pdf",
        "document_id": "FIN-EXP-003",
        "title": "Employee Expense and Reimbursement Policy",
        "department": "Finance",
        "document_type": "policy",
        "version": "1.0",
        "effective_date": "2026-01-01",
        "status": "active",
        "source": "internal-policy-demo",
        "sections": [
            (
                "Purpose",
                "This policy defines eligible employee business expenses and reimbursement requirements.",
            ),
            (
                "Business Travel",
                "Reasonable transportation, accommodation, and business-related travel expenses may be reimbursed when the travel has been approved in advance.",
            ),
            (
                "Receipts",
                "Employees must provide receipts for individual expenses of 25 USD or more. Expenses below 25 USD may be reimbursed without a receipt when the expense is clearly described.",
            ),
            (
                "Submission Deadline",
                "Expense reports should be submitted within 30 calendar days after the expense is incurred.",
            ),
            (
                "International Expenses",
                "International expenses must include the local currency amount and the converted reporting currency amount. The exchange rate used for conversion must be recorded with the expense report.",
            ),
            (
                "Approval",
                "Expenses must be approved by the employee's designated manager before reimbursement is processed.",
            ),
        ],
    },
    {
        "path": "security/access_security_policy.pdf",
        "document_id": "SEC-ACC-004",
        "title": "Access and Authentication Security Standard",
        "department": "Security",
        "document_type": "standard",
        "version": "2.0",
        "effective_date": "2026-01-15",
        "status": "active",
        "source": "internal-policy-demo",
        "sections": [
            (
                "Authentication",
                "Employees must use multi-factor authentication for systems classified as business-critical. Passwords must not be shared with other employees.",
            ),
            (
                "Access Requests",
                "Access to business systems must follow the principle of least privilege. Employees should receive only the permissions required for their role.",
            ),
            (
                "Access Reviews",
                "Privileged access must be reviewed at least quarterly. Managers are responsible for confirming that access remains appropriate.",
            ),
            (
                "Security Incidents",
                "Suspected credential compromise must be reported to the Security team immediately. Employees must not attempt to conceal or independently investigate suspected credential theft.",
            ),
            (
                "Remote Access",
                "Employees working remotely must use company-approved authentication and access mechanisms. Public or untrusted networks must not be used to bypass company security controls.",
            ),
        ],
    },
    {
        "path": "compliance/data_handling_policy.pdf",
        "document_id": "CMP-DH-005",
        "title": "Data Handling and Retention Policy",
        "department": "Compliance",
        "document_type": "policy",
        "version": "1.0",
        "effective_date": "2026-01-01",
        "status": "active",
        "source": "internal-policy-demo",
        "sections": [
            (
                "Purpose",
                "This policy defines requirements for handling, storing, and retaining company information.",
            ),
            (
                "Sensitive Information",
                "Sensitive information must only be stored in company-approved systems. Employees must not copy sensitive company information to personal storage services.",
            ),
            (
                "Data Sharing",
                "Sensitive information may only be shared with authorized recipients who require the information for legitimate business purposes.",
            ),
            (
                "Retention",
                "Business records must be retained according to the applicable record-retention schedule. Employees must not delete records subject to a legal hold.",
            ),
            (
                "External Sharing",
                "External sharing of sensitive information requires authorization from the appropriate data owner.",
            ),
            (
                "Security Incidents",
                "Suspected unauthorized disclosure of sensitive information must be reported to the Security or Compliance team immediately.",
            ),
        ],
    },
]


def add_page_number(canvas, document):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        A4[0] - 0.6 * inch,
        0.4 * inch,
        f"Page {document.page}",
    )
    canvas.restoreState()


def build_document(doc):
    output_path = OUTPUT_DIR / doc["path"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    pdf = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
        title=doc["title"],
        author="Knowledge Intelligence Agent",
    )

    story = []

    story.append(Paragraph(doc["title"], TITLE))

    metadata = [
        f"<b>Document ID:</b> {doc['document_id']}",
        f"<b>Department:</b> {doc['department']}",
        f"<b>Document Type:</b> {doc['document_type']}",
        f"<b>Version:</b> {doc['version']}",
        f"<b>Effective Date:</b> {doc['effective_date']}",
        f"<b>Status:</b> {doc['status']}",
        f"<b>Source:</b> {doc['source']}",
    ]

    if "supersedes" in doc:
        metadata.append(
            f"<b>Supersedes:</b> {doc['supersedes']}"
        )

    for item in metadata:
        story.append(Paragraph(item, META))

    story.append(Spacer(1, 18))

    for heading, body in doc["sections"]:
        story.append(Paragraph(heading, HEADING))
        story.append(Paragraph(body, BODY))

    pdf.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    print(f"Created: {output_path}")


def main():
    for document in DOCUMENTS:
        build_document(document)

    print(f"\nGenerated {len(DOCUMENTS)} PDF documents.")


if __name__ == "__main__":
    main()