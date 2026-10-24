from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0005_alter_restaurant_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='rating',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]