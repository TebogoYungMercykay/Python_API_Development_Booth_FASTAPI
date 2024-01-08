"""creating_and_updating_tables

Revision ID: 3f36a7f04611
Revises: 
Create Date: 2024-01-08 16:45:01.308437

"""
from alembic import op
import sqlalchemy as sa


# Migration for Creating and Updating Database Tables.


revision = '3f36a7f04611'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('doctors',
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surname', sa.String(length=50), nullable=False),
    sa.Column('dob', sa.DateTime(), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('mobile_no', sa.String(length=15), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('qualification', sa.String(length=20), nullable=False),
    sa.Column('registration_no', sa.String(length=20), nullable=False),
    sa.Column('year_of_registration', sa.DateTime(), nullable=False),
    sa.Column('state_medical_council', sa.String(length=30), nullable=False),
    sa.Column('specialization', sa.String(length=30), nullable=False),
    sa.Column('rating', sa.Integer(), server_default='0', nullable=True),
    sa.Column('is_patient', sa.Boolean(), server_default='FALSE', nullable=True),
    sa.Column('is_doctor', sa.Boolean(), server_default='TRUE', nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('doctor_id')
    )
    op.create_table('feedbacks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('feedback', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('patients',
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('surname', sa.String(length=50), nullable=False),
    sa.Column('dob', sa.DateTime(), nullable=False),
    sa.Column('address', sa.String(length=100), nullable=False),
    sa.Column('mobile_no', sa.String(length=15), nullable=True),
    sa.Column('gender', sa.String(length=10), nullable=False),
    sa.Column('is_patient', sa.Boolean(), server_default='TRUE', nullable=True),
    sa.Column('is_doctor', sa.Boolean(), server_default='FALSE', nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('patient_id')
    )
    op.create_table('diseaseinfos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('diseasename', sa.String(length=200), nullable=False),
    sa.Column('no_of_symp', sa.Integer(), nullable=False),
    sa.Column('symptoms', sa.ARRAY(sa.String()), nullable=False),
    sa.Column('confidence', sa.Float(), nullable=False),
    sa.Column('consultdoctor', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.patient_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ratingreviews',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), server_default='0', nullable=True),
    sa.Column('review', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.doctor_id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.patient_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('replies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['doctors.doctor_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('consultations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.Column('diseaseinfo_id', sa.Integer(), nullable=True),
    sa.Column('consultation_date', sa.DateTime(), nullable=False),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['diseaseinfo_id'], ['diseaseinfos.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['doctor_id'], ['doctors.doctor_id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.patient_id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('chats',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('created', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('consultation_id', sa.Integer(), nullable=True),
    sa.Column('sender_id', sa.Integer(), nullable=True),
    sa.Column('message', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['consultation_id'], ['consultations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('users', sa.Column('is_active', sa.Boolean(), server_default='FALSE', nullable=False))
    op.add_column('users', sa.Column('is_superuser', sa.Boolean(), server_default='FALSE', nullable=False))
    op.add_column('users', sa.Column('is_staff', sa.Boolean(), server_default='FALSE', nullable=False))
    op.add_column('users', sa.Column('last_login', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True))


def downgrade():
    op.drop_column('users', 'last_login')
    op.drop_column('users', 'is_staff')
    op.drop_column('users', 'is_superuser')
    op.drop_column('users', 'is_active')
    op.drop_table('chats')
    op.drop_table('consultations')
    op.drop_table('replies')
    op.drop_table('ratingreviews')
    op.drop_table('diseaseinfos')
    op.drop_table('patients')
    op.drop_table('feedbacks')
    op.drop_table('doctors')

