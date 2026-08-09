from alembic import op
import sqlalchemy as sa


def upgrade():
    userrole = sa.Enum("ADMIN", "USER", name="userrole")
    userrole.create(op.get_bind(), checkfirst=True)

    op.alter_column(
        "users",
        "role",
        existing_type=sa.VARCHAR(length=20),
        type_=userrole,
        existing_nullable=False,
    )


def downgrade():
    op.alter_column(
        "users",
        "role",
        existing_type=sa.Enum("ADMIN", "USER", name="userrole"),
        type_=sa.VARCHAR(length=20),
        existing_nullable=False,
    )

    sa.Enum("ADMIN", "USER", name="userrole").drop(
        op.get_bind(),
        checkfirst=True,
    )