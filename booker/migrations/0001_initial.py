

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bookable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starttime', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='OfficeHour',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),

                ('location', models.CharField(default='contact staff', max_length=20)),
                ('event_id', models.CharField(default='no event', max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=50)),

            ],
        ),
        migrations.AddField(
            model_name='bookable',
            name='officehour',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booker.OfficeHour'),
        ),
    ]
