from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE employees_employeereview RENAME TO reviews_employeereview',
            reverse_sql='ALTER TABLE reviews_employeereview RENAME TO employees_employeereview',
        ),
    ]