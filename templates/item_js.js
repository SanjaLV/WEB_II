
{% if item %}

    {
        let z = {};
        z.name = "{{ item.name }}";
        z.str = {{ item.stats.0 }};
        z.dex = {{ item.stats.1 }};
        z.vit = {{ item.stats.2 }};
        z.dmg = {{ item.stats.3 }};
        z.arm = {{ item.stats.4 }};
        z.dod = {{ item.stats.5 }};
        z.crh = {{ item.stats.6 }};
        z.rarity = {{ item.rarity }};
        z.ilvl = {{ item.ilvl }};

        Items[{{item.pk}}] = z;

    }

{% endif %}