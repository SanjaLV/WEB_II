# Generated by Django 2.0.6 on 2018-06-17 12:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Affix',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('affix_tupe', models.IntegerField(null=True)),
                ('affix_value', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='AuctionLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(null=True)),
                ('bought', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('price', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gold', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=30, null=True)),
                ('item_level', models.IntegerField(default=0)),
                ('item_tupe', models.IntegerField(null=True)),
                ('item_rarity', models.IntegerField(null=True)),
                ('character_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Character')),
            ],
        ),
        migrations.CreateModel(
            name='Loot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_out', models.IntegerField(default=0)),
                ('next_bid', models.IntegerField(default=0)),
                ('biddable', models.BooleanField(default=False)),
                ('end_time', models.DateTimeField(null=True)),
                ('character_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.Character')),
                ('item_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Item')),
            ],
        ),
        migrations.AddField(
            model_name='character',
            name='eq_armor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='armor', to='main.Item'),
        ),
        migrations.AddField(
            model_name='character',
            name='eq_helm',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='helm', to='main.Item'),
        ),
        migrations.AddField(
            model_name='character',
            name='eq_offhand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='offhand', to='main.Item'),
        ),
        migrations.AddField(
            model_name='character',
            name='eq_weapon',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='weapon', to='main.Item'),
        ),
        migrations.AddField(
            model_name='character',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bid',
            name='character_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Character'),
        ),
        migrations.AddField(
            model_name='bid',
            name='loot_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Loot'),
        ),
        migrations.AddField(
            model_name='auctionlog',
            name='character_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Character'),
        ),
        migrations.AddField(
            model_name='affix',
            name='item_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Item'),
        ),
    ]
