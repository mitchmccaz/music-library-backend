from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='likes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]