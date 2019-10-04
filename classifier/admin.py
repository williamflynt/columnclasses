from django.contrib import admin
from classifier.models import Source, Classification, Column


class ColumnInline(admin.TabularInline):
    model = Column


@admin.register(Source)
class SourceAdmin(admin.ModelAdmin):
    inlines = [ColumnInline]


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    pass


@admin.register(Classification)
class ClassificationAdmin(admin.ModelAdmin):
    pass
