from database.database import (
    Database
)


def test_database(
    tmp_path
):

    db = Database(
        tmp_path / "test.db"
    )

    db.initialize()

    db.upsert_student(
        1,
        "Test Student"
    )

    db.add_subject(
        1,
        "Python"
    )

    db.add_assignment(
        1,
        "Test Assignment",
        "2026-09-20"
    )

    student = (
        db.get_student(1)
    )

    subjects = (
        db.get_subjects(1)
    )

    assignments = (
        db.get_assignments(1)
    )

    assert (
        student["name"]
        == "Test Student"
    )

    assert len(
        subjects
    ) == 1

    assert len(
        assignments
    ) == 1