from django.contrib import admin
from django.utils.html import format_html
from django.contrib.admin import SimpleListFilter

from .models import Car, CarAttribute, CarAttributeValue, CarFeature, CarFeatureAssociation


class CarAttributeFilter(SimpleListFilter):
    title = 'attribute'
    parameter_name = 'attribute'

    def lookups(self, request, model_admin):
        return [(attribute.name, attribute.name) for attribute in CarAttribute.objects.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(attributes__attribute__name=self.value())
        return queryset


class CarAttributeValueInline(admin.TabularInline):
    model = CarAttributeValue
    extra = 1


class CarFeatureAssociationInline(admin.TabularInline):
    model = CarFeatureAssociation
    extra = 1


class CarAdmin(admin.ModelAdmin):
    def thumbnail(self, car: Car):
        return format_html(f'<img src="{car.main_photo.url}" width="40" style="border-radius: 50px" />')

    thumbnail.short_description = "Photo"

    list_display = ('thumbnail', 'title', 'brand', 'model', 'year', 'price', 'is_featured')
    search_fields = ('title', 'description')
    list_editable = ('is_featured',)
    inlines = [CarAttributeValueInline, CarFeatureAssociationInline]

    fieldsets = (
        (None, {
            'fields': ('title', 'price', 'brand', 'model', 'year', 'description', 'address', 'is_featured')
        }),
        ('Photos', {
            'fields': ('main_photo', 'photo_2', 'photo_3', 'photo_4', 'photo_5')
        }),
    )

    readonly_fields = ('main_photo_preview', 'photo_2_preview', 'photo_3_preview', 'photo_4_preview', 'photo_5_preview')

    def main_photo_preview(self, obj):
        return obj.main_photo and f'<img src="{obj.main_photo.url}" width="100" />' or ''

    main_photo_preview.short_description = 'Photo 1 Preview'
    main_photo_preview.allow_tags = True

    def photo_2_preview(self, obj):
        return obj.photo_2 and f'<img src="{obj.photo_2.url}" width="100" />' or ''

    photo_2_preview.short_description = 'Photo 2 Preview'
    photo_2_preview.allow_tags = True

    def photo_3_preview(self, obj):
        return obj.photo_3 and f'<img src="{obj.photo_3.url}" width="100" />' or ''

    photo_3_preview.short_description = 'Photo 3 Preview'
    photo_3_preview.allow_tags = True

    def photo_4_preview(self, obj):
        return obj.photo_4 and f'<img src="{obj.photo_4.url}" width="100" />' or ''

    photo_4_preview.short_description = 'Photo 4 Preview'
    photo_4_preview.allow_tags = True

    def photo_5_preview(self, obj):
        return obj.photo_5 and f'<img src="{obj.photo_5.url}" width="100" />' or ''

    photo_5_preview.short_description = 'Photo 5 Preview'
    photo_5_preview.allow_tags = True

    def get_list_filter(self, request):
        default_filters = ['price']

        attribute_filters = []
        for attr in CarAttribute.objects.all():
            class_name = f"FilterBy{attr.name}"

            def lookups(self, request, model_admin, attribute_name=attr.name):
                # Return distinct values for the attribute
                values = CarAttributeValue.objects.filter(attribute__name=attribute_name).distinct().values_list(
                    'value', 'value')
                return values

            def queryset(self, request, queryset, attribute_name=attr.name):
                if self.value():
                    return queryset.filter(attributes__attribute__name=attribute_name, attributes__value=self.value())
                return queryset

            FilterClass = type(class_name, (CarAttributeFilter,), {
                "title": attr.name,
                "parameter_name": f"attribute_{attr.id}",
                "lookups": lookups,
                "queryset": queryset,
            })
            attribute_filters.append(FilterClass)

        return default_filters + attribute_filters

    def attribute_value(self, attr_name):
        """Returns a function that fetches the CarAttributeValue for the given attribute name"""

        def _inner(car):
            value = car.attributes.filter(attribute__name=attr_name).first()
            return value.value if value else '-'

        _inner.__name__ = attr_name
        _inner.short_description = attr_name
        return _inner

    def get_list_display(self, request):
        default_fields = ['thumbnail', 'title', 'brand', 'model', 'year', 'price', 'is_featured']
        attribute_fields = [self.attribute_value(attr.name) for attr in
                            CarAttribute.objects.filter(carattributevalue__isnull=False).distinct()]

        return default_fields + attribute_fields


@admin.register(CarAttribute)
class CarAttributeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(CarFeature)
class CarFeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


admin.site.register(Car, CarAdmin)
