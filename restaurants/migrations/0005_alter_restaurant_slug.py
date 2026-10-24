from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurants', '0004_restaurant_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='slug',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]