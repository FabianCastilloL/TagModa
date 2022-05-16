# Generated by Django 4.0 on 2022-05-15 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Contacto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=254)),
                ('tipo_consulta', models.IntegerField(choices=[[0, 'Consulta'], [1, 'Reclamo'], [2, 'Sugerencias'], [3, 'Cambio Producto']])),
                ('mensaje', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombreMarca', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(null=True, upload_to='productos')),
                ('nombreProducto', models.CharField(max_length=80, null=True)),
                ('precio', models.IntegerField()),
                ('descripcion', models.TextField()),
                ('talla', models.CharField(max_length=5)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.category')),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.marca')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('producto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='app.producto')),
            ],
        ),
    ]
