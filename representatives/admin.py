import traceback

from django.contrib import admin, messages

from representatives.models import (
    Candidate,
    Election,
    Representative,
    RepresentativeSet,
    app_settings,
)


@admin.register(RepresentativeSet)
class RepresentativeSetAdmin(admin.ModelAdmin):
    actions = ['update_from_data_source']
    list_display = ['name', 'last_import_time', 'last_import_successful', 'enabled']
    list_filter = ['last_import_successful', 'enabled']

    @admin.action(
        description="Update from data source"
    )
    def update_from_data_source(self, request, queryset):
        for individual_set in queryset:
            try:
                count = individual_set.update_from_data_source()
            except Exception:
                messages.error(request, "Couldn't update individuals in {}: {}".format(individual_set, traceback.format_exc()))
                continue
            if count is False:
                messages.error(request, "Couldn't update individuals in %s." % individual_set)
            else:
                message = "Updated {} individuals in {}.".format(count, individual_set)
                no_boundaries = individual_set.individuals.filter(boundary='').values_list('name', flat=True)
                if no_boundaries:
                    messages.warning(request, message + " %d match no boundary (%s)." % (len(no_boundaries), ', '.join(no_boundaries)))
                else:
                    messages.success(request, message)


@admin.register(Representative)
class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ['name', 'representative_set', 'district_name', 'elected_office', 'boundary']
    list_filter = ['representative_set']
    search_fields = ['name', 'district_name', 'elected_office']


class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'election', 'district_name', 'elected_office', 'boundary']
    list_filter = ['election']
    search_fields = ['name', 'district_name', 'elected_office']


if app_settings.ENABLE_CANDIDATES:
    admin.site.register(Election, RepresentativeSetAdmin)
    admin.site.register(Candidate, CandidateAdmin)
