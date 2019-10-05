# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


def add_defaults(apps, schema_editor):
    """add some default classifications"""
    Classification = apps.get_model("classifier", "Classification")

    fulladdr = Classification.objects.create(label="fulladdr", description="A full address in one cell")
    street = Classification.objects.create(label="street", description="A street address")
    city = Classification.objects.create(label="city", description="A city name")
    state = Classification.objects.create(label="state", description="A state or province name")
    zipcode = Classification.objects.create(label="zipcode", description="A zipcode (US, Canadian or otherwise)")
    housenumber = Classification.objects.create(label="housenumber", description="A zipcode (US, Canadian or otherwise)")
    streetdir = Classification.objects.create(label="streetdir", description="A zipcode (US, Canadian or otherwise)")
    streetname = Classification.objects.create(label="streetname", description="A zipcode (US, Canadian or otherwise)")
    unit = Classification.objects.create(label="unit", description="A zipcode (US, Canadian or otherwise)")

    mailing = Classification.objects.create(label="mailing", description="Relates to the mailing address", main=True)
    situs = Classification.objects.create(label="situs", description="Relates to the situs/property address", main=True)
    for item in [mailing, situs]:
        item.subclasses.add(fulladdr)
        item.subclasses.add(street)
        item.subclasses.add(city)
        item.subclasses.add(state)
        item.subclasses.add(zipcode)
        item.subclasses.add(housenumber)
        item.subclasses.add(streetdir)
        item.subclasses.add(streetname)
        item.subclasses.add(unit)

    fullname = Classification.objects.create(label="fullname", description="A single person's full name in one cell")
    first = Classification.objects.create(label="first", description="A first name")
    middle = Classification.objects.create(label="middle", description="A middle name or initial")
    last = Classification.objects.create(label="last", description="A surname")
    multiname = Classification.objects.create(label="multiname", description="More than one person's name in one cell")
    name = Classification.objects.create(label="name", description="Relates to the owning entity name", main=True)
    name.subclasses.add(fullname)
    name.subclasses.add(first)
    name.subclasses.add(middle)
    name.subclasses.add(last)
    name.subclasses.add(multiname)

    phone = Classification.objects.create(label="phone", description="A phone number", main=True)

    email = Classification.objects.create(label="email", description="An email address", main=True)

    fips = Classification.objects.create(label="fips", description="FIPS code for a county")
    countyname = Classification.objects.create(label="countyname", description="Textual name of the county")
    county = Classification.objects.create(label="county", description="A county identifier", main=True)
    county.subclasses.add(fips)
    county.subclasses.add(countyname)

    apn = Classification.objects.create(label="apn", description="A parcel number", main=True)

    dontcare = Classification.objects.create(label="", description="A value we don't care about", main=True)


class Migration(migrations.Migration):

    dependencies = [("classifier", "0001_initial")]

    operations = [migrations.RunPython(add_defaults)]
