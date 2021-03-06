# Generated by Django 3.1.6 on 2021-03-16 19:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client_requests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(null=True)),
                ('description', models.TextField(null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('open', 'Open'), ('accepted', 'Accepted'), ('assigned', 'Assigned'), ('pending_completion_approval', 'Pending Completion Approval'), ('completed', 'completed')], default='pending', max_length=50)),
                ('project_duration', models.IntegerField(null=True)),
                ('payment_status', models.BooleanField(default=0)),
                ('sme_reference_num', models.CharField(max_length=20)),
                ('admin_confirm_completion', models.BooleanField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('assigned_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='service_provider_request', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_request', to='client_requests.category')),
                ('order_reference', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_reference_request', to='client_requests.order')),
                ('scope', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='scope_request', to='client_requests.scope')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_request', to='client_requests.service')),
                ('sub_service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_service_request', to='client_requests.subservice')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_request', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
