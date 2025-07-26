"""Add data warehouse tables

Revision ID: ce0d132947cf
Revises: 8efef424c52e
Create Date: 2025-07-26 10:41:28.902267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ce0d132947cf'
down_revision: Union[str, Sequence[str], None] = '8efef424c52e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Create dimension tables
    op.create_table(
        'dim_date',
        sa.Column('date_key', sa.Integer(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('year', sa.Integer(), nullable=False),
        sa.Column('quarter', sa.Integer(), nullable=False),
        sa.Column('month', sa.Integer(), nullable=False),
        sa.Column('month_name', sa.String(), nullable=False),
        sa.Column('day', sa.Integer(), nullable=False),
        sa.Column('day_of_week', sa.Integer(), nullable=False),
        sa.Column('day_name', sa.String(), nullable=False),
        sa.Column('is_weekend', sa.Boolean(), nullable=False),
        sa.Column('is_holiday', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('date_key')
    )
    
    op.create_table(
        'dim_users',
        sa.Column('user_key', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=False),
        sa.Column('is_current', sa.Boolean(), nullable=False),
        sa.Column('valid_from', sa.DateTime(), nullable=False),
        sa.Column('valid_to', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('user_key')
    )

    op.create_table(
        'dim_projects',
        sa.Column('project_key', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('is_current', sa.Boolean(), nullable=False),
        sa.Column('valid_from', sa.DateTime(), nullable=False),
        sa.Column('valid_to', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('project_key')
    )

    op.create_table(
        'dim_products',
        sa.Column('product_key', sa.Integer(), nullable=False),
        sa.Column('product_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('category', sa.String(), nullable=False),
        sa.Column('vendor', sa.String(), nullable=False),
        sa.Column('is_current', sa.Boolean(), nullable=False),
        sa.Column('valid_from', sa.DateTime(), nullable=False),
        sa.Column('valid_to', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('product_key')
    )

    # Create fact tables
    op.create_table(
        'fact_project_metrics',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date_key', sa.Integer(), nullable=False),
        sa.Column('project_key', sa.Integer(), nullable=False),
        sa.Column('user_key', sa.Integer(), nullable=False),
        sa.Column('total_products', sa.Integer(), nullable=False),
        sa.Column('total_value', sa.Numeric(10, 2), nullable=False),
        sa.Column('completion_percentage', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['date_key'], ['dim_date.date_key']),
        sa.ForeignKeyConstraint(['project_key'], ['dim_projects.project_key']),
        sa.ForeignKeyConstraint(['user_key'], ['dim_users.user_key']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'fact_product_usage',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date_key', sa.Integer(), nullable=False),
        sa.Column('product_key', sa.Integer(), nullable=False),
        sa.Column('project_key', sa.Integer(), nullable=False),
        sa.Column('quantity_used', sa.Integer(), nullable=False),
        sa.Column('total_cost', sa.Numeric(10, 2), nullable=False),
        sa.Column('efficiency_score', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['date_key'], ['dim_date.date_key']),
        sa.ForeignKeyConstraint(['product_key'], ['dim_products.product_key']),
        sa.ForeignKeyConstraint(['project_key'], ['dim_projects.project_key']),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table(
        'fact_project_daily',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('date_key', sa.Integer(), nullable=False),
        sa.Column('project_key', sa.Integer(), nullable=False),
        sa.Column('total_value', sa.Numeric(10, 2), nullable=False),
        sa.Column('tasks_completed', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['date_key'], ['dim_date.date_key']),
        sa.ForeignKeyConstraint(['project_key'], ['dim_projects.project_key']),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop fact tables first (due to foreign key constraints)
    op.drop_table('fact_project_daily')
    op.drop_table('fact_product_usage')
    op.drop_table('fact_project_metrics')
    
    # Drop dimension tables
    op.drop_table('dim_products')
    op.drop_table('dim_projects')
    op.drop_table('dim_users')
    op.drop_table('dim_date')
