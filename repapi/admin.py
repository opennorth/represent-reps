from django.contrib import admin

from repapi.models import Representative, RepresentativeSet

class RepresentativeSetAdmin(admin.ModelAdmin):

    actions = ['update_from_scraperwiki']

    def update_from_scraperwiki(self, request, queryset):
        for rset in queryset:
            num_updated = rset.update_from_scraperwiki()
            self.message_user(request, "Updated %s representatives for %s" % (num_updated, rset))
    update_from_scraperwiki.short_description = "Update from ScraperWiki"
    
class RepresentativeAdmin(admin.ModelAdmin):
    list_display = ['name', 'representative_set', 'district_name', 'elected_office', 'boundary_url']
    list_filter = ['representative_set']
    search_fields = ['name', 'district_name', 'elected_office']
    
admin.site.register(Representative, RepresentativeAdmin)
admin.site.register(RepresentativeSet, RepresentativeSetAdmin)