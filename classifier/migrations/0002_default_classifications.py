# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import migrations, models


def add_defaults(apps, schema_editor):
    """add some default classifications"""
    Classification = apps.get_model("classifier", "Classification")

    predir = Classification.objects.create(label="pre", description="A zipcode (US, Canadian or otherwise)")
    postdir = Classification.objects.create(label="post", description="A zipcode (US, Canadian or otherwise)")
    direction = Classification.objects.create(label="direction", description="A zipcode (US, Canadian or otherwise)", main=True)
    direction.subclasses.add(predir)
    direction.subclasses.add(postdir)

    mailing = Classification.objects.create(label="mailing", description="Relates to the mailing address")
    situs = Classification.objects.create(label="situs", description="Relates to the situs/property address")

    fulladdr = Classification.objects.create(label="fulladdr", description="A full address in one cell", main=True)
    street = Classification.objects.create(label="street", description="A street address", main=True)
    city = Classification.objects.create(label="city", description="A city name", main=True)
    state = Classification.objects.create(label="state", description="A state or province name", main=True)
    zipcode = Classification.objects.create(label="zipcode", description="A zipcode (US, Canadian or otherwise)", main=True)
    housenumber = Classification.objects.create(label="housenumber", description="A zipcode (US, Canadian or otherwise)", main=True)
    streetname = Classification.objects.create(label="streetname", description="A zipcode (US, Canadian or otherwise)", main=True)
    unit = Classification.objects.create(label="unit", description="A zipcode (US, Canadian or otherwise)", main=True)
    # TODO: part street name, street type, unit num, unit type

    for item in [fulladdr, street, city, state, zipcode, housenumber, streetname, unit]:
        item.subclasses.add(mailing)
        item.subclasses.add(situs)

    fullname = Classification.objects.create(label="fullname", description="One or many person names in one cell", main=True)
    partname = Classification.objects.create(label="partname", description="A name component or incomplete name.", main=True)
    first = Classification.objects.create(label="first", description="A first name")
    middle = Classification.objects.create(label="middle", description="A middle name or initial")
    last = Classification.objects.create(label="last", description="A surname")
    partname.subclasses.add(first)
    partname.subclasses.add(middle)
    partname.subclasses.add(last)

    phone = Classification.objects.create(label="phone", description="A phone number", main=True)

    email = Classification.objects.create(label="email", description="An email address", main=True)

    fips = Classification.objects.create(label="fips", description="FIPS code for a county")
    countyname = Classification.objects.create(label="countyname", description="Textual name of the county")
    county = Classification.objects.create(label="county", description="A county identifier", main=True)
    county.subclasses.add(fips)
    county.subclasses.add(countyname)

    apn = Classification.objects.create(label="apn", description="A parcel number", main=True)

    reject = Classification.objects.create(label="", description="A value we don't care about", main=True)


class Migration(migrations.Migration):

    dependencies = [("classifier", "0001_initial")]

    operations = [migrations.RunPython(add_defaults)]
