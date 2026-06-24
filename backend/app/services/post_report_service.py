from sqlmodel import Session, func, select

from app.models.post_report import PostReport
from app.models.post_report import utc_now
from app.schemas.post_report import PostReportCreate


class DuplicatePendingReportError(Exception):
    pass


def _report_with_context(report: PostReport) -> PostReport:
    object.__setattr__(report, "post_title", report.post.title if report.post else None)
    object.__setattr__(
        report,
        "reporter_username",
        report.reporter.username if report.reporter else None,
    )
    return report


def create_post_report(
    session: Session,
    payload: PostReportCreate,
    post_id: int,
    reporter_id: int,
) -> PostReport:
    existing_statement = select(PostReport).where(
        PostReport.post_id == post_id,
        PostReport.reporter_id == reporter_id,
        PostReport.status == "pending",
    )
    if session.exec(existing_statement).first() is not None:
        raise DuplicatePendingReportError

    report = PostReport(
        post_id=post_id,
        reporter_id=reporter_id,
        reason=payload.reason.strip(),
        description=payload.description.strip(),
    )
    session.add(report)
    session.commit()
    session.refresh(report)
    return _report_with_context(report)


def get_report_by_id(session: Session, report_id: int) -> PostReport | None:
    report = session.get(PostReport, report_id)
    return _report_with_context(report) if report else None


def list_reports(
    session: Session,
    page: int,
    size: int,
    status: str | None = None,
) -> tuple[list[PostReport], int]:
    filters = []
    if status:
        filters.append(PostReport.status == status)

    total_statement = select(func.count()).select_from(PostReport).where(*filters)
    total = session.exec(total_statement).one()

    offset = (page - 1) * size
    statement = (
        select(PostReport)
        .where(*filters)
        .order_by(PostReport.created_at.desc())
        .offset(offset)
        .limit(size)
    )
    reports = [_report_with_context(report) for report in session.exec(statement).all()]
    return reports, total


def update_report_status(
    session: Session,
    report: PostReport,
    status: str,
) -> PostReport:
    report.status = status
    report.updated_at = utc_now()
    session.add(report)
    session.commit()
    session.refresh(report)
    return _report_with_context(report)
