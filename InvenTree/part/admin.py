from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import PartCategory, Part
from .models import PartAttachment, PartStar
from .models import BomItem


class PartAdmin(ImportExportModelAdmin):

    list_display = ('full_name', 'description', 'total_stock', 'category')


class PartCategoryAdmin(ImportExportModelAdmin):

    list_display = ('name', 'pathstring', 'description')


class PartAttachmentAdmin(admin.ModelAdmin):

    list_display = ('part', 'attachment', 'comment')


class PartStarAdmin(admin.ModelAdmin):

    list_display = ('part', 'user')


class BomItemAdmin(ImportExportModelAdmin):
    list_display = ('part', 'sub_part', 'quantity')


"""
class ParameterTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'units', 'format')


class ParameterAdmin(admin.ModelAdmin):
    list_display = ('part', 'template', 'value')
"""

admin.site.register(Part, PartAdmin)
admin.site.register(PartCategory, PartCategoryAdmin)
admin.site.register(PartAttachment, PartAttachmentAdmin)
admin.site.register(PartStar, PartStarAdmin)
admin.site.register(BomItem, BomItemAdmin)
