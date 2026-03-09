# -*- coding: utf-8 -*-
"""
Seed script: creates test Species, SpeciesRecords, and a CMS factsheet page.
Run inside Docker: python manage.py shell < seed_test_data.py
"""
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import settings
from django.core.management import setup_environ
setup_environ(settings)

from django.contrib.auth.models import User
from cms.api import create_page
from cms.models import Page
from species.models import Species, SpeciesRecord, State, County, Collection, Collector, Author

# Ensure admin user exists
admin, _ = User.objects.get_or_create(
    username='admin',
    defaults={'is_superuser': True, 'is_staff': True, 'email': 'admin@example.com'}
)
if not admin.has_usable_password():
    admin.set_password('admin')
    admin.save()

# Create authors
author1, _ = Author.objects.get_or_create(authority='(Hufnagel, 1766)')
author2, _ = Author.objects.get_or_create(authority='(Linnaeus, 1758)')

# Create states
wa, _ = State.objects.get_or_create(code='WA')
or_st, _ = State.objects.get_or_create(code='OR')
id_st, _ = State.objects.get_or_create(code='ID')
bc, _ = State.objects.get_or_create(code='BC')

# Create counties
counties_data = [
    ('King', wa), ('Pierce', wa), ('Whatcom', wa), ('Chelan', wa),
    ('Clackamas', or_st), ('Lane', or_st), ('Deschutes', or_st),
    ('Ada', id_st), ('Kootenai', id_st),
]
counties = {}
for name, state in counties_data:
    c, _ = County.objects.get_or_create(name=name, state=state)
    counties[name] = c

# Create collections
wwu, _ = Collection.objects.get_or_create(
    name='WWU Biology Collection',
    defaults={'url': 'https://www.wwu.edu'}
)
wsu, _ = Collection.objects.get_or_create(
    name='WSU James Museum',
    defaults={'url': 'https://entomology.wsu.edu'}
)

# Create collectors
collector1, _ = Collector.objects.get_or_create(name='M. Petersen')
collector2, _ = Collector.objects.get_or_create(name='J. Huddleston')

# Create test species
sp1, _ = Species.objects.get_or_create(
    genus='Agrotis',
    species='ipsilon',
    defaults={
        'common_name': 'Black Cutworm Moth',
        'authority': author1,
    }
)

sp2, _ = Species.objects.get_or_create(
    genus='Noctua',
    species='pronuba',
    defaults={
        'common_name': 'Large Yellow Underwing',
        'authority': author2,
    }
)

# Link as similar species
sp1.similar.add(sp2)

# Specimen records for Agrotis ipsilon (spread across PNW)
records_data = [
    # (lat, lon, county, state, collection, collector, year, month, day, elevation, locality)
    (48.75, -122.48, 'Whatcom', wa, wwu, collector1, 2015, 7, 12, 100, 'Bellingham, Sehome Hill'),
    (48.77, -122.41, 'Whatcom', wa, wwu, collector1, 2015, 8, 3, 50, 'Bellingham, WWU campus'),
    (48.85, -122.76, 'Whatcom', wa, wwu, collector2, 2016, 6, 22, 200, 'Bellingham, Chuckanut Dr'),
    (47.61, -122.33, 'King', wa, wsu, collector2, 2014, 7, 15, 50, 'Seattle, Discovery Park'),
    (47.56, -122.39, 'King', wa, wsu, collector1, 2017, 8, 1, 130, 'Seattle, Lincoln Park'),
    (47.65, -122.30, 'King', wa, wwu, collector2, 2018, 9, 5, 75, 'Seattle, UW campus'),
    (47.24, -122.44, 'Pierce', wa, wsu, collector1, 2016, 7, 28, 300, 'Tacoma, Point Defiance'),
    (47.44, -120.32, 'Chelan', wa, wsu, collector2, 2019, 6, 15, 700, 'Leavenworth, Icicle Creek'),
    (47.50, -120.66, 'Chelan', wa, wwu, collector1, 2017, 8, 20, 1200, 'Lake Wenatchee area'),
    (45.52, -122.67, 'Clackamas', or_st, wsu, collector2, 2015, 7, 4, 50, 'Portland, Mt Tabor'),
    (44.05, -121.31, 'Deschutes', or_st, wwu, collector1, 2018, 8, 10, 1100, 'Bend, Deschutes River'),
    (44.05, -123.09, 'Lane', or_st, wsu, collector2, 2016, 9, 1, 130, 'Eugene, Skinner Butte'),
    (43.72, -122.14, 'Lane', or_st, wwu, collector1, 2019, 7, 22, 500, 'Oakridge area'),
    (43.60, -116.20, 'Ada', id_st, wsu, collector2, 2017, 6, 30, 830, 'Boise, Foothills'),
    (47.68, -116.78, 'Kootenai', id_st, wsu, collector1, 2015, 8, 14, 680, 'Coeur d\'Alene'),
    (48.42, -122.34, 'Whatcom', wa, wwu, collector1, 2020, 5, 18, 20, 'Skagit Valley, farmland'),
    (46.73, -117.17, None, wa, wsu, collector2, 2018, 7, 7, 770, 'Pullman, WSU campus'),
    (46.85, -121.76, None, wa, wwu, collector1, 2019, 8, 25, 1600, 'Mt Rainier, Paradise'),
    (48.86, -121.68, 'Whatcom', wa, wwu, collector2, 2016, 7, 10, 1000, 'Mt Baker, Heather Meadows'),
    (49.15, -121.75, None, bc, wsu, collector1, 2017, 6, 5, 400, 'Chilliwack, BC'),
]

for lat, lon, county_name, state, collection, collector, year, month, day, elev, locality in records_data:
    county = counties.get(county_name) if county_name else None
    SpeciesRecord.objects.get_or_create(
        species=sp1,
        latitude=lat,
        longitude=lon,
        year=year,
        month=month,
        day=day,
        defaults={
            'county': county,
            'state': state,
            'collection': collection,
            'collector': collector,
            'elevation': elev,
            'locality': locality,
            'record_type': 'specimen',
        }
    )

# Records for Noctua pronuba
records_np = [
    (48.73, -122.49, 'Whatcom', wa, wwu, collector1, 2018, 8, 5, 80, 'Bellingham, Whatcom Falls'),
    (47.60, -122.32, 'King', wa, wsu, collector2, 2019, 7, 20, 50, 'Seattle, Volunteer Park'),
    (45.51, -122.68, 'Clackamas', or_st, wsu, collector1, 2017, 9, 12, 60, 'Portland, Forest Park'),
    (44.06, -123.10, 'Lane', or_st, wwu, collector2, 2020, 8, 1, 140, 'Eugene, Spencer Butte'),
    (43.62, -116.21, 'Ada', id_st, wsu, collector1, 2018, 7, 15, 850, 'Boise, Reserve area'),
]

for lat, lon, county_name, state, collection, collector, year, month, day, elev, locality in records_np:
    county = counties.get(county_name) if county_name else None
    SpeciesRecord.objects.get_or_create(
        species=sp2,
        latitude=lat,
        longitude=lon,
        year=year,
        month=month,
        day=day,
        defaults={
            'county': county,
            'state': state,
            'collection': collection,
            'collector': collector,
            'elevation': elev,
            'locality': locality,
            'record_type': 'specimen',
        }
    )

# Create CMS factsheet pages
# The factsheet template looks up species by page title
def ensure_page(title, template, slug=None):
    pages = Page.objects.filter(title_set__title=title)
    if pages.exists():
        return pages[0]
    return create_page(title, template, 'en', published=True, created_by=admin, slug=slug)

ensure_page('Home', 'cms/home.html', slug='home')
ensure_page('Browse', 'cms/browse.html', slug='browse')

# Factsheet pages — title must match "Genus species" exactly
fs1 = ensure_page('Agrotis ipsilon', 'cms/factsheet.html', slug='agrotis-ipsilon')
fs2 = ensure_page('Noctua pronuba', 'cms/factsheet.html', slug='noctua-pronuba')

# Link species to their factsheet pages
sp1.factsheet = fs1
sp1.save()
sp2.factsheet = fs2
sp2.save()

print 'Seeded:'
print '  %d species' % Species.objects.count()
print '  %d records' % SpeciesRecord.objects.count()
print '  %d CMS pages' % Page.objects.count()
print ''
print 'Test URLs:'
print '  http://localhost:8000/agrotis-ipsilon/'
print '  http://localhost:8000/noctua-pronuba/'
print '  http://localhost:8000/admin/ (admin/admin)'
