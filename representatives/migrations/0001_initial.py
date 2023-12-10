from django.db import models, migrations

class JSONField(models.TextField):
    """Mocks jsonfield 0.92's column-type behaviour"""
    def db_type(self, connection):
        if connection.vendor == 'postgresql' and connection.pg_version >= 90300:
            return 'json'
        else:
            return super().db_type(connection)

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('district_name', models.CharField(max_length=300)),
                ('elected_office', models.CharField(max_length=200)),
                ('source_url', models.URLField(max_length=2048)),
                ('boundary', models.CharField(db_index=True, help_text='e.g. federal-electoral-districts/outremont', blank=True, max_length=300)),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('party_name', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=75)),
                ('url', models.URLField(blank=True, max_length=2048)),
                ('personal_url', models.URLField(blank=True, max_length=2048)),
                ('photo_url', models.URLField(blank=True, max_length=2048)),
                ('district_id', models.CharField(blank=True, max_length=200)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], blank=True, max_length=1)),
                ('offices', JSONField(default=dict, blank=True)),
                ('extra', JSONField(default=dict, blank=True)),
                ('incumbent', models.NullBooleanField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Election',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The name of the political body, e.g. BC Legislature', unique=True, max_length=300)),
                ('data_url', models.URLField(help_text='URL to a JSON array of representatives within this set')),
                ('data_about_url', models.URLField(help_text='URL to information about the scraper used to gather data', blank=True)),
                ('last_import_time', models.DateTimeField(null=True, blank=True)),
                ('last_import_successful', models.NullBooleanField()),
                ('boundary_set', models.CharField(help_text='Name of the boundary set on the boundaries API, e.g. federal-electoral-districts', blank=True, max_length=300)),
                ('slug', models.SlugField(unique=True, max_length=300)),
                ('enabled', models.BooleanField(default=True, db_index=True)),
                ('election_date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Representative',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
                ('district_name', models.CharField(max_length=300)),
                ('elected_office', models.CharField(max_length=200)),
                ('source_url', models.URLField(max_length=2048)),
                ('boundary', models.CharField(db_index=True, help_text='e.g. federal-electoral-districts/outremont', blank=True, max_length=300)),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('party_name', models.CharField(blank=True, max_length=200)),
                ('email', models.EmailField(blank=True, max_length=75)),
                ('url', models.URLField(blank=True, max_length=2048)),
                ('personal_url', models.URLField(blank=True, max_length=2048)),
                ('photo_url', models.URLField(blank=True, max_length=2048)),
                ('district_id', models.CharField(blank=True, max_length=200)),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], blank=True, max_length=1)),
                ('offices', JSONField(default=dict, blank=True)),
                ('extra', JSONField(default=dict, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepresentativeSet',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(help_text='The name of the political body, e.g. BC Legislature', unique=True, max_length=300)),
                ('data_url', models.URLField(help_text='URL to a JSON array of representatives within this set')),
                ('data_about_url', models.URLField(help_text='URL to information about the scraper used to gather data', blank=True)),
                ('last_import_time', models.DateTimeField(null=True, blank=True)),
                ('last_import_successful', models.NullBooleanField()),
                ('boundary_set', models.CharField(help_text='Name of the boundary set on the boundaries API, e.g. federal-electoral-districts', blank=True, max_length=300)),
                ('slug', models.SlugField(unique=True, max_length=300)),
                ('enabled', models.BooleanField(default=True, db_index=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='representative',
            name='representative_set',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='individuals', to='representatives.RepresentativeSet'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='candidate',
            name='election',
            field=models.ForeignKey(on_delete=models.CASCADE, related_name='individuals', to='representatives.Election'),
            preserve_default=True,
        ),
    ]
