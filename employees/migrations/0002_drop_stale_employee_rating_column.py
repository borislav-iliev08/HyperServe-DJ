from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE employees_employee DROP COLUMN IF EXISTS rating',
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]