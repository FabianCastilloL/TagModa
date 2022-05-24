# Generated by Django 4.0 on 2022-05-17 16:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_direccionenvio_pedido_productospedidos_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreGenero', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='producto',
            name='genero',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='app.genero'),
            preserve_default=False,
        ),
    ]