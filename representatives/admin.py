from django.contrib import admin, messages

from representatives.models import *

class RepresentativeSetAdmin(admin.ModelAdmin):

    actions = ['update_from_scraperwiki']
    list_display = ['name', 'last_import_time', 'last_scrape_time', 'last_scrape_successful', 'enabled']
    list_filter = ['last_scrape_successful', 'enabled']

    def update_from_scraperwiki(self, request, queryset):
        for rset in queryset:
            try:
                num_updated = rset.update_from_scraperwiki()
            except Exception as e:
                messages.error(request, u"Fatal error updating %s: %s" % (rset, e))
                continue
            if num_updated is False:
                messages.error(request, "%s could not be updated." % rset)
            else:
                msg = "Updated %s representatives for %s." % (num_updated, rset)
                no_boundaries = Representative.objects.filter(representative_set=rset, boundary='').count()
                if no_boundaries:
                    messages.warning(request, msg + " %s did not match a boundary." % no_boundaries)
                else:
                    messages.success(request, msg + " All matched a boundary.")
    update_from_scraperwiki.short_description = "Update from ScraperWiki"
    
class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ['name', 'representative_set', 'district_name', 'elected_office', 'boundary']
    list_filter = ['representative_set']
    search_fields = ['name', 'district_name', 'elected_office']

class CandidateAdmin(admin.ModelAdmin):
    list_display = ['name', 'election', 'district_name', 'elected_office', 'boundary']
    list_filter = ['election']
    search_fields = ['name', 'district_name', 'elected_office']    
    
admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(RepresentativeSet, RepresentativeSetAdmin)
if app_settings.ENABLE_CANDIDATES:
    admin.site.register(Candidate, CandidateAdmin)
    admin.site.register(Election, RepresentativeSetAdmin)
