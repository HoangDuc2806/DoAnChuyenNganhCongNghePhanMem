from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_chathistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50, verbose_name='Màu sắc')),
                ('color_hex', models.CharField(default='#000000', help_text='Ví dụ: #FF0000', max_length=7, verbose_name='Mã màu hex')),
                ('size', models.CharField(max_length=10, verbose_name='Size')),
                ('stock', models.IntegerField(default=0, verbose_name='Số lượng tồn')),
                ('product', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='variants',
                    to='app.product',
                )),
            ],
            options={
                'verbose_name': 'Biến thể sản phẩm',
                'verbose_name_plural': 'Biến thể sản phẩm',
                'ordering': ['color', 'size'],
            },
        ),
    ]
