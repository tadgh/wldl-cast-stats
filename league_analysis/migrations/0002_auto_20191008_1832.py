# Generated by Django 2.2.6 on 2019-10-09 01:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('league_analysis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerrollingstatistics',
            name='average_assists',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='playerrollingstatistics',
            name='average_deaths',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='playerrollingstatistics',
            name='average_kda',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='playerrollingstatistics',
            name='average_kills',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='playerrollingstatistics',
            name='creep_stats_average',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='playerrollingstatistics',
            name='gpm_average',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='playerrollingstatistics',
            name='most_common_role',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='playerrollingstatistics',
            name='xpm_average',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='average_assists',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='average_creep_stats',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='average_deaths',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='average_gpm',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='average_kda',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='average_kills',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='average_xpm',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='matches_played',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='matches_won',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='series_played',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='teamrollingstatistics',
            name='series_won',
            field=models.IntegerField(default=0),
        ),
    ]
